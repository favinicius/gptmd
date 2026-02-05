import os
import re
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from src.models import ProposalData, Intent, format_br_currency, format_br_number

class LibraryAssembler:
    """
    Assembler that builds high-fidelity proposals using the library blocks.
    """
    def __init__(self, library_dir="templates/library"):
        self.library_dir = Path(library_dir)
        self.default_source = "Proposta_EGE"
        # Setup Jinja Environment
        self.env = Environment(
            autoescape=select_autoescape(['html', 'xml'])
        )
        self.env.filters["brl"] = format_br_currency
        self.env.filters["br_num"] = format_br_number


    def _get_block_content(self, section_name: str, source_name: str = None) -> str:
        """Finds and reads the content of a block in the library."""
        if source_name is None:
            source_name = self.default_source
            
        section_path = self.library_dir / section_name
        if not section_path.exists():
            return f"\n<!-- SECTION {section_name} NOT FOUND -->\n"
            
        file_path = section_path / f"{source_name}.md"
        if not file_path.exists():
            # Fallback to any md if specific source not found, or Marata if it exists
            any_md = list(section_path.glob("*.md"))
            if any_md:
                file_path = any_md[0]
            else:
                return f"\n<!-- BLOCK {source_name} IN {section_name} NOT FOUND -->\n"
                
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Clean up redundant code block wrappers
            content = re.sub(r'^jinja\s*\n', '', content)
            content = re.sub(r'^markdown\s*\n', '', content)
            return content.strip()

    def assemble(self, proposal: ProposalData, intent: Intent, processing_time: float = 0.0, extra_context: dict = None, output_mode: str = "unified", separate_opex: bool = False) -> dict:
        """
        Assembles the proposal(s) based on intent.
        Returns a dict of {filename: content}.
        """
        outputs = {}
        
        # 1. Base Logic
        include_network = True
        if "sem rede" in intent.project_name.lower() or intent.selected_tech_template == "iodc_no_net.md":
            include_network = False

        # 2. Sequence Definition (New Lean Architecture)
        sequence = [
            "01-capa",           # Cover
            "02-carta",          # Intro Letter
            "03-institucional",   # Resumo, Aviso, Confidencial
            "04-historico",      # Históricos e Revisões
        ]

        # 2. Product-Centric Configuration (New Architecture)
        product_config = {
            "iodc_full_structured.md": {"block": "Proposta_COMPLETA", "name": "Infraestrutura Industrial (IODC Full)"},
            "iodc_no_net.md": {"block": "Proposta_IODC", "name": "Modernização de Datacenter Industrial (IODC)"},
            "struct_network_industrial.md": {"block": "Proposta_REDE_OT", "name": "Rede Industrial e Conectividade OT"},
            "struct_server_migration.md": {"block": "Proposta_MIGRACAO", "name": "Consolidação e Migração de Servidores"},
            "struct_services_cabling.md": {"block": "Proposta_CABEAMENTO", "name": "Cabeamento e Infraestrutura de Dados"},
            "noc_monitoring_support.md": {"block": "Proposta_NOC", "name": "Sustentação, Monitoramento e Suporte NOC"},
            "struct_assessment.md": {"block": "Proposta_ASSESSMENT", "name": "Assessment e Diagnóstico de Infraestrutura"}
        }
        
        config = product_config.get(intent.selected_tech_template, {"block": "Proposta_COMPLETA", "name": "Solução Integrada de TI"})
        selected_tech = config["block"]
        detected_product_name = config["name"]
        
        sequence.append(("05-tecnico", selected_tech))
        
        sequence.append("06-trabalho")        # Work periods

        # Commercial sections (Only if not split technical)
        if not intent.split_proposal:
            comm_block = "07-comercial"
            if intent.is_assessment:
                # Forçamos o uso do bloco comercial de Assessment se a flag estiver ativa
                sequence.append((comm_block, "Proposta_ASSESSMENT_COM"))
            else:
                sequence.append(comm_block)
            
        sequence.extend([
            "08-premissas",       # Premissas e Exclusões
            "09-encerramento"     # Entregáveis e Conclusão
        ])

        # 3. Context Preparation
        base_id = "D2601" + datetime.now().strftime("%d%m")
        project_cleaned = intent.project_name.replace("Marata", "").replace("Maratá", "").replace("Bionovis", "").strip()
        project_cleaned = re.sub(r'\s+(para a|da|na)\s+planta$', '', project_cleaned, flags=re.I).strip()
        project_cleaned = re.sub(r'\s+S\.?A\.?$', '', project_cleaned, flags=re.I).strip()
        
        # Format processing time (e.g. 1.2s)
        benchmark_str = f"{processing_time:.1f}s"

        context = {
            "proposal_id": base_id,
            "project_name": project_cleaned,
            "product_name": detected_product_name, 
            "client_fullname": intent.contact_name or "Responsável Técnico",
            "client_company": intent.client_name, # CORREÇÃO: Força o uso do client_name identificado
            "provider_name": "EGE Soluções Industriais",
            "provider_short": "EGE",
            "date": datetime.now().strftime("%d/%m/%Y"),
            "city": "Jundiaí",
            "state": "SP",
            "include_network": include_network,
            "company_short_name": intent.company_short_name or (intent.company_name.split()[0] if intent.company_name else "Cliente"), 
            "total_hardware": format_br_currency(proposal.total_hardware_venda),
            "total_hardware_raw": proposal.total_hardware_venda,
            "total_labor": format_br_currency(proposal.total_labor_venda),
            "total_services": format_br_currency(proposal.total_services_venda),
            "total_services_venda_raw": proposal.total_services_venda,
            "total_expenses": format_br_currency(proposal.total_expenses_venda),
            "total_expenses_raw": proposal.total_expenses_venda,
            "grand_total": format_br_currency(proposal.grand_total_venda),
            "version": "A", # Nova diretriz: Sempre versão A inicialmente
            "contact_name": intent.contact_name or "Responsável Técnico",
            "company_name": intent.client_name, # CORREÇÃO: Templates legados usam company_name como Cliente
            "project_motivation": intent.project_motivation,
            "topics": proposal.topics,
            "labor_items": proposal.labor_table,
            "ai_research_count": proposal.ai_research_count,
            "total_hours": sum(item.hours for item in proposal.labor_table),
            "payment_term": proposal.payment_term,
            "opex": proposal.opex_data if not intent.is_assessment else None, # Suprime OPEX no Assessment
            "processing_time_bench": benchmark_str,
            "detected_hardware": intent.detected_hardware_list,
            "tech_template_name": intent.selected_tech_template,
            "comm_template_name": intent.selected_comm_template,
        }

        # Merge Extra Context (Stage 3 Redaction)
        if extra_context:
            context.update(extra_context)


        
        # Helper: Hierarchical Technical Scope (9 Pillars)
        technical_hierarchy = [
            {"id": 1, "title": "Design de Arquitetura", "keywords": ["LLD", "Design de Arquitetura", "Aprovações", "Design", "Projeto", "Desenho", "Planejamento"]},
            {"id": 2, "title": "Instalação Física", "keywords": ["Instalação Física", "Rack", "PDU", "Cabeamento", "Fisica", "Infraestrutura Física", "Montagem"]},
            {"id": 3, "title": "Implantação de Switches Core", "keywords": ["Switch Core", "Core Switch", "L3"]},
            {"id": 4, "title": "Infraestrutura de Servidores e Processamento", "keywords": ["VMware", "Cluster", "ESXi", "vCenter", "Host", "SAN", "Fibre Channel", "iSCSI", "Servidor", "Storage", "Windows Server", "Linux", "Hyper-V"]},
            {"id": 5, "title": "Implantação de Backup", "keywords": ["Backup", "Veeam", "Restauração", "NAS", "Salvaguarda"]},
            {"id": 6, "title": "Implantação de Firewall", "keywords": ["Firewall", "UTM", "Fortinet", "VPN", "Segurança Perímetro"]},
            {"id": 7, "title": "Implantação de Appliance Monitoramento", "keywords": ["Appliance", "Monitoring", "Appliance de Monitoramento"]},
            {"id": 8, "title": "Implantação de Cluster Kubernetes", "keywords": ["Kubernetes", "K8s", "PAS-X", "Pods", "Körber", "Pod"]},
            {"id": 9, "title": "Implantação de Zabbix + Grafana", "keywords": ["Zabbix", "Grafana", "Dashboard", "Observabilidade", "Dashboards"]}
        ]

        structured_technical_scope = []
        used_topic_ids = set()

        # Prioritize matching
        for pillar in technical_hierarchy:
            pillar_topics = []
            for topic in proposal.topics:
                if topic.topic_id in used_topic_ids:
                    continue
                
                text_to_check = (topic.description + " " + topic.topic_id).lower()
                if any(k.lower() in text_to_check for k in pillar["keywords"]):
                    activities = [L.activity for L in proposal.labor_table if L.topic == topic.topic_id and not L.is_contingency and L.activity_type != "Logística"]
                    if activities:
                        unique_acts = []
                        for a in activities:
                            if a not in unique_acts: unique_acts.append(a)
                        
                        clean_title = topic.description.split('(')[0].strip()
                        
                        # Tenta encontrar a justificativa original no Intent
                        summary = ""
                        for item in intent.scope_items:
                            # Match aproximado pelo nome do item
                            if item.name.lower() in topic.description.lower() or topic.description.lower() in item.name.lower():
                                summary = item.summary_rational
                                break
                        
                        pillar_topics.append({
                            "title": clean_title,
                            "activities": unique_acts,
                            "summary": summary
                        })
                        used_topic_ids.add(topic.topic_id)
            
            if pillar_topics:
                structured_technical_scope.append({
                    "id": pillar["id"],
                    "title": pillar["title"],
                    "sub_topics": pillar_topics
                })

        # Add remaining topics as item 10 if any
        others = []
        for topic in proposal.topics:
            if topic.topic_id not in used_topic_ids:
                activities = [L.activity for L in proposal.labor_table if L.topic == topic.topic_id and not L.is_contingency and L.activity_type != "Logística"]
                if activities:
                    unique_acts = []
                    for a in activities:
                        if a not in unique_acts: unique_acts.append(a)
                    clean_title = topic.description.split('(')[0].strip()
                    
                    # Tenta encontrar a justificativa original no Intent
                    summary = ""
                    for item in intent.scope_items:
                        if item.name.lower() in topic.description.lower() or topic.description.lower() in item.name.lower():
                            summary = item.summary_rational
                            break
                    
                    others.append({
                        "title": clean_title,
                        "activities": unique_acts,
                        "summary": summary
                    })
        
        if others:
            structured_technical_scope.append({
                "id": 10,
                "title": "Atividades Complementares de Engenharia",
                "sub_topics": others
            })

        context["structured_technical_scope"] = structured_technical_scope

        # Metadata for Footer (Temperature)
        context["sizing_level"] = intent.sizing_mode.value if hasattr(intent.sizing_mode, 'value') else str(intent.sizing_mode)
        context["contingency_level"] = intent.contingency_level.value if hasattr(intent.contingency_level, 'value') else str(intent.contingency_level)
        context["engine_version"] = "GPT-Md v5.0 (Engines)"
        context["model_info"] = f"gemini-2.5-flash via {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"

        # Helper: Hardware summary for section 9
        context["hardware_items"] = [
            {
                "desc": h.description,
                "qty": h.qty,
                "part": h.partnumber,
                "is_client_supplied": intent.hardware_supply_by_client
            }
            for h in proposal.hardware_table if not h.is_misc
        ] if not intent.is_assessment else [] # Oculta tabela de hardware se for Assessment

        # 4. Final Assembly
        # A. UNIFIED Version
        context["proposal_title"] = f"{base_id}-A - Proposta Unificada"
        context["proposal_id_full"] = f"{base_id}"
        unified_md = self._render_sequence(sequence, context)
        
        # B. TECHNICAL Version
        tech_sequence = [s for s in sequence if s != "07-comercial"]
        tech_md = self._render_sequence(tech_sequence, context)
        
        # C. COMMERCIAL Version
        comm_sequence = ["01-capa", "02-carta", "03-institucional", "07-comercial", "09-encerramento"]
        comm_md = self._render_sequence(comm_sequence, context)

        # Filtering based on output_mode
        if output_mode == "full":
            outputs[f"PROPOSTA_UNIFICADA_{base_id}.md"] = unified_md
            outputs[f"PROPOSTA_TECNICA_{base_id}.md"] = tech_md
            outputs[f"PROPOSTA_COMERCIAL_{base_id}.md"] = comm_md
        elif output_mode == "splited":
            outputs[f"PROPOSTA_TECNICA_{base_id}.md"] = tech_md
            outputs[f"PROPOSTA_COMERCIAL_{base_id}.md"] = comm_md
        else: # unified
            outputs[f"PROPOSTA_UNIFICADA_{base_id}.md"] = unified_md

        # D. STANDALONE OPEX (NOC) Proposal
        if separate_opex and proposal.opex_data and proposal.opex_data.grand_total_monthly > 0:
            context["proposal_title"] = f"{base_id}-A - Proposta de Sustentação (NOC)"
            # Sequência focada em OPEX: Capa, Carta, Institucional, Comercial (que contém o NOC), Encerramento
            # O bloco 07-comercial lida com o if opex internamente.
            opex_sequence = ["01-capa", "02-carta", "03-institucional", "07-comercial", "09-encerramento"]
            opex_md = self._render_sequence(opex_sequence, context)
            outputs[f"PROPOSTA_NOC_SUSTENTACAO_{base_id}.md"] = opex_md

        return outputs

    def _render_sequence(self, sequence, context):
        full_md = ""
        for item in sequence:
            if isinstance(item, tuple):
                section, source = item
                raw_content = self._get_block_content(section, source)
            else:
                section = item
                raw_content = self._get_block_content(section)
                
            try:
                template = self.env.from_string(raw_content)
                rendered = template.render(**context)
                full_md += rendered + "\n\n"
            except Exception as e:
                full_md += f"\n[ERROR RENDERING {item}: {e}]\n\n"
        return full_md
