# Análise Técnica: Prioridade de Instrução vs. Bundles Fixos

Esta análise detalha por que parâmetros numéricos explícitos na instrução do usuário (ex: "30 dias de planejamento") são sobrepostos pelos valores padrão do `db_mod.json`.

## 1. O Ponto de Bloqueio no Motor de Cálculo (`src/calculator.py`)

O "culpado" técnico é a estrutura condicional na função `_calculate_labor`, especificamente nas **linhas 94 a 97**:

```python
94:  if b_act.per_unit_hours > 0:
95:      effort_hours = b_act.per_unit_hours * scope_item.detected_quantity
96:  else:
97:      effort_hours = b_act.fixed_hours
```

**O que acontece aqui:**
*   Se o bundle no `db_mod.json` estiver definido com `per_unit_hours: 0` (como é o caso do bundle de **"Projeto / Design"** nas linhas 591-592 do JSON), o sistema **ignora completamente** o `detected_quantity` (onde estariam os seus "30 dias" ou "80 horas") e assume o valor fixo (ex: 16h).
*   Mesmo que a IA extraia corretamente o número 30 ou 80, ele é descartado no `else` da linha 97 porque a regra do bundle força a atividade a ser fixa.

## 2. A Rigidez na Alocação Diária (`src/calculator.py`)

Outro ponto onde os números explícitos são "achatados" é na conversão de esforço para horas alocadas, nas **linhas 115 e 116**:

```python
115: days = math.ceil(effort_hours / (qty_profs * 8))
116: allocated_hours = qty_profs * 8 * days
```

**O que acontece aqui:**
*   O sistema arredonda o esforço para o múltiplo mais próximo da capacidade da equipe por dia (`qty_profs * 8`).
*   Se você tem uma equipe (`team_size`) de 2 pessoas e o esforço calculado (ou fixo) foi de 12h, o `math.ceil` arredonda para 1 dia, resultando em **16h** (`2 pessoas * 8h * 1 dia`). Isso explica por que valores como "16h" aparecem com tanta frequência: é a capacidade mínima de uma equipe de 2 pessoas em 1 dia de trabalho.

## 3. Limitação na Extração da IA (`src/ai_agent.py`)

No arquivo **`src/ai_agent.py`**, na definição do prompt de extração:

*   **Linha 45-46:** A IA é instruída a extrair `detected_quantity` como um inteiro. 
*   **O Problema de Semântica:** Quando o usuário diz "80 horas de curso", a IA muitas vezes interpreta que a **Quantidade** é "1" (um curso) e que "80 horas" é uma nota de contexto. Como não há um campo `explicit_total_hours` no objeto `Intent`, a informação numérica de tempo se perde antes mesmo de chegar ao calculador.

## Resumo da Falha de Prioridade

| Cenário | Onde perde a prioridade | Causa Técnica |
| :--- | :--- | :--- |
| **Planejamento (30 dias)** | `src/calculator.py:97` | Bundle "Projeto" tem `per_unit_hours: 0`, forçando o uso do `fixed_hours: 16`. |
| **Curso (80 horas)** | `src/ai_agent.py:45` | A IA mapeia "Curso" como 1 unidade. O calculador aplica o fallback de 8h/un e a alocação de equipe (2 profs) arredonda para **16h** totais. |

---

**Sugestão de Correção:**
Para que a instrução prevaleça, o calculador deve tratar o `fixed_hours` como um **piso (mínimo)** quando uma quantidade explícita for detectada, ou a IA deve ser instruída a mapear explicitamente tempos de duração para o campo de quantidade caso o item de escopo seja um serviço baseado em tempo.
