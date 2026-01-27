import argparse
import os
import json
import csv
import time
from pathlib import Path
from datetime import datetime
from src.ai_agent import AIAgent
from src.context_loader import ContextLoader
from src.database import Database
from src.models import ProposalData, TopicMapping, format_br_currency, format_br_number, SizingMode, ContingencyLevel, Intent
from src.engines import LaborEngine, LogisticsEngine, MaterialEngine, ProposalAssembler, ResearchEngine, LibraryAssembler
from src.engines.pricing_engine import PricingEngine
from src.engines.opex_engine import OpexEngine
from src.config.commerce_config import PRAZO_PADRAO_DIAS

def apply_margins(proposal: ProposalData, term_days: int = PRAZO_PADRAO_DIAS):
    """
    Aplica as margens de venda (Regra de Negócio).
    """
    # 1. Hardware - O valor de venda já é calculado pelo PricingEngine para manter consistência com o prazo
    # proposal.total_hardware_venda será setado em calculate_proposal_selling_prices
    pass
    
    # 2. Labor (MOD) - Nova lógica mandatória baseada no PricingEngine
    # O total_labor mantem o CUSTO para a tabela MOD.md
    total_labor_cost = sum(lab.hours * lab.hourly_rate for lab in proposal.labor_table)
    proposal.total_labor = total_labor_cost 
    proposal.payment_term = term_days
    
    # O valor de venda será calculado centralizadamente abaixo
    # proposal.total_labor_venda será setado em calculate_proposal_selling_prices
    
    # 3. Services (Sem margem fixa - Custo Puro)
    for serv in proposal.service_table:
        serv.total_price = serv.qty * serv.unit_price
    proposal.total_services = sum(s.total_price for s in proposal.service_table)
    
    # 4. Expenses (Sem margem fixa - Custo Puro)
    for exp in proposal.expense_table:
        exp.total_price = exp.qty * exp.unit_price
    proposal.total_expenses = sum(e.total_price for e in proposal.expense_table)

    # 5. Cálculo dos Valores de Venda (MOD, SET, DIV)
    PricingEngine.calculate_proposal_selling_prices(proposal, term_days)
    
    # Sincroniza grand_total (usado em alguns templates) com grand_total_venda
    proposal.grand_total = proposal.grand_total_venda

def format_clean_br(val):
    """Retorna o valor formatado no padrão BR: 1.234,56 ou 1.234 (se inteiro)"""
    if not isinstance(val, (int, float)):
        return val
    if val == int(val):
        return format_br_number(val, 0)
    return format_br_number(val, 2)

def save_md(output_dir, filename, title, items):
    path = output_dir / filename
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        if not items:
            f.write("Nenhum item calculado.\n")
        else:
            # Basic MD Table Generation
            if hasattr(items[0], 'topic_id'): # Topics Mapping
                f.write("| Topic_ID | Descrição |\n")
                f.write("| :--- | :--- |\n")
                for item in items:
                    f.write(f"| {item.topic_id} | {item.description} |\n")
            elif hasattr(items[0], 'role'): # Labor
                f.write("| Item | Tópico | Execs | Qtde | Horas_Dia | Dias | Total_H | Sizing | Tipo | Atividade | Detalhes Técnicos / Checklist | Profissional | Custo_Unit | Total_R$ | Source_Ref |\n")
                f.write("| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :--- | :--- | :---: | :---: | :---: |\n")
                for item in items:
                    detail = item.technical_detail.replace("\n", " ").replace("|", "-") if item.technical_detail else "-"
                    f.write(f"| {item.item_id} | {item.topic} | {format_clean_br(item.executions)} | {format_clean_br(item.qty_professionals)} | {format_clean_br(item.daily_hours)} | {format_clean_br(item.days)} | {format_clean_br(item.hours)} | {format_clean_br(item.sizing_factor)}x | {item.activity_type} | {item.activity} | {detail} | {item.role} | {format_br_currency(item.hourly_rate)} | {format_br_currency(item.total_price)} | {item.source_ref} |\n")
            elif hasattr(items[0], 'description'): # Hardware, Service, Expense
                if hasattr(items[0], 'topic'):
                        f.write("| Tópico | Descrição | Qtd | Unitário (R$) | Total (R$) |\n")
                        f.write("| :--- | :--- | :---: | :---: | :---: |\n")
                        for item in items:
                        # Fix for NoneType is_misc if relevant, but models should have defaults
                        # Using hasattr check just in case
                            f.write(f"| {item.topic} | {item.description} | {format_clean_br(item.qty)} | {format_br_currency(item.unit_price)} | {format_br_currency(item.total_price)} |\n")
                else:
                    f.write("| Descrição | Qtd | Unitário (R$) | Total (R$) |\n")
                    f.write("| :--- | :---: | :---: | :---: |\n")
                    for item in items:
                        f.write(f"| {item.description} | {format_clean_br(item.qty)} | {format_br_currency(item.unit_price)} | {format_br_currency(item.total_price)} |\n")
    return path

