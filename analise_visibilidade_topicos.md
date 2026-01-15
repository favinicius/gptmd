# Análise Técnica: Fluxo de Dados e Governança de Visibilidade (Interno vs. Externo)

Esta análise detalha como o sistema lida com a visibilidade dos tópicos entre o cálculo financeiro e a redação da proposta, identificando fragilidades e propondo uma solução estrutural.

## 1. Avaliação do Fluxo Atual

### Existe classificação 'INTERNO' vs 'EXTERNO'?
**Não.** Atualmente, não existe nenhum mecanismo no código (`src/main.py`), nos modelos (`src/models.py`) ou no banco de dados (`db_mod.json`) que rotule um item de escopo como "interno" ou "externo". Todos os itens extraídos pela IA são tratados como membros iguais do objeto `Intent`.

### Como o gerador decide o que omitir?
A omissão é **puramente semântica e baseada em contexto** realizada pelo LLM (Gemini) no método `generate_proposal_markdown`.
*   O `main.py` entrega o objeto `proposal` (com todos os valores calculados) e o objeto `intent` (com todos os detalhes do escopo).
*   A IA decide o que escrever baseada no PDF de estilo fornecido. Se o estilo não menciona "Custos de SHE", a IA tende a omiti-lo, mas não há uma trava lógica que garanta isso.

---

## 2. Fragilidade Identificada
O maior risco é a **inconsistência**. Como a IA decide o que mostrar:
1.  Ela pode omitir um item importante porque ele não estava no "modelo de estilo".
2.  Ela pode expor um item interno (ex: "Margem de Contingência") se o prompt ou o texto técnico forem ambíguos.

---

## 3. Proposta de Alteração Estrutural (Filtro 100% Confiável)

Para garantir que um tópico exista no cálculo (MOD/DIV) mas seja invisível na proposta, a lógica deve ser movida da "vontade da IA" para o **esquema de dados**.

### Passo A: Modificar o Modelo (`src/models.py`)
Adicionar um campo de visibilidade ao `ScopeItem`:

```python
class ScopeItem(BaseModel):
    name: str
    detected_quantity: int = 1
    action_type: Literal["install", "migrate_p2v", "supply_only", "turnkey", "design"]
    visibility: Literal["public", "internal"] = "public"  # <-- NOVO CAMPO
    context_note: str
```

### Passo B: Treinar a Interpretação (`src/ai_agent.py`)
No prompt do método `interpret_instruction`, deve-se adicionar a regra:
> "Sempre que um item for preparatório (ex: SHE, mobilização) ou de apoio interno, defina `visibility: internal`. Se for um entregável de valor para o cliente, defina `visibility: public`."

### Passo C: Filtro de Saída no Orquestrador (`src/main.py`)
No `main.py`, antes de chamar a geração do Markdown, realizamos a filtragem:

```python
# 1. O Motor de Cálculo usa o INTENT COMPLETO (Garante o preço correto)
proposal = engine.calculate_proposal(intent)

# 2. Criamos um 'Intent Público' para a Redação (Garante o sigilo técnico)
public_intent = intent.model_copy()
public_intent.scope_items = [i for i in intent.scope_items if i.visibility == "public"]

# 3. A IA de Redação só recebe o que pode ser escrito, mas os totais (R$) vêm do 'proposal' completo
markdown_output = agent.generate_proposal_markdown(proposal, public_intent, style_context=style_content)
```

## Conclusão
Esta abordagem é a única 100% confiável porque **remove o acesso da IA de redação aos dados sensíveis**, enquanto mantém a integridade matemática do `grand_total` calculado pelo `PricingEngine`.
