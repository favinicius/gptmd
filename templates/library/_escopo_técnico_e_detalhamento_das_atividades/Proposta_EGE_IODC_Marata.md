## 10. ESCOPO TÉCNICO E DETALHAMENTO DAS ATIVIDADES
Nossa metodologia de execução é dividida em fases lógicas que garantem uma implementação segura e controlada, desde a camada física até a aplicação.

### 10.1. Projeto, Fornecimento e Implantação de Infraestrutura
Esta fase cria o alicerce para todo o projeto.
*   **Projeto e Engenharia:** Levantamento em campo (Site Survey), elaboração de projeto executivo elétrico e de dados, com emissão de ART.
*   **Implantação e Montagem:**
    *   Instalação aérea da infraestrutura de caminhos (eletrocalhas, eletrodutos).
    *   Montagem dos quadros elétricos e lançamento dos circuitos de alimentação dedicados.
    *   Lançamento dos cabos de rede (Cat6A) e fibra óptica do Datacenter aos pontos de produção.
    *   Organização e identificação profissional de todos os componentes.

### 10.2. Instalação e Comissionamento Físico
Esta fase complementa a infraestrutura física com os equipamentos de TI.
*   Montagem dos racks de 44U (Datacenter) e 12U (Campo).
*   Instalação física ("Rack and Stack") de todos os equipamentos novos: switches, servidores (backup/NAS), no-breaks e DIOs.
*   Execução do upgrade de hardware (CPU, RAM, NICs, Risers, Fans) nos dois servidores HPE DL380 Gen10 Plus existentes.
*   Conexão e organização de todo o cabeamento de energia e dados.
*   Comissionamento básico com inicialização (Power-On), verificação de autotestes (POST), atualização de firmwares e configuração de acesso inicial às interfaces de gerenciamento (iLO, etc.).

{% if include_network %}
### 10.3. Implementação da Rede Industrial (OT)
Com o hardware no lugar, construímos a espinha dorsal de comunicação.
*   Conectorização do anel de fibra óptica.
*   Configuração dos switches Core L3 para prover roteamento inter-VLAN.
*   Configuração dos switches de acesso com as VLANs apropriadas para cada ponto.
*   Implementação do protocolo de recuperação rápida de anel MRP.
*   Criação das Zonas Funcionais (VLANs) mandatórias conforme o Modelo Purdue.
{% endif %}

### 10.4. Implementação da Infraestrutura de Datacenter
Sobre a rede resiliente, ativamos a plataforma de computação.
*   Instalação e configuração do software de virtualização (Hypervisor) nos hosts HPE.
*   Criação e configuração do cluster de alta disponibilidade (HA).
*   Configuração do zoning Fibre Channel e provisionamento de LUNs no storage HPE MSA 2060 existente.
*   Instalação e configuração completa da solução de backup, incluindo a criação das rotinas para o novo servidor NAS com imutabilidade.

### 10.5. Implementação e Migração de Aplicações
A fase final de implementação, entregando o valor de negócio ao usuário.
*   Provisionamento de todas as 26 máquinas virtuais no novo cluster.
*   Implementação completa dos serviços essenciais de infraestrutura (Active Directory, DHCP, DNS, WSUS, EDR, etc.).
*   Instalação, ativação e configuração de todo o conjunto de aplicações de automação Rockwell, incluindo a configuração de redundância (Master/Slave).
*   Execução do plano de migração para as VMs existentes ("AS-IS").