def save_csv(output_dir: Path, filename: str, items: list):
    """
    Saves a list of Pydantic models to a CSV file.
    Uses ';' as delimiter for Brazilian Excel compatibility and utf-8-sig.
    Numbers are formatted with Brazilian decimal separator (comma).
    """
    if not items:
        return None
    
    path = output_dir / filename
    
    # Extract fieldnames from the first item
    if hasattr(items[0], 'model_dump'):
        fieldnames = list(items[0].model_dump().keys())
    else:
        return None

    with open(path, "w", encoding="utf-8-sig", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for item in items:
            data = item.model_dump()
            # Format numeric fields to Brazilian style
            formatted_data = {}
            for k, v in data.items():
                if isinstance(v, (float, int)) and not isinstance(v, bool):
                    if isinstance(v, float):
                        # Use comma for decimal, no thousands separator for cleaner Excel ingestion
                        formatted_data[k] = f"{v:.2f}".replace('.', ',')
                    else:
                        formatted_data[k] = str(v)
                else:
                    formatted_data[k] = v
            writer.writerow(formatted_data)
            
    return path


def run_quality_check(output_dir: Path, intent: Intent):
    """
    Verifica se os arquivos essenciais foram gerados e se o conteúdo parece coerente.
    """
    required_sections = ["# 1. RESUMO EXECUTIVO", "## 17. INVESTIMENTOS", "Total Geral"]
    target_files = list(output_dir.glob("PROPOSTA_*.md"))
    
    if not target_files:
        print("❌ QA FALHOU: Nenhum arquivo de proposta encontrado.")
        return

    print(f"  - Analisando {len(target_files)} arquivos gerados...")
    
    issues_found = 0
    for file_path in target_files:
        try:
            content = file_path.read_text(encoding="utf-8")
            
            # Check 1: Nome do Cliente
            if intent.client_name not in content:
                 # Check flexível
                 pass 
            
            # Check 2: Nome do Provedor (EGE)
            if "EGE Soluções" not in content and "EGE" not in content:
                print(f"    ⚠️ {file_path.name}: Nome do provedor 'EGE' não encontrado no texto.")
                issues_found += 1
                
            # Check 3: Seções Críticas
            if "COMERCIAL" in file_path.name or "UNIFICADA" in file_path.name:
                 if "## 17. INVESTIMENTOS" not in content and "17.1" not in content:
                     print(f"    ❌ {file_path.name}: Tabela de preços ausente.")
                     issues_found += 1

            # Check 4: Auto-referência
            if "submeter à **EGE" in content or "submeter à EGE" in content:
                print(f"    ❌ {file_path.name}: ERRO CRÍTICO - Proposta auto-referenciada (EGE -> EGE).")
                issues_found += 1

        except Exception as e:
            print(f"    ⚠️ Erro ao ler {file_path.name}: {e}")

    if issues_found == 0:
        print("  ✅ QA APROVADO: Arquivos íntegros e coerentes.")
    else:
        print(f"  ⚠️ QA ALERTA: {issues_found} problemas potenciais detectados. Revise os arquivos.")

def run_generator(params: dict):
    """
    Versão programática do gerador para uso via API ou Scripts.
    params deve conter as chaves equivalentes aos argumentos do CLI.
    """
    start_time = time.time()
    
    # Overrides / Defaults
    template_dir = params.get("template_dir", "templates/")
    instruction = params.get("instruction", "input/instruction.txt")
    split = params.get("split", False)
    sizing = params.get("sizing")
    contingency = params.get("contingency")
    debug = params.get("debug", False)
    use_docs = params.get("use_docs", [])
    legacy_assembler = params.get("legacy_assembler", False)
    term = params.get("term", PRAZO_PADRAO_DIAS)
    model = params.get("model")
    output_mode = params.get("output_mode", "unified")
    separate_opex = params.get("separate_opex", False)

    # --- Output Dir Initialization ---
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = Path("output") / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # --- Initialization ---
    print("Loading contexts...")
    docs_content = ""
    if use_docs:
        for doc_path in use_docs:
            print(f"[*] Carregando documento técnico: {doc_path}...")
            loader = ContextLoader(docs_path=doc_path)
            docs_content += loader.load_technical_docs()
    
    db = Database()
    agent = AIAgent(model_name=model)
    
    research_engine = ResearchEngine(db, agent)
    labor_engine = LaborEngine(db, research_engine)
    logistics_engine = LogisticsEngine(db)
    material_engine = MaterialEngine(db)
    
    library_path = Path("templates/library")
    if legacy_assembler:
        proposal_assembler = ProposalAssembler(agent)
    elif library_path.exists() and not template_dir.endswith("v2"):
        proposal_assembler = LibraryAssembler(library_dir=str(library_path))
    else:
        from src.engines import ProposalAssemblerV2
        proposal_assembler = ProposalAssemblerV2(template_dir=str(Path(template_dir) / "v2"))

    # --- 1. Instruction Processing ---
    instruction_text = ""
    try:
        if len(instruction) < 255:
            instruction_path = Path(instruction)
            if instruction_path.exists() and instruction_path.is_file():
                with open(instruction_path, "r", encoding="utf-8") as f:
                    instruction_text = f.read()
            else:
                instruction_text = instruction
        else:
            instruction_text = instruction
    except OSError:
        instruction_text = instruction

    print("Stage 1: AI Analysis (Ingestion)...")
    try:
        intent = agent.interpret_instruction(instruction_text, docs_content)
    except Exception as e:
        if debug and hasattr(agent, 'last_raw_interpretation'):
             with open(output_dir / "raw_ai_interpretation.txt", "w", encoding="utf-8") as f:
                f.write("=== INTERPRETATION (ERROR) ===\n")
                f.write(agent.last_raw_interpretation)
        raise e

    intent.company_name = "EGE Soluções Industriais"
    intent.company_short_name = "EGE"
    
    if sizing:
        intent.sizing_mode = SizingMode(sizing)
    if contingency:
        intent.contingency_level = ContingencyLevel(contingency)
    if split:
        intent.split_proposal = True

    # --- 1.5 Logistics Planning ---
    origin = "Jundiaí - SP"
    destination = "Local do Cliente"
    duration_days = (intent.estimated_duration_weeks or 4) * 5
    
    log_plan = agent.plan_logistics(
        origin=origin,
        destination=destination,
        instruction_text=instruction_text,
        team_size=max(1, intent.logistics_override.team_size) if intent.logistics_override else 1,
        duration_days=duration_days
    )
    intent.detailed_logistics = log_plan

    # --- 2. Calculation (Engines) ---
    print("Stage 2: Pricing Engines (Calculation)...")
    proposal = ProposalData()
    for i, scope_item in enumerate(intent.scope_items):
        proposal.topics.append(TopicMapping(
            topic_id=f"T-{i+1:02d}",
            description=f"{scope_item.name} ({scope_item.detected_quantity} un - {scope_item.action_type})"
        ))

    requires_certification = any("fibra" in i.name.lower() or "cabeamento" in i.name.lower() for i in intent.scope_items)
    
    material_engine.calculate_materials(intent, proposal)
    material_engine.calculate_services(proposal, intent, requires_certification)
    labor_engine.calculate_labor(intent, proposal, requires_certification)
    logistics_engine.calculate_logistics(intent, proposal)
    proposal.opex_data = OpexEngine.calculate_opex(proposal, intent.scope_items)
    
    apply_margins(proposal, term_days=term)
    
    # --- 3. Output Generation ---
    if debug:
        if hasattr(agent, 'last_raw_interpretation'):
            with open(output_dir / "raw_ai_interpretation.txt", "w", encoding="utf-8") as f:
                f.write("=== INTERPRETATION ===\n")
                f.write(agent.last_raw_interpretation)

    print("Stage 3: AI Technical Redaction...")
    tech_summary_for_ai = "\n".join([f"- {t.description}" for t in proposal.topics])
    proposal_summary_for_ai = f"Total Horas: {sum(i.hours for i in proposal.labor_table)}h | Total CAPEX: {format_br_currency(proposal.grand_total_venda)}"
    
    redaction = agent.compose_technical_redaction(
        intent_summary=intent.project_motivation,
        tech_scope=tech_summary_for_ai,
        proposal_summary=proposal_summary_for_ai
    )

    extra_context = {
        "custom_objective_md": redaction.get("custom_objective_md"),
        "custom_benefits_md": redaction.get("custom_benefits_md"),
        "custom_vision_md": redaction.get("custom_vision_md"),
        "custom_testing_protocol": redaction.get("testing_protocol_md"),
        "custom_team_structure": redaction.get("team_structure_md"),
        "custom_timeline": redaction.get("timeline_md"),
        "custom_training_md": redaction.get("custom_training_md"),
        "asset_table_md": redaction.get("asset_table_md"),
        "custom_cabling_md": redaction.get("cabling_context_md"),
        "custom_software_md": redaction.get("software_licensing_md"),
        "custom_deliverables_md": redaction.get("deliverables_list_md")
    }
    extra_context = {k: v for k, v in extra_context.items() if v}

    processing_duration = time.time() - start_time
    public_intent = intent.model_copy(deep=True)
    public_intent.scope_items = [item for item in intent.scope_items if item.visibility == "public"]

    if isinstance(proposal_assembler, LibraryAssembler):
        proposal_outputs = proposal_assembler.assemble(
            proposal, public_intent, processing_time=processing_duration,
            extra_context=extra_context, output_mode=output_mode, separate_opex=separate_opex
        )
    else:
        proposal_outputs = proposal_assembler.assemble(proposal, public_intent, output_path=str(output_dir))
    
    generated_files = []
    for filename, content in proposal_outputs.items():
        content = sanitize_content(content, intent.client_name)
        final_filename = filename.replace(".md", f"_{timestamp}.md")
        final_path = output_dir / final_filename
        final_path.write_text(content, encoding="utf-8")
        generated_files.append(str(final_path))

    # Save auxiliary files
    save_md(output_dir, f"MAT_{timestamp}.md", "Tabela de Materiais", proposal.hardware_table)
    save_md(output_dir, f"MOD_{timestamp}.md", "Tabela de Mão de Obra", proposal.labor_table)
    save_csv(output_dir, f"MAT_{timestamp}.csv", proposal.hardware_table)
    save_csv(output_dir, f"MOD_{timestamp}.csv", proposal.labor_table)
    
    with open(output_dir / "LOGISTICS_AUDIT.md", "w", encoding="utf-8") as f:
        f.write(logistics_engine.get_audit_report())

    print(f"✅ Success! Output: {output_dir}")
    return {
        "status": "success",
        "output_dir": str(output_dir),
        "files": generated_files,
        "proposal_data": proposal.model_dump()
    }

def main():
    parser = argparse.ArgumentParser(description="GPT-Md CLI")
    parser.add_argument("--template_dir", type=str, default="templates/")
    parser.add_argument("--instruction", type=str, default="input/instruction.txt")
    parser.add_argument("--split", action="store_true")
    parser.add_argument("--sizing", type=str, choices=["aggressive", "standard", "secure", "critical"])
    parser.add_argument("--contingency", type=str, choices=["none", "low", "standard", "high"])
    parser.add_argument("--help-metrics", action="store_true")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--use-docs", nargs="+", metavar="FILE")
    parser.add_argument("--legacy-assembler", action="store_true")
    parser.add_argument("--term", type=int, default=PRAZO_PADRAO_DIAS)
    parser.add_argument("--model", type=str)
    parser.add_argument("--output-mode", type=str, choices=["unified", "full", "splited"], default="unified")
    parser.add_argument("--separate-opex", action="store_true")
    
    args = parser.parse_args()

    if args.help_metrics:
        # (mantem o print original se quiser ou simplifica)
        print("Sizing & Contingency Metrics Help...")
        exit(0)

    # Converte args para dict e chama run_generator
    params = vars(args)
    run_generator(params)

if __name__ == "__main__":
    main()

