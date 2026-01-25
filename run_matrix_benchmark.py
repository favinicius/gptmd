
import subprocess
import time
import re
import os
import csv
from datetime import datetime

# Configurações do teste
INSTRUCTION = "input/cenario-metalmec.txt"

# Lista de Modelos para Teste
MODELS = [
    os.getenv("GEMINI_MODEL", "gemini-2.0-flash-lite"),
    "gemini-2.0-flash"
]

# Matriz de Validacao de Temperatura
SIZING_MODES = ["standard", "secure", "aggressive"]
CONTINGENCY_LEVELS = ["standard", "high"]

def run_calc(model, sizing, contingency):
    # Busca o interpretador do venv conforme padrão do usuário
    python_exe = os.path.join(os.path.dirname(os.getcwd()), "venvs", "gptmd", "bin", "python3")
    if not os.path.exists(python_exe):
        python_exe = "python3" # Fallback
    
    cmd = [
        python_exe, "src/main.py",
        "--instruction", INSTRUCTION,
        "--sizing", sizing,
        "--contingency", contingency,
        "--debug"
    ]
    
    env = os.environ.copy()
    env["PYTHONPATH"] = "."
    env["GEMINI_MODEL"] = model
    
    while True: # Retry Loop Infinito para Quota
        start_time = time.time()
        try:
            # Executa capturando stdout e stderr
            result = subprocess.run(cmd, capture_output=True, text=True, env=env)
            duration = time.time() - start_time
            
            output = result.stdout + "\n" + result.stderr
            
            # Detecção de Erro de Quota - Gatilho para Espera
            if "Quota Excedida" in output or "cooldown" in output.lower():
                # Filtrar e mostrar quais chaves falharam
                quota_errors = [line for line in output.splitlines() if "[!]" in line]
                for err in quota_errors:
                    print(f"   ↳ {err}")
                
                print(f"⏳ [QUOTA HIT] Aguardando 60s para liberar API do Google... ({model})")
                time.sleep(60)
                continue # Tenta novamente a mesma execução
            
            # Analisa Saída (Sucesso ou Erro Técnico)
            price_match = re.search(r"Calculated Total: R\$ ([\d\.,]+)", result.stdout)
            metrics_match = re.search(r"- (\d+) atividades.*?\(([\d\.]+)\s+horas\)", result.stdout)
            
            # 2. Métricas de IA (Capturadas do log [METRICS])
            tokens_prompt = 0
            tokens_output = 0
            metrics_lines = re.findall(r"\[METRICS\].*?TOKENS_PROMPT=(\d+).*?TOKENS_OUTPUT=(\d+)", result.stdout)
            for p, o in metrics_lines:
                tokens_prompt += int(p)
                tokens_output += int(o)
                
            error_msg = None
            if result.returncode != 0:
                error_msg = result.stderr.splitlines()[-1] if result.stderr else 'Unknown Error'

            return {
                "price": price_match.group(1) if price_match else "N/A",
                "activities": metrics_match.group(1) if metrics_match else "0",
                "hours": metrics_match.group(2) if metrics_match else "0",
                "duration": round(duration, 2),
                "tokens_prompt": tokens_prompt,
                "tokens_output": tokens_output,
                "tokens_total": tokens_prompt + tokens_output,
                "error": error_msg
            }
            
        except Exception as e:
            return {
                "price": "Fail",
                "activities": 0,
                "hours": 0,
                "duration": round(time.time() - start_time, 2),
                "tokens_prompt": 0,
                "tokens_output": 0,
                "tokens_total": 0,
                "error": str(e)
            }

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Garantir pasta de output de benchmark (v7.1)
    out_dir = os.path.join("output", "benchmarks")
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    filename = os.path.join(out_dir, f"benchmark_matrix_{timestamp}.csv")
    
    print(f"\n🚀 Iniciando Matriz de Benchmark GPT-Md (Modelos x Temperaturas)")
    print(f"📄 Arquivo de saída: {filename}")
    print(f"🎯 Cenário: '{INSTRUCTION}'")
    print("-" * 150)
    
    headers = ["Model", "Sizing", "Contingcy", "Acts", "Hours", "Cost (R$)", "M. Run(s)", "M. Tok (tot)", "Status"]
    print(f"{headers[0]:<22} | {headers[1]:<10} | {headers[2]:<10} | {headers[3]:<5} | {headers[4]:<6} | {headers[5]:<15} | {headers[6]:<10} | {headers[7]:<12} | {headers[8]}")
    print("-" * 150)
    
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Model", "Sizing", "Contingency", "Price", "Activities", "Total_Hours", "Duration_Seconds", "Tokens_Total", "Tokens_Input", "Tokens_Output", "Error"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    
        for model in MODELS:
            for sz in SIZING_MODES:
                for ct in CONTINGENCY_LEVELS:
                    
                    data = run_calc(model, sz, ct)
                    
                    is_error = bool(data["error"])
                    status = "✅" if not is_error else "❌"
                    if is_error and "404" in str(data["error"]): status = "🚫 (N/A)"
                    
                    print(f"{model:<22} | {sz:<10} | {ct:<10} | {data['activities']:<5} | {data['hours']:<6} | {data['price']:<15} | {data['duration']:<10} | {data['tokens_total']:<12} | {status}")
                    
                    row = {
                        "Model": model,
                        "Sizing": sz,
                        "Contingency": ct,
                        "Price": data['price'],
                        "Activities": data['activities'],
                        "Total_Hours": data['hours'],
                        "Duration_Seconds": data['duration'],
                        "Tokens_Total": data['tokens_total'],
                        "Tokens_Input": data['tokens_prompt'],
                        "Tokens_Output": data['tokens_output'],
                        "Error": data['error'] or ""
                    }
                    
                    writer.writerow(row)
                    
            print("-" * 150) # Separador entre modelos
        
    print("🏁 Benchmark Cartesiano Concluído.")

if __name__ == "__main__":
    main()
