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
from src.models import ProposalData, TopicMapping, format_br_currency, format_br_number, SizingMode, ContingencyLevel
from src.engines import LaborEngine, LogisticsEngine, MaterialEngine, ProposalAssembler, ResearchEngine, LibraryAssembler
from src.engines.pricing_engine import PricingEngine
from src.engines.opex_engine import OpexEngine
from src.config.commerce_config import PRAZO_PADRAO_DIAS

def apply_margins(proposal: ProposalData, term_days: int = PRAZO_PADRAO_DIAS):
    """
    Aplica as margens de venda (Regra de Negócio).
    """
    # 1. Hardware (* 2) - Manter regra atual enquanto não houver PricingEngine para MAT
    for hw in proposal.hardware_table:
        hw.unit_price = hw.unit_price * 2
        hw.total_price = hw.unit_price * hw.qty
    proposal.total_hardware = sum(h.total_price for h in proposal.hardware_table)
    
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
                f.write("| Item | Tópico | Execs | Qtde | Horas_Dia | Dias | Total_H | Tipo | Atividade | Detalhes Técnicos / Checklist | Profissional | Custo_Unit | Total_R$ | Source_Ref |\n")
                f.write("| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :--- | :--- | :---: | :---: | :---: |\n")
                for item in items:
                    detail = item.technical_detail.replace("\n", " ").replace("|", "-") if item.technical_detail else "-"
                    f.write(f"| {item.item_id} | {item.topic} | {format_clean_br(item.executions)} | {format_clean_br(item.qty_professionals)} | {format_clean_br(item.daily_hours)} | {format_clean_br(item.days)} | {format_clean_br(item.hours)} | {item.activity_type} | {item.activity} | {detail} | {item.role} | {format_br_currency(item.hourly_rate)} | {format_br_currency(item.total_price)} | {item.source_ref} |\n")
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

