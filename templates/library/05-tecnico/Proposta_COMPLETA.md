## 6. OBJETIVO GERAL
{% if custom_objective_md %}
{{ custom_objective_md }}
{% elif project_motivation %}
{{ project_motivation }}
{% else %}
Este informativo tem como objetivo apresentar a solução técnica para a modernização da infraestrutura de TI Industrial da planta {{ client_company }}. O foco é garantir máxima disponibilidade, performance e segurança para as operações críticas, criando uma base escalável para as demandas da Indústria 4.0.
{% endif %}

## 7. BENEFÍCIOS
{{ custom_benefits_md | default("A implementação da nossa solução trará para a **" ~ company_short_name ~ "** ganhos significativos em resiliência e eficiência:\n\n### CONFIABILIDADE\n*   **Continuidade de Negócio:** Arquitetura projetada para alta disponibilidade e mitigação de falhas.\n*   **Segurança Industrial:** Alinhamento com padrões de mercado para proteção de ativos críticos.\n\n### OPERACIONAIS\n*   **Manutenção Simplificada:** Infraestrutura organizada para facilitar diagnósticos e futuras expansões.") }}

## 8. VISÃO GERAL DA SOLUÇÃO PROPOSTA
{{ custom_vision_md | default("Nossa abordagem consiste em um projeto integrado fundamentado em pilares estratégicos que garantem a entrega de uma solução robusta, escalável e de fácil gestão para a **" ~ company_short_name ~ "**.") }}

## 9. RELAÇÃO DE EQUIPAMENTOS E SOFTWARES ESPECIFICADOS
Esta seção consolida os ativos de hardware, software e acessórios que fazem parte da solução proposta.

{% if (hardware_items and not hardware_items[0].is_client_supplied) %}
*Estes itens compõem o fornecimento turnkey da **{{ provider_name }}**:*

| ITEM | DESCRIÇÃO TÉCNICA | QTD | PART-NUMBER / REF |
| :--- | :--- | :--- | :--- |
{% for hw in hardware_items -%}
| {{ loop.index }} | {{ hw.desc }} | {{ hw.qty }} | {{ hw.part }} |
{% endfor %}

{% elif detected_hardware %}
*Relação de equipamentos extraída do contexto técnico (RFQ/Orçamento) para fornecimento pelo **Cliente/Terceiros** e validação pela nossa engenharia:*

| ITEM | DESCRIÇÃO TÉCNICA | QTD | REF / PN |
| :--- | :--- | :--- | :--- |
{% for hw in detected_hardware -%}
| {{ loop.index }} | {{ hw.description }} | {{ hw.quantity }} | {{ hw.part_number }} |
{% endfor %}

{% elif hardware_items %}
*Conforme definido no escopo, o fornecimento físico do hardware será realizado pela **{{ client_company }}** (ou terceiros), listamos abaixo os itens calculados para referência:*

| ITEM | DESCRIÇÃO TÉCNICA | QTD | PART-NUMBER / REF |
| :--- | :--- | :--- | :--- |
{% for hw in hardware_items -%}
| {{ loop.index }} | {{ hw.desc }} | {{ hw.qty }} | {{ hw.part }} |
{% endfor %}

{% else %}
*(A relação detalhada de equipamentos será validada durante a fase de projeto executivo e Site Survey)*
{% endif %}

### CABOS E ACESSÓRIOS
{{ custom_cabling_md | default("Incluso o fornecimento de transceivers, cordões e acessórios para a interconexão de todos os equipamentos." if not hardware_supply_by_client else "O fornecimento de transceivers, cordões e acessórios de conectividade é de responsabilidade da **" ~ client_company ~ "**, conforme premissa de hardware.") }}

### COMPONENTES DE SOFTWARE E LICENCIAMENTO
{{ custom_software_md | default("Incluso o licenciamento necessário para a operação plena da solução proposta." if not hardware_supply_by_client else "O licenciamento de software e sistemas operacionais é de responsabilidade da **" ~ client_company ~ "**.") }}

## 10. ESCOPO TÉCNICO E DETALHAMENTO DAS ATIVIDADES
Nossa metodologia de execução é dividida em blocos lógicos que garantem uma implementação segura e controlada, desde o design até a observabilidade final.

