import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from src.models import ProposalData, Intent, format_br_currency

class ProposalAssemblerV2:
    def __init__(self, template_dir="templates/v2"):
        self.template_dir = template_dir
        self.env = Environment(
            loader=FileSystemLoader(searchpath=template_dir),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        self._register_filters()

    def _register_filters(self):
        """Registra filtros customizados para uso no Jinja2."""
        
        def filter_brl(value):
            if value is None: return "0,00"
            try:
                val = float(value)
                return f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            except (ValueError, TypeError):
                return str(value)

        def filter_date_ptbr(value, format="%d/%m/%Y"):
            if isinstance(value, str): return value # Já formatado
            if isinstance(value, datetime):
                return value.strftime(format)
            return datetime.now().strftime(format)
            
        def filter_role_short(value):
            """Encurta nomes de roles para tabelas."""
            mapping = {
                "Analista de Infraestrutura": "Analista Infra",
                "Auxiliar de Redes": "Auxiliar",
                "Gestor de Projetos": "Gestor",
                "Engenheiro de Redes": "Eng. Redes",
                "Arquiteto de Soluções": "Arquiteto"
            }
            return mapping.get(value, value)

        self.env.filters["brl"] = filter_brl
        self.env.filters["date_pt"] = filter_date_ptbr
        self.env.filters["role_short"] = filter_role_short

    def assemble(self, proposal: ProposalData, intent: Intent, output_path: str = "output") -> dict:
        """
        Renderiza a proposta usando templates Jinja2.
        Retorna um dicionário com os nomes dos arquivos gerados e seus conteúdos.
        """
        
        # Contexto global disponível para todos os templates
        context = {
            "proposal": proposal,
            "intent": intent,
            "now": datetime.now(),
            "client": intent.client_name,
            "project": intent.project_name
        }

        outputs = {}
        
        # Seleção de template mestre (pode ser dinâmico no futuro)
        # Por enquanto, assumimos um template mestre que faz includes
        master_template = "master_full.md.j2"
        
        try:
            template = self.env.get_template(master_template)
            content = template.render(**context)
            
            filename = f"PROPOSTA_{intent.client_name.replace(' ', '_').upper()}_{datetime.now().strftime('%Y%m%d')}.md"
            outputs[filename] = content
            
            # Se split_proposal for True, podemos renderizar templates parciais aqui
            if intent.split_proposal:
                tech_tpl = self.env.get_template("technical/technical_only.md.j2")
                outputs["ANEXO_TECNICO.md"] = tech_tpl.render(**context)
                
                comm_tpl = self.env.get_template("commercial/commercial_only.md.j2")
                outputs["ANEXO_COMERCIAL.md"] = comm_tpl.render(**context)
                
        except Exception as e:
            print(f"[!] Erro ao renderizar template Jinja2: {e}")
            # Fallback ou re-raise
            raise e

        # Salvar arquivos (opcional aqui, mas útil para debug do assembler)
        # O main.py geralmente salva, mas retornamos o conteúdo para ele
        return outputs
