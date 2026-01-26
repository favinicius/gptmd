
import subprocess
import time
import os
import csv
import re
import json
from datetime import datetime
from pathlib import Path

# --- CONFIGURAÇÃO DE CENÁRIOS ---
INSTRUCTION_PATH = "input/cenario-metalmec.txt"
MODELS = ["gemini-2.0-flash", "gemini-2.0-flash-lite"]
SIZING_MODES = ["standard", "secure", "aggressive"]
CONTINGENCY_LEVELS = ["standard", "high"]

# Interpretador (Respeitando a regra de Venv Externo: ../venvs/gptmd)
PYTHON_EXE = os.path.abspath(os.path.join(os.path.dirname(os.getcwd()), "venvs", "gptmd", "bin", "python3"))
if not os.path.exists(PYTHON_EXE):
    PYTHON_EXE = "python3" # Fallback

def extract_metrics(output_msg):
    """
    Extrai métricas do stdout do main.py via Regex.
    """
    data = {
        "price": "N/A",
        "hours": "0",
        "acts": "0",
        "tokens": "0",
        "out_dir": "N/A"
    }
    
    # 1. Busca Price (Valor de Venda final)
    price_match = re.search(r"Calculated Total: R\$ ([\d\.,]+)", output_msg)
    if price_match: data["price"] = price_match.group(1)
    
    # 2. Busca Tokens Prompt ([METRICS])
    token_match = re.search(r"TOKENS_PROMPT=(\d+)", output_msg)
    if token_match: data["tokens"] = token_match.group(1)
    
    # 3. Busca Horas e Atividades
    # Ex: "- 113 atividades planejadas (1470 horas)"
    metrics_match = re.search(r"- (\d+) atividades.*?\((\d+\.?\d*) horas\)", output_msg)
    if metrics_match:
        data["acts"] = metrics_match.group(1)
        data["hours"] = metrics_match.group(2)
        
    # 4. Busca Pasta de Saída
    folder_match = re.search(r"saved to: (output/[0-9\-_]+)", output_msg)
    if folder_match: data["out_dir"] = folder_match.group(1).strip()
    
    return data

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path("output/benchmarks")
    out_dir.mkdir(parents=True, exist_ok=True)
    report_file = out_dir / f"benchmark_matrix_{timestamp}.csv"
    
    print(f"\n🚀 GPT-Md ROBUST BENCHMARK (V3.1)")
    print(f"📄 Arquivo de resultados: {report_file}")
    print(f"🎯 Cenário: {INSTRUCTION_PATH}")
    print(f"🐍 Python: {PYTHON_EXE}")
    print("-" * 145)
    
    headers = ["Model", "Sizing", "Contingcy", "Price (R$)", "Hours", "Acts", "Tok(In)", "Time(s)", "Status", "Folder"]
    print(f"{headers[0]:<22} | {headers[1]:<10} | {headers[2]:<10} | {headers[3]:<15} | {headers[4]:<6} | {headers[5]:<5} | {headers[6]:<8} | {headers[7]:<7} | {headers[8]:<6} | {headers[9]}")
    print("-" * 145)
    
    with open(report_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(headers)
        
        for model in MODELS:
            for sz in SIZING_MODES:
                for ct in CONTINGENCY_LEVELS:
                    
                    cmd = [
                        PYTHON_EXE, "src/main.py",
                        "--instruction", INSTRUCTION_PATH,
                        "--sizing", sz,
                        "--contingency", ct,
                        "--debug"
                    ]
                    
                    env = os.environ.copy()
                    env["PYTHONPATH"] = "."
                    env["GEMINI_MODEL"] = model
                    
                    start_time = time.time()
                    try:
                        # Execução isolada com timeout de 5 minutos
                        proc = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=300)
                        duration = time.time() - start_time
                        
                        # Combina stdout e stderr para análise
                        full_output = proc.stdout + "\n" + proc.stderr
                        metrics = extract_metrics(full_output)
                        
                        status = "✅" if proc.returncode == 0 else "❌"
                        if "Quota Excedida" in full_output:
                            status = "🚨 Q" # Quota
                        
                        row = [
                            model, sz, ct, 
                            metrics["price"], metrics["hours"], metrics["acts"], 
                            metrics["tokens"], round(duration, 1), status, metrics["out_dir"]
                        ]
                        
                        print(f"{row[0]:<22} | {row[1]:<10} | {row[2]:<10} | {row[3]:<15} | {row[4]:<6} | {row[5]:<5} | {row[6]:<8} | {row[7]:<7} | {row[8]:<6} | {row[9]}")
                        writer.writerow(row)
                        f.flush() # Salva imediatamente no disco
                        
                    except subprocess.TimeoutExpired:
                        print(f"{model:<22} | {sz:<10} | {ct:<10} | {'TIMEOUT':<15} | {'-':<6} | {'-':<5} | {'-':<8} | {300:<7} | {'⏱️':<6} | -")
                        writer.writerow([model, sz, ct, "TIMEOUT", 0, 0, 0, 300, "TIMEOUT", "N/A"])
                        f.flush()
                    except Exception as e:
                        print(f"Erro Crítico em {model}/{sz}/{ct}: {str(e)[:50]}")
                    
                    # Pausa de segurança entre execuções para ajudar a API a respirar
                    time.sleep(2)
                    
            print("-" * 145)
            
    print(f"\n🏁 Benchmark Concluído com Sucesso!")
    print(f"📊 Resultados salvos em: {report_file}")

if __name__ == "__main__":
    main()
