
import subprocess
import time
import re
import os
import csv
from datetime import datetime

# Configurações do teste
INSTRUCTION = "Instalação de 1 Servidor e 1 Switch na OFI Ilhéus. Cliente fornece hardware."

# Modelos para Teste (Sincronizado com API)
MODELS = [
    "gemini-2.0-flash",        # Nova geração 2.0
    "gemini-flash-latest",     # Alias estável para 1.5 Flash
    "gemini-pro-latest",       # Alias robusto para 1.5 Pro
    "gemini-2.5-flash"         # Próxima geração 2.5
]

# Configuração Padrão para Benchmark e Comparação Justa
SIZING = "standard"
CONTINGENCY = "standard"

def run_calc(model):
    # Ajustado para seguir a regra de Venv Externo: ../venvs/gptmd
    python_exe = os.path.join(os.path.dirname(os.getcwd()), "venvs", "gptmd", "bin", "python")
    
    cmd = [
        python_exe, "src/main.py",
        "--instruction", INSTRUCTION,
        "--sizing", SIZING,
        "--contingency", CONTINGENCY,
        "--debug"
    ]
    
    env = os.environ.copy()
    env["PYTHONPATH"] = "."
    env["GEMINI_MODEL"] = model
    
    start_time = time.time()
    try:
        # Executa capturando stdout e stderr
        result = subprocess.run(cmd, capture_output=True, text=True, env=env)
        duration = time.time() - start_time
        
        # Analisa Saída
        output = result.stdout
        
        # 2. Métricas de Negócio (Atualizado para float)
        price_match = re.search(r"Calculated Total: R\$ ([\d\.,]+)", output)
        metrics_match = re.search(r"- (\d+) atividades.*?\((\d+\.?\d*) horas\)", output)
        
        # 3. Métricas de IA (Capturadas do log [METRICS])
        tokens_prompt = 0
        tokens_output = 0
        
        metrics_lines = re.findall(r"TOKENS_PROMPT=(\d+)", output)
        for p in metrics_lines:
            tokens_prompt += int(p)
            
        error_msg = None
        if result.returncode != 0:
            # Busca por "ERRO CRÍTICO" na saída para ser mais específico
            critical_error = re.search(r"ERRO CRÍTICO.*?: (.*)", output)
            if critical_error:
                error_msg = critical_error.group(1).strip()[:50]
            else:
                error_msg = result.stderr.splitlines()[-1] if result.stderr else 'Process Error'

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
    filename = f"benchmark_models_{timestamp}.csv"
    
    print(f"\n🚀 Iniciando Benchmark de Modelos Gemini")
    print(f"📄 Arquivo de saída: {filename}")
    print(f"🎯 Cenário: '{INSTRUCTION}'")
    print("-" * 140)
    
    headers = ["Model", "Price (R$)", "Acts", "Hours", "Time(s)", "Tok(In)", "Tok(Out)", "Tok(Tot)", "Status"]
    print(f"{headers[0]:<25} | {headers[1]:<15} | {headers[2]:<5} | {headers[3]:<6} | {headers[4]:<7} | {headers[5]:<8} | {headers[6]:<8} | {headers[7]:<8} | {headers[8]}")
    print("-" * 140)
    
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Model", "Price", "Activities", "Hours", "Duration_Seconds", "Tokens_Input", "Tokens_Output", "Tokens_Total", "Error"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    
        for model in MODELS:
            data = run_calc(model)
            
            is_error = bool(data["error"])
            status = "✅" if not is_error else "❌"
            if is_error and "404" in  str(data["error"]): status = "🚫 (N/A)" # Modelo não existe
            
            print(f"{model:<25} | {data['price']:<15} | {data['activities']:<5} | {data['hours']:<6} | {data['duration']:<7} | {data['tokens_prompt']:<8} | {data['tokens_output']:<8} | {data['tokens_total']:<8} | {status}")
            
            row = {
                "Model": model,
                "Price": data['price'],
                "Activities": data['activities'],
                "Hours": data['hours'],
                "Duration_Seconds": data['duration'],
                "Tokens_Input": data['tokens_prompt'],
                "Tokens_Output": data['tokens_output'],
                "Tokens_Total": data['tokens_total'],
                "Error": data['error'] or ""
            }
            
            writer.writerow(row)
            
            # Pequena pausa para evitar rate limit agressivo entre modelos
            time.sleep(2)
        
    print("-" * 140)
    print("🏁 Benchmark concluído.")

if __name__ == "__main__":
    main()
