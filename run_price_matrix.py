
import subprocess
import time
import re
import os
import csv
from datetime import datetime

# Configurações do teste
INSTRUCTION = "Instalação de 1 Servidor e 1 Switch na OFI Ilhéus. Cliente fornece hardware."

# Parâmetros de Teste
SIZING_MODES = ["standard", "secure"] # Reduzi para o teste ser mais rápido, mas pode expandir
CONTINGENCY_LEVELS = ["standard", "high"]
MODELS = ["gemini-2.0-flash-exp", "gemini-1.5-flash"] # Modelos para benchmark

def run_calc(model, sizing, contingency):
    # Caminho absoluto para o python do venv
    python_exe = os.path.join(os.getcwd(), "venv", "bin", "python3")
    
    cmd = [
        python_exe, "src/main.py",
        "--instruction", INSTRUCTION,
        "--sizing", sizing,
        "--contingency", contingency
    ]
    
    env = os.environ.copy()
    env["PYTHONPATH"] = "."
    env["GEMINI_MODEL"] = model
    
    start_time = time.time()
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, env=env)
        duration = time.time() - start_time
        
        if result.returncode != 0:
            error_msg = result.stderr.splitlines()[-1] if result.stderr else 'Unknown Error'
            return {
                "price": "Error",
                "activities": 0,
                "hours": 0,
                "duration": round(duration, 2),
                "error": error_msg
            }
            
        # Parse Output
        # Padrão esperado: 
        # Calculated Total: R$ 477.770,25
        #   - 113 atividades planejadas (1470 horas)
        
        price_match = re.search(r"Calculated Total: R\$ ([\d\.,]+)", result.stdout)
        metrics_match = re.search(r"- (\d+) atividades.*?\((\d+) horas\)", result.stdout)
        
        return {
            "price": price_match.group(1) if price_match else "N/A",
            "activities": metrics_match.group(1) if metrics_match else "0",
            "hours": metrics_match.group(2) if metrics_match else "0",
            "duration": round(duration, 2),
            "error": None
        }
        
    except Exception as e:
        return {
            "price": "Fail",
            "activities": 0,
            "hours": 0,
            "duration": round(time.time() - start_time, 2),
            "error": str(e)
        }

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"benchmark_results_{timestamp}.csv"
    
    print(f"\n🚀 Iniciando Benchmark GPT-Md")
    print(f"📄 Arquivo de saída: {filename}")
    print(f"🎯 Cenário: '{INSTRUCTION}'")
    print("-" * 110)
    
    headers = ["Model", "Sizing", "Contingency", "Price (R$)", "Activities", "Hours", "Time (s)", "Status"]
    print(f"{headers[0]:<20} | {headers[1]:<10} | {headers[2]:<12} | {headers[3]:<15} | {headers[4]:<5} | {headers[5]:<6} | {headers[6]:<6} | {headers[7]}")
    print("-" * 110)
    
    results = []
    
    # Initialize CSV
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Model", "Sizing", "Contingency", "Price", "Activities", "Hours", "Duration_Seconds", "Error"])
        writer.writeheader()
    
    for model in MODELS:
        for sz in SIZING_MODES:
            for ct in CONTINGENCY_LEVELS:
                data = run_calc(model, sz, ct)
                
                status = "✅" if not data["error"] else "❌"
                print(f"{model:<20} | {sz:<10} | {ct:<12} | {data['price']:<15} | {data['activities']:<5} | {data['hours']:<6} | {data['duration']:<6} | {status}")
                
                row = {
                    "Model": model,
                    "Sizing": sz,
                    "Contingency": ct,
                    "Price": data['price'],
                    "Activities": data['activities'],
                    "Hours": data['hours'],
                    "Duration_Seconds": data['duration'],
                    "Error": data['error'] or ""
                }
                
                # Append to CSV
                with open(filename, "a", newline="", encoding="utf-8") as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=row.keys())
                    writer.writerow(row)
        
    print("-" * 110)
    print(f"🏁 Benchmark concluído. {len(results)} cenários executados.")

if __name__ == "__main__":
    main()
