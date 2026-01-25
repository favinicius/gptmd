## 6. OBJETIVO GERAL
{% if project_motivation %}
{{ project_motivation }}
{% endif %}

Este informativo tem como objetivo apresentar a solução de **Migração de Aplicações Operacionais e Softwares de Automação** para a planta **{{ client_company }}** em {{ city }} - {{ state }}. O foco é realizar a TRANSIÇÃO lógica e segura de sistemas críticos (Historian, MES, Supervisórios e Serviços de Infraestrutura) para o novo ambiente, garantindo a integridade das configurações, o histórico de dados e a continuidade operacional, minimizando o impacto na produção durante o cutover.

## 7. BENEFÍCIOS
A migração estruturada de aplicações trará para a {{ company_short_name }} segurança e eficiência na transição digital:

### CONFIABILIDADE
*   **Integridade de Dados Assegurada:** Garantia de que históricos de processo e configurações críticas sejam preservados e validados no novo ambiente.
*   **Redução de Riscos de Cutover:** Metodologia de migração por fases (pilotagem) que permite validar a aplicação antes do desligamento definitivo do sistema legado.
*   **Padronização de Versões:** Alinhamento das aplicações às versões mais recentes suportadas pelo fabricante, garantindo suporte e patches de segurança.

### OPERACIONAIS
*   **Menor Downtime de Software:** Planejamento detalhado das janelas de interrupção, focando em manter a visibilidade do processo pelo maior tempo possível.
*   **Ambiente Otimizado:** Ajuste fino das aplicações para o novo hardware virtualizado, resultando em tempos de resposta mais rápidos e maior estabilidade.

### FINANCEIROS
*   **Custo de Parada Mitigado:** A transição suave reduz o risco de "startups" problemáticos após a migração, evitando perdas de produção.
*   **Extensão de Vida Útil do Legado:** Migração de aplicações de hardware obsoletos para plataformas modernas sem necessidade de reescrita total imediata.

### ESTRATÉGICOS
*   **Soberania Tecnológica:** Domínio total sobre as novas instâncias de software, com documentação atualizada e arquitetura resiliente.
*   **Prontidão para Dados:** Preparação da base de dados (Historian/MES) para futuras integrações com sistemas ERP ou plataformas de Analytics.

## 9. RELAÇÃO DE APLICAÇÕES E SOFTWARES NO ESCOPO
Esta seção consolida os sistemas que serão objeto da migração ou atualização.

{% if application_items %}
| SISTEMA | DESCRIÇÃO DA ATIVIDADE | VERSÃO ORIGEM | VERSÃO DESTINO |
| :--- | :--- | :--- | :--- |
{% for app in application_items -%}
| {{ app.name }} | {{ app.action }} | {{ app.source_ver }} | {{ app.target_ver }} |
{% endfor %}

{% else %}
*(A relação detalhada de softwares e bancos de dados será validada durante o levantamento lógico - Logical Survey)*

### CATEGORIAS DE SOFTWARE COBERTAS
*   **Serviços de Diretório:** Active Directory, DNS, DHCP.
*   **Aplicações de Automação:** FactoryTalk View, Studio 5000, AssetCentre.
*   **Gerenciamento de Dados:** SQL Server, Historian, InSQL.
*   **Proteção e Updates:** EDR, WSUS, Servidor de Antivírus.
{% endif %}

## 10. ESCOPO TÉCNICO E DETALHAMENTO DA MIGRAÇÃO LÓGICA
Diferente da migração física, a migração de aplicações foca na camada de software e interconectividade.

{% for pillar in structured_technical_scope %}
### 10.{{ pillar.id }}. {{ pillar.title }}
{% if pillar.id == 1 %}
O Planejamento Lógico foca no mapeamento de dependências entre softwares, usuários e bancos de dados, definindo a ordem crítica de migração para evitar quebras de serviço.
{% elif pillar.id == 2 %}
Preparação do Ambiente de Destino: Instalação de sistemas operacionais, pré-requisitos (Frameworks, IIS, Java) e configuração de instâncias de bancos de dados.
{% elif pillar.id == 3 %}
Migração de Dados e Backup: Extração de backups do sistema legado e restauração controlada no novo servidor, com verificação de checksum e compatibilidade.
{% elif pillar.id == 4 %}
Configuração de Licenciamento: Transferência de licenças de software, ativação de novos servidores de licença e validação de conformidade.
{% elif pillar.id == 5 %}
Validação de Comunicação Field-to-App: Testes de drivers de comunicação (OPC, RSLinx) para garantir que as aplicações no novo ambiente "enxerguem" os CLPs e dispositivos de campo.
{% elif pillar.id == 6 %}
Testes de Estresse e Carga: Validação da performance das aplicações sob condições reais de operação no novo ambiente virtualizado.
{% elif pillar.id == 7 %}
Cutover e Virada Definiva: Execução da janela final de migração, apontamento de clientes e desligamento seguro do sistema legado.
{% endif %}

{% for sub in pillar.sub_topics %}
*   **{{ sub.title }}**: {% if sub.summary %}{{ sub.summary }}{% else %}{% if sub.activities %}{% for activity in sub.activities -%}{{ activity }}{% if not loop.last %}; {% else %}.{% endif %}{% endfor %}{% endif %}{% endif %}
{% endfor %}

{% endfor %}

## 11. VALIDAÇÃO DE QUALIDADE (V&V)
*   **Teste de Integridade de Banco de Dados:** Comparação de registros e contagens entre origem e destino.
*   **Teste de Latência de Tela:** Verificação se o tempo de atualização dos supervisórios está dentro dos limites operacionais.
*   **Validação de Alarmística:** Garantia de que todos os alarmes críticos estão sendo reportados e registrados corretamente.
*   **Sinal de Vida (Heartbeat):** Verificação da comunicação contínua com dispositivos de campo durante 24h pós-migração.

## 13. CRONOGRAMA DE MIGRAÇÃO LÓGICA
*   **Semana 1:** Levantamento de Credenciais e Inventário de Aplicações.
*   **Semana 2-3:** Instalação e "Hardening" dos novos servidores (Staging).
*   **Semana 4-6:** Migração de dados e testes em ambiente paralelo.
*   **Semana 7:** Janela de Cutover (Virada) e Assistência na Produção.

## 15. SUPORTE PÓS-MIGRAÇÃO
Garantia de que quaisquer ajustes finos necessários após a entrada em produção sejam atendidos prioritariamente, assegurando que o novo ambiente de software opere com 100% de sua funcionalidade.
