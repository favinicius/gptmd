#!/usr/bin/env python3
"""
Benchmark Robusto v2.0 - Abordagem de Controle + Análise de Artefatos
======================================================================

Estratégia:
1. Executa src/main.py sequencialmente para cada cenário
2. Captura o caminho da pasta output/ gerada
3. Lê os artefatos (CSV, JSON, MD) para extrair métricas
4. Salva progresso incremental em CSV
5. Permite resumo se interrompido

Não trava porque:
- Timeout de 5min por execução
- Sem loops infinitos
- Sem parsing complexo de stdout
- Estado salvo a cada iteração
"""

import subprocess
import time
import os
import re
import csv
import json
from datetime import datetime
from pathlib import Path

# ==================== CONFIGURAÇÕES ====================

INSTRUCTION = "input/cenario-metalmec.txt"

# Modelos para teste
MODELS = [
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite"
]

# Matriz de variações
SIZING_MODES = ["standard", "secure", "aggressive"]
CONTINGENCY_LEVELS = ["standard", "high"]

# Timeout por execução (segundos)
EXECUTION_TIMEOUT = 300  # 5 minutos

# Caminho do Python do venv (seguindo regra do usuário)
PROJECT_DIR = Path(__file__).parent
VENV_PYTHON = PROJECT_DIR.parent / "venvs" / "gptmd" / "bin" / "python3"

if not VENV_PYTHON.exists():
    VENV_PYTHON = Path("python3")  # Fallback para python do sistema

# Arquivo de resultados
RESULTS_FILE = PROJECT_DIR / f"benchmark_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

# Arquivo de registro de progresso (para resumo)
PROGRESS_FILE = PROJECT_DIR / "benchmark_progress.json"

# ==================== FUNÇÕES AUXILIARES ====================

def load_progress():
    """Carrega o registro de progresso para permitir resumo."""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {"completed": []}

def save_progress(scenario_id):
    """Salva o ID do cenário completado."""
    progress = load_progress()
    if scenario_id not in progress["completed"]:
        progress["completed"].append(scenario_id)
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

def run_scenario(model, sizing, contingency):
    """
    Executa src/main.py para um cenário específico.
    
    Retorna:
        (output_path, error_msg) onde output_path é o caminho da pasta gerada
        ou None se houver erro.
    """
    cmd = [
        str(VENV_PYTHON),
        "src/main.py",
        "--instruction", INSTRUCTION,
        "--sizing", sizing,
        "--contingency", contingency,
        "--debug"
    ]
    
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_DIR)
    env["GEMINI_MODEL"] = model
    
    scenario_id = f"{model}_{sizing}_{contingency}"
    print(f"\n{'='*70}")
    print(f"▶️  Executando: {scenario_id}")
    print(f"{'='*70}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=env,
            timeout=EXECUTION_TIMEOUT,
            cwd=PROJECT_DIR
        )
        
        # Procura o caminho do output no stdout
        # Ex: "Output artifacts saved to: output/2026-01-25_21-00-34"
        output_path = None
        for line in result.stdout.splitlines():
            if "Output artifacts saved to:" in line:
                output_path = line.split(":")[-1].strip()
                break
        
        if result.returncode != 0:
            error_msg = result.stderr.strip().splitlines()[-1] if result.stderr else "Erro desconhecido"
            print(f"❌ Falha: {error_msg}")
            return None, error_msg
        
        if not output_path:
            print(f"⚠️  Output path não encontrado no log")
            return None, "Output path não encontrado"
        
        print(f"✅ Concluído: {output_path}")
        return output_path, None
        
    except subprocess.TimeoutExpired:
        print(f"⏱️  TIMEOUT ({EXECUTION_TIMEOUT}s)")
        return None, f"TIMEOUT ({EXECUTION_TIMEOUT}s)"
    except Exception as e:
        print(f"💥 Exceção: {str(e)}")
        return None, str(e)

