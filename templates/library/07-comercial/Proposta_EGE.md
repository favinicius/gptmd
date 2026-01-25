## 17. INVESTIMENTOS E CONDIÇÕES COMERCIAIS

Abaixo, apresentamos o resumo dos investimentos necessários para a execução deste projeto, divididos entre a implantação (CAPEX) e a sustentação mensal (OPEX).

### 17.1. INVESTIMENTO CAPEX (IMPLANTAÇÃO)

| ITEM | DESCRIÇÃO | VALOR (R$) |
| :--- | :--- | :--- |
{%- if total_hardware_raw > 0 %}
| Materiais | Fornecimento de Hardware e Softwares de Base | {{ total_hardware }} |
{%- endif %}
| Mão de Obra | Engenharia, Gestão e Instalação (EGE) | {{ total_labor }} |
{%- if total_services_venda_raw > 0 %}
| Serviços | Licenciamentos e Serviços Externos | {{ total_services }} |
{%- endif %}
{%- if total_expenses_raw > 0 %}
| Despesas | Despesas Logísticas e Administrativas | {{ total_expenses }} |
{%- endif %}
| **TOTAL CAPEX** | **Investimento Único** | **{{ grand_total }}** |

### 17.2. INVESTIMENTO OPEX (SUSTENTAÇÃO)

{% if opex %}
| ITEM | DESCRIÇÃO | VALOR MENSAL (R$) |
| :--- | :--- | :--- |
| Monitoramento e NOC | Serviços de Monitoramento Proativo e Suporte Técnico | R$ {{ opex.grand_total_monthly | brl }} |
| **TOTAL OPEX** | **Mensalidade (Contrato {{ opex.contract_duration_months }} meses)** | **R$ {{ opex.grand_total_monthly | brl }}** |

#### RELAÇÃO DE ATIVOS (CONSOLIDAÇÃO)
| Item Monitorado / Ativos | Quantidade |
| :--- | :---: |
{% for item in opex.items -%}
| {{ item.item_name }} | {{ item.quantity }} |
{% endfor %}

> [!TIP]
> **Franquia de Horas:** O contrato inclui uma franquia mensal de **{{ opex.support_hours_f2 }} horas (F2)** para atendimentos remotos.
{% else %}
| ITEM | DESCRIÇÃO | VALOR MENSAL (R$) |
| :--- | :--- | :--- |
| Monitoramento | Serviços de Sustentação 24x7 e Monitoramento Proativo | {{ total_services }} |
| **TOTAL OPEX** | **Mensalidade (Contrato 60 meses)** | **{{ total_services }}** |
{% endif %}

### 17.3. RESUMO GERAL DE INVESTIMENTOS

| CATEGORIA | DESCRIÇÃO | INVESTIMENTO |
| :--- | :--- | :---: |
| **CAPEX** | Total para Implantação do Projeto (Investimento Único) | **{{ grand_total }}** |
{% if opex -%}
| **OPEX** | Mensalidade de Serviços Recorrentes e Monitoramento | **R$ {{ opex.grand_total_monthly | brl }}** |
| **CONTRATO** | Valor Total Projetado (Fidelidade {{ opex.contract_duration_months }} meses) | **R$ {{ opex.contract_total_value | brl }}** |
{% else -%}
| **OPEX** | Mensalidade de Serviços Recorrentes | **{{ total_services }}** |
{%- endif %}


### 17.4. PRAZO DE MOBILIZAÇÃO
O prazo de mobilização para início do projeto, compreende o período em que a equipe técnica da **{{ provider_short }}** realizará as atividades de alinhamento, planejamento detalhado e revisão técnica do projeto. Este período antecede a **Reunião de Kick-Off**, data na qual o projeto será oficialmente iniciado em campo. Este prazo é de até **10 (dez) dias úteis** após a confirmação do pedido (PO).

### 17.5. HORAS EXTRAS
Intervenções solicitadas pela **{{ client_company }}** fora dos horários padrão acordados (noites, fins de semana ou feriados) serão faturadas conforme a tabela de multiplicadores:
*   Horas Extras (Seg-Sex após as 17:00): +50% sobre o valor da hora base.
*   Sábados, Domingos e Feriados: +100% sobre o valor da hora base.

### 17.6. PRAZO DE PAGAMENTO
O prazo de pagamento para os valores apresentados nesta proposta é de **{{ payment_term }} dias**, contados a partir da emissão da nota fiscal de cada evento de faturamento.

### 17.7. IMPOSTOS
Todos os impostos incidentes sobre a prestação de serviços e fornecimento de materiais já estão inclusos nos valores apresentados, conforme a legislação tributária vigente.

| EVENTO | MARCO DE ENTREGA (MILESTONE) | FATURAMENTO |
| :--- | :--- | :---: |
| **Início** | Aprovação do pedido e mobilização para projeto | 30% |
| **Sprints** | Entregáveis definidos na Entrevista de Alinhamento do projeto | 60% |
| **Conclusão** | Entrega final de projeto (Databook) | 10% |

### 17.9. DESLOCAMENTO
Todas as despesas de deslocamento terrestre da equipe técnica da **{{ provider_short }}** estão contempladas no valor de despesas logísticas.

### 17.10. REFEIÇÕES
As refeições da equipe de campo durante a execução do projeto estão inclusas, exceto quando houver acesso ao refeitório da planta, conforme acordado nas premissas.

### 17.11. EPIs, EPCs e MATERIAIS ADICIONAIS
A **{{ provider_short }}** fornecerá todos os EPIs e EPCs necessários para a segurança de seus profissionais. Materiais adicionais de consumo não previstos no projeto executivo serão orçados separadamente mediante aprovação prévia.

### 17.12. ATRASOS DE PAGAMENTO
Atrasos no pagamento dos marcos ou mensalidades OPEX acarretarão multa de 2% e juros de 1% ao mês *pro rata die*.

## 18. REAJUSTES E RESCISÃO - CONTRATO OPEX

### 18.1. REAJUSTES
O valor das mensalidades de sustentação (OPEX) será reajustado anualmente pela variação acumulada do IGPM-FGV ou, em sua ausência, pelo IPCA-IBGE.

### 18.2. RESCISÃO CONTRATUAL
Qualquer parte poderá rescindir o contrato de sustentação mediante aviso prévio de 90 (noventa) dias. Em caso de rescisao antecipada por iniciativa da **{{ client_company }}** antes do término do período de 60 meses, será devida multa compensatória equivalente a 30% das parcelas vincendas.