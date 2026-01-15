import json
from src.models import Intent, ProposalData

class ProposalAssembler:
    def __init__(self, agent):
        self.agent = agent

    def assemble_proposal(self, proposal: ProposalData, intent: Intent, style_context: str = "") -> str:
        """
        Gera o markdown da proposta usando a IA, com blindagem de escopo interno.
        """
        
        # 1. Privacy Filter (Blindagem de Redação)
        # Filtra itens com visibility="internal" para que NÃO apareçam no texto gerado
        public_scope_items = [
            item for item in intent.scope_items 
            if item.visibility == "public"
        ]
        
        # Cria um objeto Intent "dummy" apenas com itens públicos para serialização
        # (Não alteramos o intent original para não perder referências de custo)
        public_intent_dict = intent.model_dump()
        public_intent_dict["scope_items"] = [i.model_dump() for i in public_scope_items]
        
        # Serialização para o Prompt
        scope_json = json.dumps(public_intent_dict["scope_items"], indent=2, ensure_ascii=False)
        logistics_json = intent.detailed_logistics.model_dump_json(indent=2) if intent.detailed_logistics else "{}"
        data_json = proposal.model_dump_json(indent=2)
        
        # 2. Prompt Construction (Moved from ai_agent.py)
        prompt = f"""
        # ATUE COMO SR. PROPOSAL ENGINEER - REDAÇÃO FINAL (V1.2 - PROTOCOLO DE CONTAGEM)

        Você é um Engenheiro de Propostas Meticuloso. Sua tarefa é **CLONAR** a estrutura e a densidade de conteúdo do arquivo de estilo (`style_content`).

        ## INPUTS
        1. **DADOS CALCULADOS (JSON - Financeiro Completo)**:
           {data_json}
           
        2. **INTENÇÃO DO USUÁRIO**:
           - Cliente: {intent.client_name}
           - Empresa: {intent.company_name}
           - Projeto: {intent.project_name}
        
        3. **ESCOPO TÉCNICO VENDIDO (Scope Items - APENAS PÚBLICOS)**:
           {scope_json}

        4. **PLANO LOGÍSTICO (Logistics Plan)**:
           {logistics_json}

        5. **ARQUIVO DE ESTILO (Style Text - REFERÊNCIA DE ESTRUTURA E CONTEÚDO)**:
           {style_context[:15000]} 

        ---
        
        ## REGRAS DE OURO PARA REDAÇÃO (FIDELIDADE MÁXIMA v2.1)
        
        1.  **PROTOCOLO DE CONTAGEM E ADAPTAÇÃO (IMPERATIVO)**: 
            - Analise cada uma das premissas e exclusões presentes no arquivo de estilo (`style_content`).
            - **ADAPTE CADA UMA DELAS** para o contexto técnico deste projeto (ex: IODC, Disaster Recovery, Migração, Nuvem).
            - É expressamente **PROIBIDO** usar premissas genéricas. Quero uma lista **LONGA, DETALHADA E PROTETIVA**.
            - Se o modelo de estilo contém 15 premissas, você deve gerar no mínimo 15 premissas adaptadas. Não resuma.
        2.  **Seções Padrão (Boilerplate):** Para seções como 'Aviso Legal', 'Confidencialidade', 'Garantia', 'Exclusões' e 'Responsabilidades', use o texto do modelo de referência quase *ipsis litteris*. Apenas substitua os nomes (Cliente/Empresa) e datas. Não invente, não encurte.
        3.  **Seções Técnicas (Objetivo/Escopo):** Aqui você deve usar o conteúdo técnico extraído (dos inputs de Escopo e Dados Calculados), mas escreva usando o **vocabulário e a formatação** do modelo. Se o modelo usa bullet points detalhados, use bullet points detalhados.
        4.  **Tabelas Financeiras:** Insira APENAS o Resumo de Investimento (Totalizadores). NÃO insira tabelas detalhadas item a item no corpo do texto (elas já existem em anexos).
        5.  **DENSIDADE:** Nunca resuma. Seja prolixo onde o modelo for prolixo. Use Temperature 0.1 para evitar criatividade excessiva.

        ## DIRETRIZES FINAIS
        - **Estrutura de Tópicos:** Siga rigorosamente a ordem de tópicos (Índice) encontrada no arquivo de estilo.
        - **Conteúdo Interno vs Público**: A lista de escopo fornecida acima JÁ ESTÁ FILTRADA. Não mencione itens que não estejam nela. O custo total, porém (nos DADOS CALCULADOS), inclui tudo. Confie no JSON de dados.
        - **Objetivo:** O arquivo final deve ser indistinguível de uma proposta feita manualmente, mantendo todas as cláusulas de segurança e o rigor técnico do PDF de exemplo.

        Responda APENAS com o Markdown da proposta.
        """

        # 3. Call AI Agent (Generic Method)
        # We assume agent has a generic generate_content method exposed now.
        return self.agent.generate_content(prompt, temperature=0.1)
