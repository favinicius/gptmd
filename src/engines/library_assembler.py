import os
import re
from datetime import datetime
from pathlib import Path
from jinja2 import Template
from src.models import ProposalData, Intent, format_br_currency

class LibraryAssembler:
    """
    Assembler that builds high-fidelity proposals using the library blocks.
    """
    def __init__(self, library_dir="templates/library"):
        self.library_dir = Path(library_dir)
        self.default_source = "Proposta_EGE_IODC_Marata"

    def _get_block_content(self, section_name: str, source_name: str = None) -> str:
        """Finds and reads the content of a block in the library."""
        if source_name is None:
            source_name = self.default_source
            
        section_path = self.library_dir / section_name
        if not section_path.exists():
            return f"\n<!-- SECTION {section_name} NOT FOUND -->\n"
            
        file_path = section_path / f"{source_name}.md"
        if not file_path.exists():
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

    def assemble(self, proposal: ProposalData, intent: Intent) -> dict:
        """
        Assembles the proposal(s) based on intent.
        Returns a dict of {filename: content}.
        """
        outputs = {}
        
        # 1. Base Logic
        include_network = True
        if "sem rede" in intent.project_name.lower() or intent.selected_tech_template == "iodc_no_net.md":
            include_network = False

        # 2. Sequence Definition (Refined Architecture)
        sequence = [
            "Capa",                         # Cover Page
            "_resumo_executivo",             # #1
            "_aviso",                        # #2
            "_informação_confidencial",      # #3
            "_histórico_de_revisões",        # #4
            "_lista_de_revisões",            # #5
            "_objetivo_geral",               # #6
            "_benefícios",                   # #7
            "_visão_geral_da_solução_proposta", # #8
            "_relação_de_equipamentos_e_softwares_fornecidos", # #9 (Consolidated)
            "_escopo_técnico_e_detalhamento_das_atividades",    # #10 (Consolidated summary)
            "_testes,_validações_e_comissionamento",                # #11
            "_equipe_chave_e_responsabilidades",                    # #12
            "_cronograma_sugerido",                                 # #13
            "_prazo_de_mobilização",                                # 13.1
            "_treinamento_e_transferência_de_conhecimento",        # #14
            "_sustentação_e_monitoramento_contínuo",               # #15
            "_lista_de_entregáveis",                                # #16
            "_premissas"                                            # #17
        ]

        # 3. Context Preparation
        base_id = "D2601" + datetime.now().strftime("%d%m")
        context = {
            "proposal_id": base_id,
            "project_name": intent.project_name.replace("Marata", "").replace("Maratá", "").strip(),
            "client_fullname": intent.client_name,
            "client_company": intent.company_name,
            "provider_name": "EGE Soluções Industriais",
            "provider_short": "EGE",
            "date": datetime.now().strftime("%d/%m/%Y"),
            "city": "Ilhéus",
            "state": "BA",
            "include_network": include_network, # For conditional logic in blocks
            "total_hardware": format_br_currency(proposal.total_hardware),
            "total_labor": format_br_currency(proposal.total_labor),
            "total_services": format_br_currency(proposal.total_services),
            "total_expenses": format_br_currency(proposal.total_expenses),
            "grand_total": format_br_currency(proposal.grand_total),
            "company_name": "EGE Soluções Industriais", # Backwards compatibility
        }

        # 4. Final Assembly
        if intent.split_proposal:
            # TECHNICAL VERSION
            context["proposal_title"] = f"{base_id} - Proposta Técnica"
            tech_md = self._render_sequence(sequence, context)
            outputs[f"PROPOSTA_TECNICA_{base_id}.md"] = tech_md
            
            # COMMERCIAL VERSION (Usually simpler but here we use similar structure)
            context["proposal_title"] = f"{base_id} - Proposta Comercial"
            # In a real scenario, we might skip technical details
            comm_md = self._render_sequence(sequence, context) # Simplified for now
            outputs[f"PROPOSTA_COMERCIAL_{base_id}.md"] = comm_md
        else:
            # UNIFIED VERSION
            context["proposal_title"] = f"{base_id} - Proposta Técnica e Comercial"
            unified_md = self._render_sequence(sequence, context)
            outputs[f"PROPOSTA_UNIFICADA_{base_id}.md"] = unified_md

        return outputs

    def _render_sequence(self, sequence, context):
        full_md = ""
        for section in sequence:
            raw_content = self._get_block_content(section)
            try:
                template = Template(raw_content)
                rendered = template.render(**context)
                full_md += rendered + "\n\n"
            except Exception as e:
                full_md += f"\n[ERROR RENDERING {section}: {e}]\n\n"
        return full_md