def extract_metrics(output_path):
    """
    Extrai métricas dos artefatos salvos na pasta output.
    
    Retorna dict com:
        - price: Preço total (string formatada)
        - hours: Total de horas
        - acts: Número de atividades
        - tokens: Tokens consumidos
    """
    metrics = {
        "price": "N/A",
        "hours": 0.0,
        "acts": 0,
        "tokens": 0
    }
    
    path = Path(output_path)
    
    if not path.exists():
        return metrics
    
    # 1. Extrai dados do MOD_*.csv
    mod_files = list(path.glob("MOD_*.csv"))
    if mod_files:
        try:
            with open(mod_files[0], 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f, delimiter=';')
                rows = list(reader)
                metrics["acts"] = len(rows)
                
                # Soma as horas (formato brasileiro: vírgula decimal)
                total_hours = 0.0
                for row in rows:
                    hours_str = row.get("hours", "0").replace(",", ".")
                    try:
                        total_hours += float(hours_str)
                    except ValueError:
                        pass
                metrics["hours"] = round(total_hours, 1)
        except Exception as e:
            print(f"⚠️  Erro ao ler MOD CSV: {e}")
    
    # 2. Extrai preço do PROPOSTA_*.md
    proposta_files = list(path.glob("PROPOSTA_*.md"))
    if proposta_files:
        try:
            content = proposta_files[0].read_text(encoding='utf-8')
            # Procura por "TOTAL GERAL" ou "Valor Total"
            price_match = re.search(r'(?:TOTAL GERAL|Valor Total)[:\s]+R\$\s*([\d.,]+)', content)
            if price_match:
                metrics["price"] = f"R$ {price_match.group(1)}"
        except Exception as e:
            print(f"⚠️  Erro ao ler PROPOSTA MD: {e}")
    
    # 3. Extrai tokens do API_USAGE_STATS.md
    usage_file = path / "API_USAGE_STATS.md"
    if usage_file.exists():
        try:
            content = usage_file.read_text(encoding='utf-8')
            token_match = re.search(r'TOTAL ACUMULADO:.*?\|\s*([\d.,]+)\s*tokens', content)
            if token_match:
                tokens_str = token_match.group(1).replace(".", "").replace(",", "")
                metrics["tokens"] = int(tokens_str)
        except Exception as e:
            print(f"⚠️  Erro ao ler API_USAGE_STATS: {e}")
    
    return metrics

def write_result(writer, model, sizing, contingency, metrics, error=None):
    """Escreve uma linha no CSV de resultados."""
    writer.writerow({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "model": model,
        "sizing": sizing,
        "contingency": contingency,
        "price": metrics["price"] if not error else "ERROR",
        "hours": metrics["hours"] if not error else 0,
        "acts": metrics["acts"] if not error else 0,
        "tokens": metrics["tokens"] if not error else 0,
        "status": "OK" if not error else "FAILED",
        "error": error or ""
    })

# ==================== EXECUÇÃO PRINCIPAL ====================

def main():
    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║          BENCHMARK ROBUSTO v2.0 - GPT-MD                         ║
╚══════════════════════════════════════════════════════════════════╝

📋 Cenário: {INSTRUCTION}
🤖 Modelos: {', '.join(MODELS)}
📊 Sizing: {', '.join(SIZING_MODES)}
🛡️  Contingency: {', '.join(CONTINGENCY_LEVELS)}
⏱️  Timeout: {EXECUTION_TIMEOUT}s por execução
💾 Resultados: {RESULTS_FILE.name}

""")
    
    # Carrega progresso anterior (se houver)
    progress = load_progress()
    completed = set(progress["completed"])
    
    if completed:
        print(f"📌 Resumindo benchmark anterior ({len(completed)} cenários já concluídos)\n")
    
    # Gera lista de cenários
    scenarios = []
    for model in MODELS:
        for sizing in SIZING_MODES:
            for contingency in CONTINGENCY_LEVELS:
                scenario_id = f"{model}_{sizing}_{contingency}"
                if scenario_id not in completed:
                    scenarios.append((model, sizing, contingency, scenario_id))
    
    total_scenarios = len(scenarios)
    print(f"🎯 Total de cenários a executar: {total_scenarios}\n")
    
    if total_scenarios == 0:
        print("✅ Todos os cenários já foram executados!")
        return
    
    # Prepara arquivo CSV de resultados
    fieldnames = ["timestamp", "model", "sizing", "contingency", "price", "hours", "acts", "tokens", "status", "error"]
    
    with open(RESULTS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        # Executa cada cenário
        for idx, (model, sizing, contingency, scenario_id) in enumerate(scenarios, 1):
            print(f"\n[{idx}/{total_scenarios}] Processando: {scenario_id}")
            
            # Executa
            output_path, error = run_scenario(model, sizing, contingency)
            
            if error:
                # Falha: registra erro
                write_result(writer, model, sizing, contingency, {}, error=error)
            else:
                # Sucesso: extrai métricas
                metrics = extract_metrics(output_path)
                write_result(writer, model, sizing, contingency, metrics)
                
                print(f"   💰 Preço: {metrics['price']}")
                print(f"   ⏱️  Horas: {metrics['hours']}h")
                print(f"   📋 Atividades: {metrics['acts']}")
                print(f"   🎯 Tokens: {metrics['tokens']:,}")
            
            # Salva progresso
            save_progress(scenario_id)
            
            # Flush do CSV para garantir que dados não sejam perdidos
            f.flush()
            
            # Pequena pausa entre execuções para evitar sobrecarga
            if idx < total_scenarios:
                time.sleep(2)
    
    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║                    BENCHMARK CONCLUÍDO                           ║
╚══════════════════════════════════════════════════════════════════╝

📊 Resultados salvos em: {RESULTS_FILE}
🧹 Para limpar o progresso e recomeçar: rm {PROGRESS_FILE}

""")

if __name__ == "__main__":
    main()
