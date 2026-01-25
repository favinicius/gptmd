## 3. INVESTIMENTO COMERCIAL (HÍBRIDO)

### 3.1 Investimento de Implementação (CAPEX)

| Categoria | Descrição | Valor Total (R$) |
| :--- | :--- | :---: |
| **Implementação** | Hardware, Mão de Obra e Logística | {{GRAND_TOTAL}} |


{% if opex %}
### 3.2 Suporte e Sustentação (OPEX)

O serviço de Monitoramento e Suporte Contínuo (NOC) contempla a gestão proativa dos ativos abaixo listados:

| Item Monitorado / Conectividade | Quantidade |
| :--- | :---: |
{% for item in opex.items -%}
| {{ item.item_name }} | {{ item.quantity }} |
{% endfor %}

#### Investimento Mensal e Níveis de Serviço

| Descrição | Valor Mensal |
| :--- | :---: |
| **Monitoramento, Suporte e Conectividade** | **R$ {{ opex.grand_total_monthly | brl }}** |

> [!NOTE]
> **Franquia de Atendimento Técnico:**
> O contrato contempla uma franquia mensal de **{{ opex.support_hours_f2 }} horas** para atendimentos remotos em horário comercial (F2).
> *Atendimentos fora de horário (F3 - Madrugada/Feriados) consomem a franquia na proporção de 1:3 (1h F3 consome 3h de franquia).*

#### Projeção do Contrato

| Período | Investimento Total Estimado |
| :--- | :---: |
| **{{ opex.contract_duration_months }} Meses** | **R$ {{ opex.contract_total_value | brl }}** |

{% else %}
### 3.2 Suporte e Sustentação (OPEX)

| Serviço | Periodicidade | Investimento (R$) |
| :--- | :--- | :---: |
| Suporte Técnico Remoto 8x5 | Mensal | A DEFINIR |
| Manutenção Preventiva | Trimestral | A DEFINIR |

*Nota: Valores sob consulta baseados no inventário final.*
{% endif %}


## 4. CONDIÇÕES DE PAGAMENTO (MILESTONES)

| Marco (Milestone) | Evento de Pagamento | Percentual |
| :--- | :--- | :---: |
| **M1: Kick-off** | Aprovação do cronograma e mobilização de equipe | 30% |
| **M2: Sprints** | Conclusão das etapas de execução (instalação/configuração) | 60% |
| **M3: Aceite Final** | Entrega do Data Book e encerramento operacional | 10% |

## 5. PREMISSAS E TERMOS
1. Contrato de suporte com fidelidade de 12 meses (renovável).
2. Reajuste anual pelo IGPM/IPCA.
3. Prazo de pagamento: {{ payment_term | default(30) }} dias.
