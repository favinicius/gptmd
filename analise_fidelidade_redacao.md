# Análise Técnica: Fidelidade de Redação e Comportamento do Gemini-3-Flash

Esta análise compara o comportamento nativo do modelo Gemini-3-Flash com as necessidades de fidelidade estrutural ao arquivo de estilo (`Proposta_EGE_IODC_Marata.pdf`), focando na prevenção de sínteses indesejadas.

## 1. Configurações Atuais de Temperatura e Comprimento

No código atual (`src/ai_agent.py`), as chamadas ao método `generate_content` (linhas 90, 155 e 235) são realizadas **sem parâmetros explícitos** de configuração de geração.

*   **Temperatura:** O padrão (default) do SDK é geralmente `1.0`. Para um gerador de propostas técnicas que exige precisão e clonagem de texto, este valor é excessivamente alto, permitindo que a IA "alucine" resumos para ganhar eficiência.
*   **Max Output Tokens:** Não há limite definido, o que permite respostas longas, mas a natureza do modelo "Flash" é otimizada para respostas rápidas e concisas, o que explica a tendência de transformar 15 itens de premissas em apenas 5 parágrafos sintetizados.

## 2. Estratégias para Impedir a Síntese (Loop de Conferência)

Para garantir que a densidade do arquivo de estilo seja mantida, a instrução deve mudar de "clonar o estilo" para um **protocolo de conferência obrigatória**.

### Alteração Sugerida no Prompt (`generate_proposal_markdown`)

Substituir as regras genéricas de redação por um comando de **Chain of Thought (Cadeia de Pensamento)**:

```markdown
## PROTOCOLO DE FIDELIDADE E DENSIDADE (Obrigatório)
1. **Contagem de Itens:** Antes de escrever as seções 'Premissas', 'Exclusões' e 'Responsabilidades', conte quantos itens existem no modelo de estilo.
2. **Replicação 1:1:** Sua proposta DEVE conter o mesmo número de itens (ou mais). É terminantemente PROIBIDO agrupar dois tópicos do estilo em um único parágrafo.
3. **Mecanismo de Verificação:** Se o modelo Maratá tem 20 exclusões, sua proposta deve listar 20 exclusões adaptadas.
```

## 3. Alteração Técnica no Código

É necessário forçar a precisão do modelo através do objeto `config` na chamada da API:

```python
# Sugestão de implementação no src/ai_agent.py
from google.genai import types

def generate_proposal_markdown(self, proposal, intent, style_context):
    # ...
    response = self.client.models.generate_content(
        model=MODEL_ID,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.1,         # Reduz a criatividade, aumenta a fidelidade
            max_output_tokens=8192,  # Garante espaço para o texto completo
            top_p=0.95
        )
    )
```

## Conclusão

O modelo Gemini-3-Flash sintetiza o conteúdo porque está operando em uma temperatura alta e sem diretrizes de "contagem de itens". Implementar um **Loop de Conferência** no prompt e reduzir a **Temperatura para 0.1** são as ações necessárias para garantir que a proposta final tenha a mesma densidade e rigor jurídico do arquivo de estilo original.
