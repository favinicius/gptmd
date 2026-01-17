import json
from datetime import datetime
from src.models import Intent, ProposalData, format_br_currency

class ProposalAssembler:
    def __init__(self, agent):
        self.agent = agent

    def _format_brazilian_numbers(self, data: dict) -> dict:
        """
        Recursivamente formata números no dicionário para o padrão brasileiro:
        - Inteiros (ou floats .0): string sem decimal.
        - Floats: string com vírgula e ponto como milhar.
        """
        if isinstance(data, dict):
            return {k: self._format_brazilian_numbers(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._format_brazilian_numbers(i) for i in data]
        elif isinstance(data, (int, float)):
            if data == int(data) and not isinstance(data, bool):
                return str(int(data))
            return format_br_currency(data)
        return data

    def fill_template_segment(self, segment_text: str, context_data: dict) -> str:
        """
        Processa um segmento de template. 
        - Se contiver a tag IA_DYNAMIC_BLOCK, envia para a IA.
        - Caso contrário, faz substituição de variáveis {{}}.
        """
        if "<!-- IA_DYNAMIC_BLOCK_START -->" in segment_text:
            return self._generate_dynamic_segment(segment_text, context_data)
        else:
            return self._fill_static_variables(segment_text, context_data)

    def _fill_static_variables(self, text: str, ctx: dict) -> str:
        """
        Substituição simples de placeholders {{}}.
        """
        replacements = {
            "{{CLIENT_NAME}}": ctx["intent"].company_name or "CLIENTE NÃO INFORMADO",
            "{{PROJECT_NAME}}": ctx["intent"].project_name,
            "{{CLIENT_CONTACT}}": ctx["intent"].client_name or "A/C Responsável",  
            "{{AUTHOR_NAME}}": "Roberto Pereira",
            "{{COMPANY_NAME}}": "EGE Soluções Industriais",
            "{{DATE}}": ctx.get("date", "16/01/2026"),
            "{{TOTAL_HARDWARE}}": ctx["totals"].get("hardware", "0,00"),
            "{{TOTAL_LABOR}}": ctx["totals"].get("labor", "0,00"),
            "{{TOTAL_SERVICES}}": ctx["totals"].get("services", "0,00"),
            "{{TOTAL_EXPENSES}}": ctx["totals"].get("expenses", "0,00"),
            "{{GRAND_TOTAL}}": ctx["totals"].get("grand_total", "0,00"),
        }
        
        result = text
        for placeholder, value in replacements.items():
            result = result.replace(placeholder, str(value))
        return result

    def _generate_dynamic_segment(self, segment_text: str, ctx: dict) -> str:
        """
        Chama a IA para processar o segmento dinâmico.
        """
        # Remove as tags de comentário para o prompt
        clean_template = segment_text.replace("<!-- IA_DYNAMIC_BLOCK_START -->", "").replace("<!-- IA_DYNAMIC_BLOCK_END -->", "")
        
        prompt = f"""
        # AGENTE DE REDAÇÃO V4.0 - BLOCO DINÂMICO
        Você deve preencher o gabarito abaixo seguindo rigorosamente as instruções contidas nele.
        
        ## GABARITO / INSTRUÇÕES:
        {clean_template}
        
        ## CONTEXTO DO PROJETO:
        - Cliente: {ctx['intent'].client_name}
        - Projeto: {ctx['intent'].project_name}
        - Escopo Detalhado (JSON): {ctx['scope_json']}
        - Plano Logístico (JSON): {ctx['logistics_json']}
        
        ## REGRAS DE OURO:
        - Fidelidade técnica total aos dados fornecidos.
        - Se houver discrepância entre o template e os dados, PRIORIZE OS DADOS (JSON).
        - Nunca use nomes proibidos (JDE, Maratá, Sergipe, etc). Use OFI / Ilhéus.
        
        Responda apenas com o Markdown resultante do preenchimento.
        """
        return self.agent.generate_content(prompt, temperature=0.1, max_output_tokens=4096)

    def assemble_proposal(self, proposal: ProposalData, intent: Intent, template_dir: str = "templates") -> dict:
        """
        Gera a proposta baseada no roteamento do Intent.
        Retorna um dicionário: {" filename.md": "conteúdo"}
        """
        from pathlib import Path
        t_path = Path(template_dir)
        
        # Preparação de dados
        formatted_totals = {
            "hardware": format_br_currency(proposal.total_hardware),
            "labor": format_br_currency(proposal.total_labor),
            "services": format_br_currency(proposal.total_services),
            "expenses": format_br_currency(proposal.total_expenses),
            "grand_total": format_br_currency(proposal.grand_total)
        }
        
        public_scope_items = [item for item in intent.scope_items if item.visibility == "public"]
        formatted_intent = self._format_brazilian_numbers(intent.model_dump())
        
        context = {
            "intent": intent,
            "totals": formatted_totals,
            "scope_json": json.dumps([item.model_dump() for item in public_scope_items], indent=2, ensure_ascii=False),
            "logistics_json": json.dumps(formatted_intent.get("detailed_logistics", {}), indent=2, ensure_ascii=False),
            "date": datetime.now().strftime("%d/%m/%Y")
        }

        # Fragmentos Base
        with open(t_path / "base" / "01_intro.md", "r", encoding="utf-8") as f:
            intro = self.fill_template_segment(f.read(), context)
        
        with open(t_path / "base" / "06_conclusao.md", "r", encoding="utf-8") as f:
            conclusao = self.fill_template_segment(f.read(), context)

        # Fragmento Técnico
        with open(t_path / "technical" / intent.selected_tech_template, "r", encoding="utf-8") as f:
            technical = self.fill_template_segment(f.read(), context)

        # Fragmento Comercial
        with open(t_path / "commercial" / intent.selected_comm_template, "r", encoding="utf-8") as f:
            commercial = self.fill_template_segment(f.read(), context)

        if intent.split_proposal:
            return {
                "PROPOSTA_TECNICA.md": f"{intro}\n\n{technical}\n\n{conclusao}",
                "PROPOSTA_COMERCIAL.md": f"{intro}\n\n{technical[:500]}... (Resumo do Escopo)\n\n{commercial}\n\n{conclusao}",
                "PROPOSTA_COMPLETA.md": f"{intro}\n\n{technical}\n\n{commercial}\n\n{conclusao}"
            }
        else:
            return {
                "PROPOSTA_COMPLETA.md": f"{intro}\n\n{technical}\n\n{commercial}\n\n{conclusao}"
            }



