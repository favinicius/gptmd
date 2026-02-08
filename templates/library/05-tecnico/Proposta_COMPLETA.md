```
## 6. OBJETIVO GERAL
{% if custom_objective_md %}
{{ custom_objective_md }}
{% elif project_motivation %}
{{ project_motivation }}
{% else %}
Este informativo tem como objetivo apresentar a solução **Solução Integrada de TI** para a modernização da infraestrutura de TI Industrial da planta **{{ client_company }}** em {{ city }} - {{ state }}. O objetivo é implantar uma INFRASTRUTURA FÍSICA e uma nova REDE DE AUTOMAÇÃO segura e resiliente, garantindo máxima disponibilidade, performance e segurança para as operações críticas de manufatura, ao mesmo tempo em que se cria uma base escalável para as demandas da Indústria 4.0.
{% endif %}

## 7. BENEFÍCIOS
{% if custom_benefits_md %}
{{ custom_benefits_md }}
{% else %}
A implementação da nossa solução integrada trará para a {{ company_short_name }} uma transformação completa em sua capacidade operacional de TI/TA, gerando valor tangível em todas as frentes do negócio:

### CONFIABILIDADE
*   **Base Física Segura e Normalizada:** Mitigação de riscos de paradas por falhas elétricas ou de cabeamento, com uma infraestrutura projetada e executada em estrita conformidade com as normas técnicas (NBR 5410, NR10).
*   **Máxima Continuity de Negócio:** A arquitetura de cluster (N+1) e a rede em anel com recuperação rápida eliminam pontos únicos de falha, garantindo que a produção não seja interrompida por incidentes de infraestrutura.
*   **Segurança Industrial de Ponta a Ponta:** A segmentação da rede baseada no Modelo Purdue e a gestão centralizada de segurança (EDR, WSUS) reduzem drasticamente a superfície de ataque e alinham a planta aos padrões globais de cibersegurança (ISA/IEC 62443).

### OPERACIONAIS
*   **Facilidade de Manutenção e Expansão Futura:** Infraestrutura organizada e documentada, com caminhos de cabos e quadros elétricos que facilitam futuras manutenções e ampliações.
*   **Gestão Simplificada e Diagnóstico Rápido:** A centralização da infraestrutura em um ambiente virtualizado e uma rede totalmente gerenciável permite visibilidade total, otimizando a operação e reduzindo o tempo de resolução de incidentes (MTTR).

### FINANCEIROS
*   **Redução de Perdas por Paradas:** A alta disponibilidade da infraestrutura mitiga o risco de paradas de produção causadas por falhas, protegendo diretamente a receita e a eficiência da planta.
*   **Proteção do Investimento (ROI):** A solução maximiza o retorno sobre os ativos existentes (servidores e storage HPE) ao integrá-los em uma arquitetura moderna, evitando custos de substituição completa.
*   **Previsibilidade de Custos:** A consolidação do projeto e do suporte em um único parceiro, com um contrato de sustentação de 5 anos, transforma custos reativos e variáveis em um investimento fixo e previsível.

### ESTRATÉGICOS
*   **Plataforma à Prova de Futuro:** O dimensionamento da infraestrutura já contempla a projeção de crescimento de 50%, fornecendo uma base sólida, padronizada e escalável que suportará as necessidades da {{ company_short_name }} pelos próximos 5 anos.
*   **Liberação da Equipe Interna:** Nossa abordagem completa, do hardware à sustentação, permite que os valiosos especialistas da {{ company_short_name }} se dediquem a projetos de engenharia, melhoria de processos e inovação, em vez de tarefas operacionais de infraestrutura.
*   **Responsabilidade Técnica Assegurada:** Projeto assinado por engenheiro responsável, garantindo conformidade e segurança legal.
{%- endif %}

## 8. VISÃO GERAL DA SOLUÇÃO PROPOSTA
{% if custom_vision_md %}
## 8. METODOLOGIA E VISÃO DE PROJETO
{{ custom_vision_md }}
{% else %}
Nossa abordagem consiste em um projeto integrado de ponta a ponta, fundamentado em cinco pilares que se constroem sequencialmente para entregar uma solução robusta e sem preocupações para a {{ company_short_name }}:

1.  **Engenharia e Fundação Física:** Projeto, fornecimento e implantação da infraestrutura física de base, incluindo as instalações elétricas e de dados que servirão como alicerce para todos os novos ativos de TI.
2.  **Hardware e Conectividade:** Fornecimento, instalação e comissionamento de todo o hardware necessário, desde os componentes de upgrade dos servidores até a nova e resiliente infraestrutura de rede industrial.
3.  **Plataforma de Computação Centralizada:** Transformação dos servidores existentes em um cluster de virtualização de alta disponibilidade (N+1), com uma solução moderna de proteção de dados, formando o coração do novo Datacenter Industrial.
4.  **Ecossistema de Aplicações e Serviços:** Implementação completa da camada de software, incluindo os serviços essenciais de infraestrutura (AD, DNS, etc.) e a instalação e configuração de todo o conjunto de aplicações de automação da Rockwell.
5.  **Parceria e Sustentação de Longo Prazo:** Após a entrega do projeto, iniciamos uma parceria de 5 anos através de um serviço de monitoramento proativo e suporte técnico especializado 24x7.
{% endif %}

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
A infraestrutura de servidores e processamento é o motor da solução. Esta fase engloba a configuração de sistemas operacionais, ambientes de virtualização (se houver) e integração com o armazenamento centralizado, garantindo performance e disponibilidade.
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
{% if custom_testing_protocol %}
{{ custom_testing_protocol }}
{% else %}
Nosso compromisso com a qualidade é garantido por um protocolo de testes integrado que valida cada camada da solução.
*   **Validação da Infraestrutura Física:** Testes elétricos e validação de 100% dos pontos de rede e fibra com scanner.
*   **Validação de Hardware e Conectividade:** Testes de resiliência do anel de rede e validação de comunicação com as interfaces de gerenciamento.
*   **Validação da Infraestrutura:** Teste de failover do cluster de virtualização, simulando a falha de um host, e execução de um ciclo completo de backup e restauração de VMs críticas.
*   **Validação Funcional das Aplicações:** Testes de login, conectividade ponta-a-ponta entre servidores e dispositivos de campo, e verificação da redundância das aplicações Rockwell.
*   **Teste de Aceitação em Campo (SAT):** Execução de um roteiro consolidado de testes junto à equipe da {{ client_company }} para o aceite formal da solução completa.
{% endif %}

## 12. EQUIPE CHAVE E RESPONSABILIDADES
{% if custom_team_structure -%}
{{ custom_team_structure }}
{%- else -%}
Alocaremos uma equipe de projeto unificada e multidisciplinar para garantir uma execução coesa:
*   **Gerente de Projeto:** Focado no sucesso geral, cronograma e gestão de riscos.
*   **Engenheiro Responsável:** Liderança técnica de infraestrutura e gestão da equipe de campo.
*   **Arquiteto de Soluções:** Responsável pela arquitetura técnica integrada e conectividade entre frentes.
*   **Especialistas Técnicos:** Equipe composta por técnicos de redes, virtualização, elétrica e automação.
{%- endif %}

## 13. CRONOGRAMA SUGERIDO
{% if custom_timeline -%}
{{ custom_timeline }}
{%- else -%}
O cronograma macro será refinado no Kick-off, seguindo a sequência lógica estimada:
*   **Marco 1 - Entrevista de Expectativa:** Alinhamento inicial de requisitos e visão do cliente.
*   **Fase 1 - Planejamento:** Kick-off, Site Survey e finalização do projeto executivo.
*   **Fase 2 - Infraestrutura Física (Semanas 1-4):** Instalações elétricas e lançamento de cabos.
*   **Fase 3 - Implantação de TI (Semanas 5-9):** Instalação de hardware, configuração de redes e servidores.
*   **Fase 4 - Go-Live e Transição (Semanas 10-12):** Testes integrados, SAT e Operação Assistida.
{%- endif %}

## 14. TREINAMENTO E TRANSFERÊNCIA DE CONHECIMENTO
{% if custom_training_md -%}
{{ custom_training_md }}
{%- else -%}
Conforme solicitado, será fornecido um programa de treinamento formal e completo para as equipes da **{{ client_company }}**, cobrindo os três turnos operacionais e dividido em trilhas de conhecimento:
*   **Handover da Infraestrutura Física:** Apresentação dos equipamentos, organização dos racks e identificação dos ativos.
*   **Trilha de Operação de Infraestrutura de TI:** Visão Geral dos servidores, sistemas e solução de backup.
*   **Trilha de Operação e Engenharia de Redes:** Gestão da plataforma **{{ provider_short }}** e troubleshooting.
*   **Handover das Aplicações:** Sessões sobre a nova arquitetura das aplicações implementadas.
{%- endif %}

## 15. SUSTENTAÇÃO E MONITORAMENTO CONTÍNUO
Após a conclusão e aceite do projeto, inicia-se a nossa parceria de longo prazo, garantindo a tranquilidade e a saúde contínua do ambiente:
*   **Escopo:** Cobertura de todos os ativos de hardware e software de base implementados, com monitoramento proativo 24x7 e suporte técnico especializado.
*   **Vigência:** 60 meses (5 anos).
*   **SLA:** Atendimento com tempos de resposta definidos por severidade (N1, N2, N3), conforme RFQ.
*   **Franquia:** Inclusão de uma franquia mínima de 80 horas anuais para atendimentos técnicos.
*   **Governança:** Acesso a uma Central de Tickets, canais de atendimento emergenciais e a uma Plataforma de Monitoramento com visibilidade em tempo real para a {{ provider_short }}.

{% if opex -%}
### 15.1. RELAÇÃO DE ATIVOS (CONSOLIDAÇÃO)
| Item Monitorado / Ativos | Quantidade |
| :--- | :---: |
{% for item in opex.items -%}
| {{ item.item_name }} | {{ item.quantity }} |
{% endfor %}

{% if asset_table_md -%}
*Detalhamento Adicional de Ativos:*
{{ asset_table_md }}
{%- endif %}

{%- elif asset_table_md -%}
### 15.1. RELAÇÃO DE ATIVOS (CONSOLIDAÇÃO)
{{ asset_table_md }}
{%- endif %}