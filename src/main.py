import argparse
import os
import json
from pathlib import Path
from datetime import datetime
from src.ai_agent import AIAgent
from src.context_loader import ContextLoader
from src.database import Database
from src.models import ProposalData, TopicMapping
from src.engines import LaborEngine, LogisticsEngine, MaterialEngine, ProposalAssembler

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
                f.write("| Item | Tópico | Qtde | Horas_Dia | Dias | Total_H | Tipo | Atividade | Profissional | Custo_Unit | Total_R$ | Source_Ref |\n")
                f.write("| :---: | :--- | :---: | :---: | :---: | :---: | :--- | :--- | :--- | :---: | :---: | :---: |\n")
                for item in items:
                    f.write(f"| {item.item_id} | {item.topic} | {item.qty_professionals} | {item.daily_hours} | {item.days} | {item.hours} | {item.activity_type} | {item.activity} | {item.role} | {item.hourly_rate:,.2f} | {item.total_price:,.2f} | {item.source_ref} |\n")
            elif hasattr(items[0], 'description'): # Hardware, Service, Expense
                if hasattr(items[0], 'topic'):
                        f.write("| Tópico | Descrição | Qtd | Unitário (R$) | Total (R$) |\n")
                        f.write("| :--- | :--- | :---: | :---: | :---: |\n")
                        for item in items:
                        # Fix for NoneType is_misc if relevant, but models should have defaults
                        # Using hasattr check just in case
                            f.write(f"| {item.topic} | {item.description} | {item.qty} | {item.unit_price:,.2f} | {item.total_price:,.2f} |\n")
                else:
                    f.write("| Descrição | Qtd | Unitário (R$) | Total (R$) |\n")
                    f.write("| :--- | :---: | :---: | :---: |\n")
                    for item in items:
                        f.write(f"| {item.description} | {item.qty} | {item.unit_price:,.2f} | {item.total_price:,.2f} |\n")
    return path

def main():
    parser = argparse.ArgumentParser(description="GPT-Md: Technical Proposal Generator - Phase 3 (Engines)")
    parser.add_argument("--tech_ref", type=str, help="Path to technical PDF/docs", default="input/docs")
    parser.add_argument("--style_ref", type=str, help="Path to style PDF/example", default="input/style")
    parser.add_argument("--instruction", type=str, help="Instruction text or path to .txt", default="input/instruction.txt")
    
    args = parser.parse_args()
    
    # --- Initialization ---
    print("Loading contexts...")
    loader = ContextLoader(docs_path=args.tech_ref, style_path=args.style_ref)
    docs_content = loader.load_technical_docs()
    style_content = loader.load_style_guide()
    
    db = Database()
    agent = AIAgent()
    
    # Engines
    labor_engine = LaborEngine(db)
    logistics_engine = LogisticsEngine(db)
    material_engine = MaterialEngine(db)
    proposal_assembler = ProposalAssembler(agent)

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
    intent = agent.interpret_instruction(instruction_text, docs_content)
    print(f"Dados extraídos: {intent.client_name} / {intent.project_name}")
    
    # --- 1.5 Logistics Planning ---
    origin = "Jundiaí - SP" # Fixed Origin as per requirements
    destination = "Local do Cliente" # Or extract?
    
    duration_days = intent.estimated_duration_weeks * 5 # Approx
    
    log_plan = agent.plan_logistics(
        origin=origin,
        destination=destination,
        instruction_text=instruction_text,
        team_size=max(1, intent.logistics_override.team_size),
        duration_days=duration_days
    )
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
    material_engine.calculate_services(proposal, requires_certification) # If handling services there
    labor_engine.calculate_labor(intent, proposal, requires_certification)
    logistics_engine.calculate_logistics(intent, proposal)
    
    # Apply Margins
    apply_margins(proposal)
    
    print(f"Calculated Total: R$ {proposal.grand_total:,.2f}")

    # --- 3. Output Generation ---
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") # Timestamp as requested
    output_dir = Path("output") / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Debug JSON
    with open(output_dir / "debug_intent.json", "w", encoding="utf-8") as f:
        json.dump(intent.model_dump(), f, indent=4, ensure_ascii=False)

    print("Stage 3: Proposal Assembly (Markdown)...")
    markdown_output = proposal_assembler.assemble_proposal(proposal, intent, style_context=style_content)
    
    # Add Footer
    footer = f"\n\n---\n*Gerado automaticamente pelo GPT-Md v2.0 (Engines) via {agent.model_name} em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*"
    markdown_output += footer
    
    # Save Artifacts
    save_md(output_dir, f"MAT_{timestamp}.md", "Tabela de Materiais", proposal.hardware_table)
    save_md(output_dir, f"MOD_{timestamp}.md", "Tabela de Mão de Obra", proposal.labor_table)
    save_md(output_dir, f"SET_{timestamp}.md", "Serviços Externos", proposal.service_table)
    save_md(output_dir, f"DIV_{timestamp}.md", "Despesas de Viagem", proposal.expense_table)
    save_md(output_dir, f"TOPICS_{timestamp}.md", "Índice de Tópicos", proposal.topics)

    final_output_path = output_dir / f"PROPOSTA_COMPLETA_{timestamp}.md"
    with open(final_output_path, "w", encoding="utf-8") as f:
        f.write(markdown_output)

    print(f"Success! Output artifacts saved to: {output_dir}")

if __name__ == "__main__":
    main()
