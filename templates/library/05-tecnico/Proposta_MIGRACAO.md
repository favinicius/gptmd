## 6. OBJETIVO GERAL
{% if custom_objective_md %}
{{ custom_objective_md }}
{% else %}
{% if project_motivation %}
{{ project_motivation }}
{% endif %}

Este informativo tem como objetivo apresentar a solução de **Migração de Servidores e Datacenter** para a planta **{{ client_company }}** em {{ city }} - {{ state }}. O foco é realizar a MIGRAÇÃO segura e otimizada dos servidores e aplicações existentes para uma nova infraestrutura, garantindo a integridade dos dados, mínima inatividade e atualização tecnológica do ambiente operacional, ao mesmo tempo em que se cria uma base escalável para o crescimento futuro e as demandas da Indústria 4.0.
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
Esta seção consolida todos os ativos de hardware, software e acessórios que fazem parte desta solução. 

{% if hardware_items %}
{% set client_supplied = hardware_items[0].is_client_supplied %}
{% if client_supplied %}
*Nota: Conforme definido no escopo, o fornecimento físico do hardware será realizado pela **{{ client_company }}**, sendo a **{{ provider_name }}** responsável pela especificação técnica, dimensionamento e comissionamento dos itens abaixo:*
{% else %}
*Estes itens compõem o fornecimento turnkey da **{{ provider_name }}**:*
{% endif %}

| ITEM | DESCRIÇÃO TÉCNICA | QTD | PART-NUMBER / REF |
| :--- | :--- | :--- | :--- |
{% for hw in hardware_items -%}
| {{ loop.index }} | {{ hw.desc }} | {{ hw.qty }} | {{ hw.part }} |
{% endfor %}

{% else %}
*(A relação detalhada de equipamentos será validada durante a fase de projeto executivo e Site Survey)*

### COMPONENTES DE INFRAESTRUTURA FÍSICA
*   **Caminhos:** Eletrocalhas, leitos para cabos, eletrodutos.
*   **Elétrica:** Quadros de distribuição, disjuntores, cabos de energia, tomadas industriais.
*   **Dados:** Cabos de rede Categoria 6A SFTP, cabos de fibra óptica.
{% endif %}

### CABOS E ACESSÓRIOS
Todos os transceivers, cordões ópticos, cabos de rede Categoria 6A e acessórios necessários para a interconexão completa de todos os equipamentos.

### COMPONENTES DE SOFTWARE E LICENCIAMENTO
Os softwares necessários para a operação do ambiente (Hypervisors, Windows Server, Backup) estão listados conforme o dimensionamento do cluster.

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
Alocaremos uma equipe de projeto unificada e multidisciplinar para garantir uma execução coesa e eficiente, liderada por:
*   **Gerente de Projeto:** Ponto focal para o cliente, responsável pelo cronograma, comunicação, gestão de riscos e sucesso geral do projeto.
*   **Engenheiro Responsável:** Responsável técnico pelo projeto de infraestrutura física, planejamento e gestão da equipe de campo.
*   **Arquiteto de Soluções:** Responsável pela arquitetura técnica integrada e por garantir que todas as frentes de trabalho se conectem perfeitamente.
*   **Especialistas Técnicos:** Uma equipe composta por Eletricistas, Técnicos de Cabeamento, Engenheiros de Redes, Analistas de Infraestrutura e Virtualização, Especialistas em Automação Rockwell e Técnicos de Campo, cada um atuando em suas respectivas fases do projeto sob a coordenação do Gerente de Projeto.

## 13. CRONOGRAMA SUGERIDO
O cronograma macro do projeto será detalhado e refinado na reunião de kick-off. A sequência estimada de fases é:
*   **Fase 1 - Planejamento e Aquisição de Materiais:**
    *   Kick-off, Site Survey e finalização do projeto executivo. Esta fase ocorre em paralelo ao prazo de entrega (lead time) dos equipamentos.
*   **Fase 2 - Implantação da Infraestrutura Física (Semanas 1-4):**
    *   Montagem dos caminhos, instalações elétricas e lançamento de cabos.
*   **Fase 3 - Instalação e Configuração de TI (Semanas 5-9):**
    *   Instalação física do hardware.
    *   Configuração da Rede e do Datacenter.
    *   Provisionamento das VMs e serviços essenciais
    *   Testes integrados da infraestrutura.
*   **Fase 4 - Implementação de Aplicações e Migração (Semanas 10-11):**
    *   Instalação das aplicações Rockwell.
    *   Janelas de migração das VMs legadas.
*   **Fase 4 - Encerramento e Transição (Semana 12):**
    *   Execução do Teste de Aceitação Final (SAT).
    *   Operação Assistida (10 dias úteis).
    *   Treinamento, entrega da documentação e início do contrato de suporte.

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