# 19. PREÇOS E IMPOSTOS

Condições comerciais, valores e incidência de impostos aplicáveis à este projeto.

## 19.1. INVESTIMENTO EM CAPITAL (CAPEX) - TURNKEY

Pelos serviços contratados, fornecimento de todos os materiais e pela execução completa dos serviços, a CONTRATANTE pagará à CONTRATADA o valor total de **{{TOTAL_CAPEX}}**, que serão pagos conforme os Eventos de Pagamento descritos nesta proposta.

| Item | Descrição | Total |
|---|---|---|
{{TABLE_CAPEX_ITEMS}}
| | **VALOR TOTAL** | **{{TOTAL_CAPEX}}** |


## 19.2. DESPESAS OPERACIONAIS (OPEX) - CONTRATO DE MONITORAMENTO E SUPORTE 24/7

{% if opex %}
Para o serviço contínuo de monitoramento proativo e suporte técnico especializado (NOC/Sustentação), incluindo a locação e gestão da infraestrutura de conectividade (Appliance EGE + Links), com vigência de {{ opex.contract_duration_months }} meses:

*   **Mensalidade:** **R$ {{ opex.grand_total_monthly | brl }}**
*   **Franquia de Horas (F2):** {{ opex.support_hours_f2 }} horas mensais.

## 19.3. TOTAL DO INVESTIMENTO

| Item | Condição | Descrição | Total |
|---|---|---|---|
| 1 | NF. SERVIÇOS EGE | PROJETO TURNKEY {{PROJECT_NAME}} | {{GRAND_TOTAL}} |
| 2 | NF. SERVIÇOS EGE | SUPORTE E MONITORAMENTO {{ opex.contract_duration_months }} MESES | R$ {{ opex.contract_total_value | brl }} |
| | | **VALOR TOTAL** | **R$ {{ (proposal.grand_total_venda + opex.contract_total_value) | brl }}** |
{% else %}
Para o serviço contínuo de monitoramento proativo e suporte técnico especializado, com vigência de 12 meses após o aceite final do projeto, o valor mensal será definido conforme SLA.

## 19.3. TOTAL DO INVESTIMENTO

| Item | Condição | Descrição | Total |
|---|---|---|---|
| 1 | NF. SERVIÇOS EGE | PROJETO TURNKEY {{PROJECT_NAME}} | {{GRAND_TOTAL}} |
| | | **VALOR TOTAL** | **{{GRAND_TOTAL}}** |
{% endif %}


*Obs: Não se incluem na base de cálculo do INSS, valores de materiais fornecidos na prestação de serviços, conforme disposto na IN-RFB n° 2.110/2022. (cód. 7.02.03 / 237)*

## 19.5. IMPOSTOS

A EGE Soluções Industriais é uma empresa que opera sob o regime de lucro real, garantindo transparência e precisão na tributação dos serviços prestados. Todos os impostos especificados na tabela abaixo estão inclusos na presente proposta.

| Alíquota | IRPJ | CSLL | COFINS | PIS | CPP | ICMS | ISS | IPI |
|---|---|---|---|---|---|---|---|---|
| - | - | - | 7,60% | 1,65% | - | - | 5,00% | - |

*Serviços serão faturados com o Código 7.02.03/237*