def main():
    start_time = time.time()
    print("DEBUG: Entrou no main()")
    parser = argparse.ArgumentParser(description="GPT-Md: Technical Proposal Generator - Phase 3 (Engines)")
    # Remove redundant --tech_ref and make --use-docs take files
    parser.add_argument("--template_dir", type=str, help="Path to Markdown templates", default="templates/")
    parser.add_argument("--instruction", type=str, help="Instruction text or path to .txt", default="input/instruction.txt")
    parser.add_argument("--split", action="store_true", help="Force split of technical and commercial proposals (and generate all 3 versions in dev mode)")
    parser.add_argument("--sizing", type=str, choices=["aggressive", "standard", "secure", "critical"], help="Override sizing mode (0.85x, 1.0x, 1.4x, 1.6x)")
    parser.add_argument("--contingency", type=str, choices=["none", "low", "standard", "high"], help="Override contingency level (SHE/Buffer)")
    parser.add_argument("--help-metrics", action="store_true", help="Show detailed metrics table and exit")
    parser.add_argument("--debug", action="store_true", help="Enable verbose debug and save raw AI responses")
    parser.add_argument("--use-docs", nargs="+", help="Explicit technical documents (PDF/TXT/MD) to load for context", metavar="FILE")
    parser.add_argument("--legacy-assembler", action="store_true", help="Use old non-Jinja assembler")
    parser.add_argument("--term", type=int, default=PRAZO_PADRAO_DIAS, help="Payment term in days (default: 30)")
    
    args = parser.parse_args()

    if args.help_metrics:
        print("\n=== GPT-Md Sizing & Contingency Metrics (v6.0) ===")
        print("\n1. SIZING MODES (Estimativa de Horas):")
        print("| Mode      | Multiplicador de Esforço | Perfil Indicado |")
        print("| :---      | :---:                    | :---            |")
        print("| aggressive| 0.85x                    | Propostas competitivas, enxutas (Risco Médio) |")
        print("| standard  | 1.00x                    | Padrão equilibrado (Risco Baixo - Recomendado) |")
        print("| secure    | 1.40x                    | Cenários conservadores, alta incerteza, premium |")
        print("| critical  | 1.60x                    | Missão Crítica (Governo/Militar/Bancos) |")
        
        print("\n2. CONTINGENCY LEVELS (Ineficiência/SHE):")
        print("| Level     | Ineficiência (SHE)      | Buffer Extra |")
        print("| :---      | :---                    | :---         |")
        print("| none      | 0.0h / dia (Removido)   | 0%           |")
        print("| low       | 1.0h / dia físico       | 0%           |")
        print("| standard  | 1.5h / dia físico       | 0%           |")
        print("| high      | 2.0h / dia físico       | +10% Tech    |")
        print("\nUse --sizing [mode] ou --contingency [level] para forçar estes valores.\n")
        exit(0)
    
    # --- Output Dir Initialization (Moved for Debugging) ---
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = Path("output") / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # --- Initialization ---
    print("Loading contexts...")
    docs_content = ""
    if args.use_docs:
        for doc_path in args.use_docs:
            print(f"[*] Carregando documento técnico: {doc_path}...")
            loader = ContextLoader(docs_path=doc_path)
            docs_content += loader.load_technical_docs()
    else:
        print("[*] Documentos técnicos ignorados (Modo Instrução Soberana).")
    
    db = Database()
    agent = AIAgent()
    
    # Engines
    research_engine = ResearchEngine(db, agent)
    labor_engine = LaborEngine(db, research_engine)
    logistics_engine = LogisticsEngine(db)
    material_engine = MaterialEngine(db)
    material_engine = MaterialEngine(db)
    
    # Seleção de Assembler (v9.6: Força Bruta Premium)
    library_path = Path("templates/library")
    
    if args.legacy_assembler:
        print("[*] Usando Assembler V1 (Legado/Estático)")
        proposal_assembler = ProposalAssembler(agent)
    elif library_path.exists() and not args.template_dir.endswith("v2"):
        print("[*] Usando LibraryAssembler (V3 - Alta Fidelidade)")
        proposal_assembler = LibraryAssembler(library_dir=str(library_path))
    else:
        print(f"[*] Usando Assembler V2 (Jinja2/Fidelidade) - Path: {args.template_dir}")
        from src.engines import ProposalAssemblerV2
        proposal_assembler = ProposalAssemblerV2(template_dir=str(Path(args.template_dir) / "v2"))





    # --- 1. Instruction Processing ---
    instruction_text = ""
    try:
        if len(args.instruction) < 255:
            instruction_path = Path(args.instruction)
            if instruction_path.exists() and instruction_path.is_file():
                with open(instruction_path, "r", encoding="utf-8") as f:
                    instruction_text = f.read()
            else:
                instruction_text = args.instruction
        else:
            instruction_text = args.instruction
    except OSError:
        instruction_text = args.instruction

    print("Stage 1: AI Analysis (Ingestion)...")
    try:
        intent = agent.interpret_instruction(instruction_text, docs_content)
    except Exception as e:
        if args.debug and hasattr(agent, 'last_raw_interpretation'):
             with open(output_dir / "raw_ai_interpretation.txt", "w", encoding="utf-8") as f:
                f.write("=== INTERPRETATION (ERROR) ===\n")
                f.write(agent.last_raw_interpretation)
        print(f"\nERRO CRÍTICO NO STAGE 1: {e}")
        print(f"Verifique o arquivo 'raw_ai_interpretation.txt' in {output_dir}")
        exit(1)

    print(f"Dados extraídos: {intent.client_name} / {intent.project_name}")

    # Guardrail (Governance v2.0)
    if intent.needs_clarification:
        print("\n" + "="*60)
        print("⛔ PROPOSTA BARRADA POR AMBIGUIDADE (GOVERNANÇA TÉCNICA)")
        print("="*60)
        print("O Agente identificou lacunas críticas no escopo que impedem")
        print("o dimensionamento técnico sem 'alucinações'.")
        print("\nPor favor, responda às seguintes perguntas no seu input:")
        for i, q in enumerate(intent.clarification_questions):
            print(f" {i+1}. {q}")
        print("="*60 + "\n")
        exit(1)
    
    if args.split:
        intent.split_proposal = True
        print("[*] Split forçado via CLI.")

    # Apply Sizing/Contingency Overrides (v6.0)
    if args.sizing:
        intent.sizing_mode = SizingMode(args.sizing)
        print(f"[*] Sizing Mode forçado via CLI: {intent.sizing_mode.value}")
    
    if args.contingency:
        intent.contingency_level = ContingencyLevel(args.contingency)
        print(f"[*] Contingency Level forçado via CLI: {intent.contingency_level.value}")

    print(f"Templates selecionados: {intent.selected_tech_template} / {intent.selected_comm_template} (Split={intent.split_proposal})")

    
    # --- 1.5 Logistics Planning ---
    origin = "Jundiaí - SP" # Fixed Origin as per requirements
    destination = "Local do Cliente" # Or extract?
    
    duration_days = intent.estimated_duration_weeks * 5 # Approx
    
    try:
        log_plan = agent.plan_logistics(
            origin=origin,
            destination=destination,
            instruction_text=instruction_text,
            team_size=max(1, intent.logistics_override.team_size) if intent.logistics_override else 1,
            duration_days=duration_days
        )
    except Exception as e:
        if args.debug and hasattr(agent, 'last_raw_logistics'):
            with open(output_dir / "raw_ai_interpretation.txt", "a", encoding="utf-8") as f:
                f.write("\n\n=== LOGISTICS PLAN (ERROR) ===\n")
                f.write(agent.last_raw_logistics)
        print(f"\nERRO CRÍTICO NA LOGÍSTICA: {e}")
        exit(1)
    intent.detailed_logistics = log_plan
    print(f"Plano Logístico: Flight={log_plan.requires_flight}, Region={log_plan.flight_region}")

    # --- 2. Calculation (Engines) ---
    print("Stage 2: Pricing Engines (Calculation)...")
    proposal = ProposalData()
    
    # Generate Topic Mappings
    for i, scope_item in enumerate(intent.scope_items):
        proposal.topics.append(TopicMapping(
            topic_id=f"T-{i+1:02d}",
            description=f"{scope_item.name} ({scope_item.detected_quantity} un - {scope_item.action_type})"
        ))

    requires_certification = any("fibra" in i.name.lower() or "cabeamento" in i.name.lower() for i in intent.scope_items)
    
    # Run Engines
    material_engine.calculate_materials(intent, proposal)
    material_engine.calculate_services(proposal, intent, requires_certification)
    labor_engine.calculate_labor(intent, proposal, requires_certification)
    logistics_engine.calculate_logistics(intent, proposal)
    
    # Run OPEX Engine (Monthly Recurring Costs) - v10.0
    proposal.opex_data = OpexEngine.calculate_opex(proposal, intent.scope_items)
    
    # Apply Margins
    apply_margins(proposal, term_days=args.term)
    
    print(f"Calculated Total: R$ {format_br_currency(proposal.grand_total)}")
    
    total_hours = sum(l.hours for l in proposal.labor_table)
    print(f"  - {len(proposal.labor_table)} atividades planejadas ({total_hours} horas)")

    # --- 3. Output Generation ---
    # output_dir already created at start
    # --- Debug - Save Raw AI Files (v2.5) ---
    if args.debug:
        print(f"[*] Modo DEBUG ativado. Salvando arquivos brutos em {output_dir}")
        if hasattr(agent, 'last_raw_interpretation'):
            with open(output_dir / "raw_ai_interpretation.txt", "w", encoding="utf-8") as f:
                f.write("=== INTERPRETATION ===\n")
                f.write(agent.last_raw_interpretation)
                if hasattr(agent, 'last_raw_logistics'):
                    f.write("\n\n=== LOGISTICS PLAN ===\n")
                    f.write(agent.last_raw_logistics)
    
    # Debug JSON
    with open(output_dir / "debug_intent.json", "w", encoding="utf-8") as f:
        json.dump(intent.model_dump(), f, indent=4, ensure_ascii=False)

    print("Stage 3: Proposal Assembly (Markdown Fragmentation v5.0)...")
    
    # Blindagem e Privacidade (Reforço): Expurgar itens internos antes da IA de redação ver o intent
    public_intent = intent.model_copy(deep=True)
    public_intent.scope_items = [item for item in intent.scope_items if item.visibility == "public"]
    
    print(f"  - Visibilidade: {len(intent.scope_items)} itens totais -> {len(public_intent.scope_items)} itens públicos.")
    
    processing_duration = time.time() - start_time
    
    # Stage 3: Technical Redaction (Personalization) - v11.0
    print("Stage 3: AI Technical Redaction...")
    tech_summary_for_ai = "\n".join([f"- {t.description}" for t in proposal.topics])
    proposal_summary_for_ai = f"Total Horas: {sum(i.hours for i in proposal.labor_table)}h | Total CAPEX: {format_br_currency(proposal.grand_total_venda)}"
    
    redaction = {}
    try:
        redaction = agent.compose_technical_redaction(
            intent_summary=intent.project_motivation,
            tech_scope=tech_summary_for_ai,
            proposal_summary=proposal_summary_for_ai
        )
        if args.debug:
            with open(output_dir / "raw_ai_proposal.txt", "w", encoding="utf-8") as f:
                f.write("=== TECHNICAL REDACTION ===\n")
                f.write(json.dumps(redaction, indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"⚠️ Erro no Al-Redaction (Personalização): {e}")

    # Assembly Context Augmentation (v12.3 - Deliverables)
    extra_context = {
        "custom_objective_md": redaction.get("custom_objective_md", ""),
        "custom_benefits_md": redaction.get("custom_benefits_md", ""),
        "custom_vision_md": redaction.get("custom_vision_md", ""),
        "custom_testing_protocol": redaction.get("testing_protocol_md", ""),
        "custom_team_structure": redaction.get("team_structure_md", ""),
        "custom_timeline": redaction.get("timeline_md", ""),
        "custom_cabling_md": redaction.get("cabling_context_md", ""),
        "custom_software_md": redaction.get("software_licensing_md", ""),
        "custom_deliverables_md": redaction.get("deliverables_list_md", "")
    }

    if isinstance(proposal_assembler, LibraryAssembler):
        proposal_outputs = proposal_assembler.assemble(
            proposal, 
            public_intent, 
            processing_time=processing_duration,
            extra_context=extra_context
        )
    elif hasattr(proposal_assembler, 'assemble'):
        # V2
        proposal_outputs = proposal_assembler.assemble(proposal, public_intent, output_path=str(output_dir))
    else:
        # V1 (Legacy)
        proposal_outputs = proposal_assembler.assemble_proposal(proposal, public_intent, template_dir=args.template_dir)
    
    for filename, content in proposal_outputs.items():
        # Adicionar timestamp ao nome do arquivo se necessário ou usar o nome fixo
        final_filename = filename.replace(".md", f"_{timestamp}.md")
        final_path = output_dir / final_filename
        with open(final_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  - Proposta gerada: {final_filename}")

    # Save Tables
    save_md(output_dir, f"MAT_{timestamp}.md", "Tabela de Materiais", proposal.hardware_table)
    save_md(output_dir, f"MOD_{timestamp}.md", "Tabela de Mão de Obra", proposal.labor_table)
    save_md(output_dir, f"SET_{timestamp}.md", "Serviços Externos", proposal.service_table)
    save_md(output_dir, f"DIV_{timestamp}.md", "Despesas de Viagem", proposal.expense_table)
    save_md(output_dir, f"TOPICS_{timestamp}.md", "Índice de Tópicos", proposal.topics)

    # Save CSVs for Excel Import (v11.0)
    save_csv(output_dir, f"MAT_{timestamp}.csv", proposal.hardware_table)
    save_csv(output_dir, f"MOD_{timestamp}.csv", proposal.labor_table)
    save_csv(output_dir, f"SET_{timestamp}.csv", proposal.service_table)
    save_csv(output_dir, f"DIV_{timestamp}.csv", proposal.expense_table)


    # Save Logistics Audit (v2.5)
    with open(output_dir / "LOGISTICS_AUDIT.md", "w", encoding="utf-8") as f:
        f.write(logistics_engine.get_audit_report())

    # Save raw proposal after assembly (last segment generated)
    if args.debug and hasattr(agent, 'last_raw_content'):
        with open(output_dir / "raw_ai_proposal.txt", "w", encoding="utf-8") as f:
            f.write(agent.last_raw_content)


    # API Usage Report (v2.6.1)
    usage_report = agent.get_usage_stats()
    with open(output_dir / "API_USAGE_STATS.md", "w", encoding="utf-8") as f:
        f.write(usage_report)
    
    if args.debug:
        print("\n" + usage_report)

    print(f"\nSuccess! Output artifacts saved to: {output_dir}")

if __name__ == "__main__":
    main()
