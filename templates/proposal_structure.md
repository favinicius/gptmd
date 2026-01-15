# Proposta Técnica: {{ client_name }}

## 1. Visão Executiva

**Objetivo:** Modernização e Estruturação da Rede Industrial.

A EGE Soluções apresenta esta proposta técnica para o fornecimento de infraestrutura de rede, garantindo alta disponibilidade e segurança para a operação da {{ client_name }}.

## 2. Escopo de Fornecimento

### 2.1 Hardware e Materiais (Tabela MAT)

| Item | P/N | Qtd | Valor Un. (R$) | Total (R$) |
| :--- | :--- | :--- | :--- | :--- |
{% for item in hardware_table %}
| {{ item.description }} | {{ item.partnumber }} | {{ item.qty }} | {{ "%.2f"|format(item.unit_price) }} | {{ "%.2f"|format(item.total_price) }} |
{% endfor %}
| **Total Hardware** | | | | **{{ "%.2f"|format(total_hardware) }}** |

### 2.2 Serviços de Engenharia e Instalação (Tabela MOD)

| Perfil / Atividade | Horas | Taxa (R$/h) | Total (R$) |
| :--- | :--- | :--- | :--- |
{% for item in labor_table %}
| **{{ item.role }}** - {{ item.activity }} | {{ item.hours }} | {{ "%.2f"|format(item.hourly_rate) }} | {{ "%.2f"|format(item.total_price) }} |
{% endfor %}
| **Total Serviços** | | | **{{ "%.2f"|format(total_labor) }}** |

{% if service_table %}
### 2.3 Serviços Especializados (Tabela SET)

| Descrição | Qtd | Valor Un. | Total |
| :--- | :--- | :--- | :--- |
{% for item in service_table %}
| {{ item.description }} | {{ item.qty }} | {{ "%.2f"|format(item.unit_price) }} | {{ "%.2f"|format(item.total_price) }} |
{% endfor %}
| **Total Especial** | | | **{{ "%.2f"|format(total_services) }}** |
{% endif %}

### 2.4 Logística e Despesas (Tabela DIV)

| Item | Qtd | Valor Un. | Total |
| :--- | :--- | :--- | :--- |
{% for item in expense_table %}
| {{ item.description }} | {{ item.qty }} | {{ "%.2f"|format(item.unit_price) }} | {{ "%.2f"|format(item.total_price) }} |
{% endfor %}
| **Total Despesas** | | | **{{ "%.2f"|format(total_expenses) }}** |

## 3. Resumo de Investimento

Abaixo o consolidado dos valores:

*   **Hardware / Materiais:** R$ {{ "%.2f"|format(total_hardware) }}
*   **Serviços (MOD):** R$ {{ "%.2f"|format(total_labor) }}
*   **Serviços Especiais (SET):** R$ {{ "%.2f"|format(total_services) }}
*   **Logística (DIV):** R$ {{ "%.2f"|format(total_expenses) }}

### **Total Geral: R$ {{ "%.2f"|format(grand_total) }}**

---
*Proposta gerada automaticamente por GPT-Md.*
