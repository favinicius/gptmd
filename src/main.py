import argparse
import os
import json
from pathlib import Path
from datetime import datetime
from src.ai_agent import AIAgent
from src.context_loader import ContextLoader
from src.database import Database
from src.models import ProposalData, TopicMapping, format_br_currency, SizingMode, ContingencyLevel
from src.engines import LaborEngine, LogisticsEngine, MaterialEngine, ProposalAssembler, ResearchEngine, LibraryAssembler

def apply_margins(proposal: ProposalData):
    """
    Aplica as margens de venda (Regra de Negócio).
    """
    # Hardware (* 2)
    for hw in proposal.hardware_table:
        hw.unit_price = hw.unit_price * 2
        hw.total_price = hw.unit_price * hw.qty
    proposal.total_hardware = sum(h.total_price for h in proposal.hardware_table)
    
    # Labor (* 3)
    for lab in proposal.labor_table:
        lab.total_price = lab.total_price * 3.0
    proposal.total_labor = sum(l.total_price for l in proposal.labor_table)
    
    # Services (* 1.6)
    for serv in proposal.service_table:
        serv.unit_price = serv.unit_price * 1.6
        serv.total_price = serv.qty * serv.unit_price
    proposal.total_services = sum(s.total_price for s in proposal.service_table)
    
    # Expenses (* 1.2)
    for exp in proposal.expense_table:
        exp.unit_price = exp.unit_price * 1.2
        exp.total_price = exp.qty * exp.unit_price
    proposal.total_expenses = sum(e.total_price for e in proposal.expense_table)
    
    proposal.grand_total = (
        proposal.total_hardware +
        proposal.total_labor +
        proposal.total_services +
        proposal.total_expenses
    )

def clean_value(val):
    if isinstance(val, (int, float)) and val == int(val):
        return int(val)
    return val

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
                f.write("| Item | Tópico | Execs | Qtde | Horas_Dia | Dias | Total_H | Tipo | Atividade | Profissional | Custo_Unit | Total_R$ | Source_Ref |\n")
                f.write("| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :--- | :---: | :---: | :---: |\n")
                for item in items:
                    f.write(f"| {item.item_id} | {item.topic} | {clean_value(item.executions)} | {clean_value(item.qty_professionals)} | {clean_value(item.daily_hours)} | {clean_value(item.days)} | {clean_value(item.hours)} | {item.activity_type} | {item.activity} | {item.role} | {format_br_currency(item.hourly_rate)} | {format_br_currency(item.total_price)} | {item.source_ref} |\n")
            elif hasattr(items[0], 'description'): # Hardware, Service, Expense
                if hasattr(items[0], 'topic'):
                        f.write("| Tópico | Descrição | Qtd | Unitário (R$) | Total (R$) |\n")
                        f.write("| :--- | :--- | :---: | :---: | :---: |\n")
                        for item in items:
                        # Fix for NoneType is_misc if relevant, but models should have defaults
                        # Using hasattr check just in case
                            f.write(f"| {item.topic} | {item.description} | {clean_value(item.qty)} | {format_br_currency(item.unit_price)} | {format_br_currency(item.total_price)} |\n")
                else:
                    f.write("| Descrição | Qtd | Unitário (R$) | Total (R$) |\n")
                    f.write("| :--- | :---: | :---: | :---: |\n")
                    for item in items:
                        f.write(f"| {item.description} | {clean_value(item.qty)} | {format_br_currency(item.unit_price)} | {format_br_currency(item.total_price)} |\n")
    return path

def main():
    parser = argparse.ArgumentParser(description="GPT-Md: Technical Proposal Generator - Phase 3 (Engines)")
    parser.add_argument("--tech_ref", type=str, help="Path to technical PDF/docs", default="input/docs")
    parser.add_argument("--template_dir", type=str, help="Path to Markdown templates", default="templates/")
    parser.add_argument("--instruction", type=str, help="Instruction text or path to .txt", default="input/instruction.txt")
    parser.add_argument("--split", action="store_true", help="Force split of technical and commercial proposals (and generate all 3 versions in dev mode)")
    parser.add_argument("--sizing", type=str, choices=["aggressive", "standard", "secure"], help="Override sizing mode (0.85x, 1.0x, 1.25x)")
    parser.add_argument("--contingency", type=str, choices=["none", "low", "standard", "high"], help="Override contingency level (SHE/Buffer)")
    parser.add_argument("--help-metrics", action="store_true", help="Show detailed metrics table and exit")
    parser.add_argument("--debug", action="store_true", help="Enable verbose debug and save raw AI responses")
    parser.add_argument("--use-docs", action="store_true", help="Load and use technical documents from --tech_ref")
    parser.add_argument("--legacy-assembler", action="store_true", help="Use old non-Jinja assembler")
    
    args = parser.parse_args()

    if args.help_metrics:
        print("\n=== GPT-Md Sizing & Contingency Metrics (v6.0) ===")
        print("\n1. SIZING MODES (Estimativa de Horas):")
        print("| Mode      | Multiplicador de Esforço | Perfil Indicado |")
        print("| :---      | :---:                    | :---            |")
        print("| aggressive| 0.85x                    | Propostas competitivas, enxutas (Risco Médio) |")
        print("| standard  | 1.00x                    | Padrão equilibrado (Risco Baixo - Recomendado) |")
        print("| secure    | 1.25x                    | Cenários conservadores, alta incerteza, premium |")
        
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
        print(f"[*] Carregando documentos técnicos de {args.tech_ref}...")
        loader = ContextLoader(docs_path=args.tech_ref)
        docs_content = loader.load_technical_docs()
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
    
    # Seleção de Assembler (v9.0: Suporte Híbrido + Library)
    if args.legacy_assembler:
        print("[*] Usando Assembler V1 (Legado/Estático)")
        proposal_assembler = ProposalAssembler(agent)
    elif args.template_dir == "templates/library":
        print("[*] Usando LibraryAssembler (V3 - Alta Fidelidade)")
        proposal_assembler = LibraryAssembler(library_dir=args.template_dir)
    else:
        print("[*] Usando Assembler V2 (Jinja2/Fidelidade)")
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
    
    # Apply Margins
    apply_margins(proposal)
    
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
    
    if isinstance(proposal_assembler, LibraryAssembler):
        proposal_outputs = proposal_assembler.assemble(proposal, public_intent)
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