{% for pillar in structured_technical_scope %}
### 10.{{ pillar.id }}. {{ pillar.title }}
{% if pillar.id == 1 %}
As atividades de design contemplam o levantamento detalhado das necessidades de negócio e a tradução destas em especificações técnicas de baixo nível (LLD), garantindo que a implantação siga as melhores práticas de arquitetura e segurança.
{% elif pillar.id == 2 %}
A fundação física é o alicerce de toda a solução. Esta fase engloba a montagem mecânica, a organização do rack, o fornecimento de energia estabilizada e o cabeamento estruturado, garantindo um ambiente limpo, identificado e normalizado.
{% elif pillar.id == 3 %}
A camada de conectividade core estabelece o "backbone" de comunicação da planta. Os switches core são configurados para alta performance, resiliência e segmentação de tráfego, servindo como o nó central de distribuição de dados.
{% elif pillar.id == 4 %}
O cluster de virtualização é o motor de processamento da solução. Concentra os hosts físicos em um pool de recursos redundante, onde as máquinas virtuais operam com failover automático e balanceamento dinâmico de carga.
{% elif pillar.id == 5 %}
A estratégia de backup garante a proteção contra perda de dados. Implementamos rotinas automatizadas, armazenamento dedicado e validação de restauração, assegurando que o ambiente possa ser recuperado rapidamente em caso de falha.
{% elif pillar.id == 6 %}
O firewall atua como o guardião do perímetro e da segmentação interna. As políticas de acesso são configuradas para proteger os ativos industriais contra ameaças externas e controlar estritamente o tráfego entre zonas de segurança (Purdue).
{% elif pillar.id == 7 %}
O appliance de monitoramento centraliza a visibilidade da saúde de todo o ecossistema. Através de hardware dedicado, coletamos telemetria crítica de servidores, redes e aplicações para identificação proativa de anomalias.
{% elif pillar.id == 8 %}
A camada de orquestração Kubernetes provê um ambiente moderno para as aplicações MES e serviços conteinerizados. Esta fase foca na estabilidade, gestão de pods e conectividade segura para as aplicações de manufatura.
{% elif pillar.id == 9 %}
A observabilidade avançada entrega o valor analítico do monitoramento. Dashboards visuais e alarmística inteligente permitem que a equipe de operação tome decisões baseadas em dados reais sobre a performance da planta.
{% endif %}

{% for sub in pillar.sub_topics %}
*   **{{ sub.title }}**: {% if sub.summary %}{{ sub.summary }}{% else %}{% if sub.activities %}{% for activity in sub.activities -%}{{ activity }}{% if not loop.last %}; {% else %}.{% endif %}{% endfor %}{% endif %}{% endif %}
{% endfor %}
{% if not pillar.sub_topics %}
*(Atividades desta fase serão detalhadas conforme os pré-requisitos detectados no Site Survey)*
{% endif %}

{% endfor %}

## 11. TESTES, VALIDAÇÕES E COMISSIONAMENTO
{{ custom_testing_protocol | default("Nosso compromisso com a qualidade é garantido por um protocolo de testes integrado que valida cada camada da solução.") }}

## 12. EQUIPE CHAVE E RESPONSABILIDADES
{{ custom_team_structure | default("Alocaremos uma equipe de projeto unificada e multidisciplinar para garantir uma execução coesa e eficiente.") }}

## 13. CRONOGRAMA SUGERIDO
{{ custom_timeline | default("O cronograma macro do projeto será detalhado e refinado na reunião de kick-off.") }}

## 14. TREINAMENTO E TRANSFERÊNCIA DE CONHECIMENTO
Conforme solicitado, será fornecido um programa de treinamento formal e completo para as equipes da **{{ client_company }}**, cobrindo os três turnos operacionais e dividido em trilhas de conhecimento:
*   **Handover da Infraestrutura Física:** Apresentação dos quadros elétricos, organização dos racks e identificação dos pontos.
*   **Trilha de Operação de Infraestrutura de TI:** Visão Geral do cluster de virtualização e da solução de backup.
*   **Trilha de Operação e Engenharia de Redes:** Gestão da plataforma **{{ provider_short }}** e troubleshooting.
*   **Handover das Aplicações:** Sessões sobre a nova arquitetura das aplicações **{{ provider_short }}**.

## 15. SUSTENTAÇÃO E MONITORAMENTO CONTÍNUO
Após a conclusão e aceite do projeto, inicia-se a nossa parceria de longo prazo, garantindo a tranquilidade e a saúde contínua do ambiente:
*   **Escopo:** Cobertura de todos os ativos de hardware e software de base implementados, com monitoramento proativo 24x7 e suporte técnico especializado.
*   **Vigência:** 60 meses (5 anos).
*   **SLA:** Atendimento com tempos de resposta definidos por severidade (N1, N2, N3), conforme RFQ.
*   **Franquia:** Inclusão de uma franquia mínima de 80 horas anuais para atendimentos técnicos.
*   **Governança:** Acesso a uma Central de Tickets, canais de atendimento emergenciais e a uma Plataforma de Monitoramento com visibilidade em tempo real para a {{ provider_short }}.