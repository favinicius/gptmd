# Análise Técnica: Lacunas no Planejamento de Logística Multimodal

Esta análise detalha por que o trecho terrestre "Jundiaí-Aeroporto" é ignorado e como a estrutura atual do sistema impede a detecção de múltiplos modais integrados.

## 1. O Problema da Extração (Onde a informação se perde)

O motivo técnico reside no **esquema de dados (Data Schema)** definido no prompt da função `plan_logistics` em `src/ai_agent.py`.

*   **Prompt da IA (Linhas 142-150):** O JSON de saída possui campos para `requires_flight` e `estimated_daily_km`, mas **não possui um campo para "Mobilização Terrestre de Origem"**.
*   **Consequência:** Embora a IA leia o texto "Jundiaí-Aeroporto", ela não tem um campo no objeto `LogisticsPlan` para armazenar essa quilometragem específica. A informação é descartada na fase de tradução "Texto -> JSON".

## 2. Limitação da Lógica Multimodal

A lógica atual é **sequencial e isolada (Monomodal por etapa)**. 

No `src/calculator.py` (`_calculate_logistics`), o cálculo segue um fluxo fixo:
1.  **Aéreo:** Se `requires_flight` é verdadeiro, adiciona o custo do voo.
2.  **Terrestre Local:** O cálculo de KM (`trip_km`) é estritamente baseado no `estimated_daily_km` multiplicado pelos dias de estadia no destino.

O sistema assume o seguinte trajeto padrão:
`[Origem] --(Voo)--> [Destino] --(Carro Local)--> [Fábrica]`

Ele **não prevê** a perna inicial:
`[Sua Casa/Empresa] --(KM de Mobilização)--> [Aeroporto]`

## 3. Ajustes Necessários no `calculator.py`

Para que o KM de Jundiaí seja somado aos custos, o ajuste deve ser feito em duas frentes:

### A. Expansão do Modelo (`src/models.py`)
Adicionar um campo `mobilization_km` ao `LogisticsPlan` para capturar deslocamentos de ida/volta ao aeroporto ou terminais de saída.

### B. Ajuste no Cálculo de Despesas (`src/calculator.py`)
Injetar logicamente a "Mobilização" como uma despesa de KM separada do deslocamento diário:

```python
# Sugestão de correção lógica:
if plan.mobilization_km > 0:
    total_mob_km = plan.mobilization_km * 2 # Ida e Volta
    proposal.expense_table.append(CalculatedExpense(
        topic="LOG-00", # Tópico de Mobilização Geral
        description=f"Mobilização Terrestre Origem (ex: Jundiaí-Aeroporto)",
        qty=total_mob_km,
        unit_price=policies.km_reimbursement,
        total_price=total_mob_km * policies.km_reimbursement
    ))
```

## Conclusão

O trecho terrestre inicial é ignorado porque o sistema trata o voo como o "ponto de partida zero", sem considerar o deslocamento necessário para chegar até ele. Para corrigir, deve-se permitir que a IA capture essa distância em um campo de **Mobilização** e que o motor de cálculo aplique a taxa de reembolso de KM sobre esse valor.
