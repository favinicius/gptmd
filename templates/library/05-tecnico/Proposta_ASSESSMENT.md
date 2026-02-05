# OBJETIVO GERAL DO ASSESSMENT
{% if project_motivation %}
{{ project_motivation }}
{% endif %}

Este documento descreve a oferta técnica para a realização de um **ASSESSMENT TÉCNICO E CONSULTIVO** para a planta **{{ client_company }}**. O objetivo central é a **investigação profunda** da infraestrutura atual (As-Is), através de levantamentos em campo, auditoria de ativos e validação de topologias, sem intervenções de instalação de novos equipamentos ou alterações produtivas.

# BENEFÍCIOS DO DIAGNÓSTICO
A realização deste Assessment trará para a **{{ client_company }}** uma visão clara e detalhadada de sua infraestrutura:

### VISIBILIDADE E CONTROLE
*   **Inventário Ativo e Atualizado:** Identificação precisa de cada componente da rede (CLPs, IHMs, Switches), incluindo Part Numbers, versões de firmware e status de ciclo de vida.
*   **Documentação As-Is Confiável:** Entrega de diagramas de rede e topologias físicas/lógicas que refletem a realidade atual da planta, facilitando troubleshooting e expansões.

### SEGURANÇA E CONFORMIDADE
*   **Detecção de Vulnerabilidades:** Identificação de falhas de configuração, protocolos obsoletos ou brechas de segurança física na infraestrutura.
*   **Análise de Riscos Operacionais:** Diagnóstico de condições físicas de instalação e caminhos de cabos que possam representar riscos de parada não planejada.

### PLANEJAMENTO ESTRATÉGICO
*   **Suporte à Tomada de Decisão:** Dados concretos para embasar futuros investimentos em modernização e segurança.
*   **Otimização de Manutenção:** Melhoria no tempo médio de reparo (MTTR) através do conhecimento detalhado da conectividade porta-a-porta.

# VISÃO GERAL DA INVESTIGAÇÃO
Nosso trabalho de Assessment é fundamentado em quatro fases investigativas:

1.  **Levantamento Físico de Campo:** Inspeção visual detalhada de painéis, máquinas e caminhos de cabos para catalogação de ativos e condições físicas.
2.  **Auditoria de Conectividade:** Desconexão controlada e teste de cabos para validação de porta de origem/destino e mapeamento de topologia (especialmente em switches não gerenciáveis).
3.  **Coleta de Configurações (Running Configs):** Acesso e avaliação de configurações de switches, servidores e ativos de rede (quando disponível).
4.  **Consolidação e Relatório:** Análise de todos os dados coletados para elaboração do Relatório Diagnóstico Final e Diagramas.

# ATIVOS SOB ANÁLISE (INVENTÁRIO ESTIMADO)
Abaixo, relacionamos a carga de trabalho estimada baseada nos ativos informados para investigação:

| CATEGORIA | DESCRIÇÃO DOS ATIVOS | QTD ESTIMADA |
| :--- | :--- | :---: |
{% for hw in detected_hardware -%}
| {{ hw.category | default("Hardware") }} | {{ hw.description }} | {{ hw.quantity }} |
{% endfor %}

# ESCOPO TÉCNICO E DETALHAMENTO DA CARGA DE TRABALHO
As atividades abaixo representam o esforço de engenharia e consultoria para o diagnóstico:

{% for pillar in structured_technical_scope %}
### 10.{{ pillar.id }}. {{ pillar.title }}
{% for sub in pillar.sub_topics %}
*   **{{ sub.title }}**: {% if sub.summary %}{{ sub.summary }}{% else %}{% if sub.activities %}{% for activity in sub.activities -%}{{ activity }}{% if not loop.last %}; {% else %}.{% endif %}{% endfor %}{% endif %}{% endif %}
{% endfor %}
{% endfor %}

# METODOLOGIA DE INVESTIGAÇÃO TÉCNICA
Nosso protocolo em dupla (Analista + Técnico) garante a integridade dos dados coletados:
*   **Investigação Porta-a-Porta em Dupla**: Enquanto um técnico realiza o rastreamento físico e testes de continuidade, o analista valida a conectividade lógica e registra o inventário em tempo real.
*   **Protocolo de Não-Interferência:** Toda auditoria lógica é realizada de forma passiva ou em janelas autorizadas pela produção.
*   **Certificação Instrumentada**: Utilização de equipamentos certificados (ex: Fluke DSX) para garantir que a camada física suporta o tráfego industrial atual.

# EQUIPE DE INVESTIGAÇÃO
Alocaremos uma squad multidisciplinar especializada para o Assessment:
*   **Engenheiro Sênior:** Responsável pela revisão técnica final, validação do Databook e conformidade normativa.
*   **Analista de Sistemas Industrial:** Liderança de campo, responsável pela auditoria lógica, inventário de ativos e consolidação de documentos.
*   **Técnico de Infraestrutura:** Suporte em campo para rastreamento físico, testes de continuidade e identificação de cabos.
