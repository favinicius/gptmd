## 6. OBJETIVO GERAL
{% if custom_objective_md %}
{{ custom_objective_md }}
{% elif project_motivation %}
{{ project_motivation }}
{% else %}
Este informativo tem como objetivo apresentar a solução de **Sustentação, Monitoramento e Suporte NOC** para a infraestrutura de TI Industrial da planta **{{ client_company }}**. O foco é garantir a máxima disponibilidade, performance e segurança dos ativos existentes, através de uma camada de observabilidade avançada e suporte técnico especializado proativo.
{% endif %}

## 7. BENEFÍCIOS
{{ custom_benefits_md | default("A implementação da nossa solução de sustentação trará para a **" ~ company_short_name ~ "** ganhos significativos em resiliência e continuidade:\n\n### CONFIABILIDADE\n*   **Monitoramento 24x7:** Vigilância constante da saúde dos ativos para detecção precoce de falhas.\n*   **Suporte Especializado:** Acesso a especialistas em infraestrutura industrial para resolução rápida de incidentes.\n\n### OPERACIONAIS\n*   **MTTR Reduzido:** Identificação imediata da causa raiz, reduzindo o tempo médio de reparo.\n*   **Planejamento de Capacidade:** Visibilidade real sobre o uso de recursos para expansões futuras assertivas.") }}

## 8. VISÃO GERAL DA SOLUÇÃO PROPOSTA
{{ custom_vision_md | default("Nossa abordagem de serviços baseia-se na integração proativa entre ferramentas de monitoramento e equipes de engenharia, focando na estabilidade operacional do ambiente existente da **" ~ company_short_name ~ "**.") }}

## 9. RELAÇÃO DE EQUIPAMENTOS E SOFTWARES (EXISTENTES E NOVOS)
Abaixo listamos os ativos que serão objeto de monitoramento e suporte, conforme levantamento preliminar.

{% if (hardware_items and not hardware_items[0].is_client_supplied) %}
*Novos componentes de infraestrutura para monitoramento fornecidos pela **{{ provider_name }}**:*

| ITEM | DESCRIÇÃO TÉCNICA | QTD | PART-NUMBER / REF |
| :--- | :--- | :--- | :--- |
{% for hw in hardware_items -%}
| {{ loop.index }} | {{ hw.desc }} | {{ hw.qty }} | {{ hw.part }} |
{% endfor %}

{% elif detected_hardware %}
*Relação de ativos existentes na planta que serão monitorados/suportados:*

| ITEM | DESCRIÇÃO TÉCNICA | QTD | REF / PN |
| :--- | :--- | :--- | :--- |
{% for hw in detected_hardware -%}
| {{ loop.index }} | {{ hw.description }} | {{ hw.quantity }} | {{ hw.part_number }} |
{% endfor %}

{% else %}
*(A relação detalhada de ativos será validada durante a fase de Site Survey e Inventário Inicial)*
{% endif %}

### 10.7. Implantação de Infraestrutura de Monitoramento
O monitoramento é viabilizado pelo uso de um **Appliance próprio da EGE**, um recurso intrínseco à nossa prestação de serviço. Este dispositivo centraliza a telemetria de rede e servidores, permitindo o envio seguro de dados para a nossa central de operações (NOC) através de um link de contingência dedicado, garantindo a observabilidade mesmo em casos de indisponibilidade da rede principal do cliente.

## 11. VALIDAÇÃO E GOVERNANÇA DE SERVIÇOS
{% if custom_testing_protocol -%}
{{ custom_testing_protocol }}
{%- else -%}
A qualidade do serviço de sustentação é garantida por processos rigorosos de governança:
*   **Validação do Coletor Inicial:** Testes de comunicação e descoberta de ativos no ambiente local.
*   **Simulação de Incidentes:** Testes de alarmística para validar se as notificações chegam corretamente aos canais acordados.
*   **Reuniões de Status:** Revisão mensal de SLAs e apresentação de relatórios de disponibilidade.
*   **Operação NOC 24x7 e Suporte Especializado**: Ativação do serviço de monitoramento contínuo pela equipe NOC da EGE, com escalonamento N1/N2/N3 e acionamento do suporte técnico especializado conforme os SLAs definidos. Para garantir a eficácia do serviço, a EGE utiliza um **Appliance de Monitoramento e Suporte próprio (EGE RASA)**, desenvolvido especificamente para esta prestação de serviço, que atua como o coletor local de telemetria.
*   **Otimização Contínua e Relatórios**: Análise periódica dos dados coletados para identificar oportunidades de otimização de recursos e desempenho, com a entrega de relatórios mensais de performance e incidentes.
{%- endif %}

## 12. EQUIPE DE SUSTENTAÇÃO
{% if custom_team_structure -%}
{{ custom_team_structure }}
{%- else -%}
Alocaremos uma equipe multidisciplinar para o suporte ao contrato:
*   **Gestor de Conta Técnico:** Ponto focal para governança e escalonamento.
*   **Analistas de NOC:** Monitoramento 24x7 e resposta inicial a incidentes.
*   **Engenheiros N3:** Suporte avançado para resolução de problemas complexos de infraestrutura.
{%- endif %}

## 13. CRONOGRAMA DE IMPLANTAÇÃO DA SUSTENTAÇÃO
{% if custom_timeline -%}
{{ custom_timeline }}
{%- else -%}
A fase de transição para o modelo de sustentação segue a sequência:
*   **Fase 1 - Inventário (Semana 1):** Levantamento detalhado de ativos e gaps de documentação.
*   **Fase 2 - Instalação de Agentes (Semana 2):** Deploy do appliance de coleta e configuração de protocolos (SNMP, WMI).
*   **Fase 3 - Homologação (Semana 3):** Ajuste de limiares de alarme e validação de notificações.
*   **Fase 4 - Operação Plena (Semana 4):** Início oficial do faturamento mensal e monitoramento proativo.
{%- endif %}

## 14. TREINAMENTO DE OPERAÇÃO
{% if custom_training_md -%}
{{ custom_training_md }}
{%- else -%}
Forneceremos treinamento para a equipe da **{{ client_company }}** sobre o uso da plataforma de monitoramento:
*   **Portal de Visibilidade:** Como interpretar dashboards e relatórios de saúde.
*   **Canais de Acionamento:** Procedimentos para abertura de chamados e solicitações via central de tickets.
{%- endif %}

## 15. SUSTENTAÇÃO E MONITORAMENTO CONTÍNUO
Após a conclusão da implantação inicial, inicia-se a execução contínua dos serviços:
*   **Escopo:** Cobertura de todos os ativos acordados, com monitoramento proativo 24x7.
*   **Vigência:** 60 meses (5 anos).
*   **SLA:** Atendimento com tempos de resposta definidos conforme a severidade do incidente.
*   **Franquia:** Inclusão de franquia mensal de horas para atendimentos técnicos remotos e presenciais.

{% if asset_table_md or opex -%}
### 15.1. RELAÇÃO DE ATIVOS (CONSOLIDAÇÃO)
{% if asset_table_md -%}
{{ asset_table_md }}
{%- elif opex -%}
| Item Monitorado / Ativos | Quantidade |
| :--- | :---: |
{% for item in opex.items -%}
| {{ item.item_name }} | {{ item.quantity }} |
{% endfor %}
{%- endif %}
{%- endif %}
