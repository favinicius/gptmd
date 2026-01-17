## 10.4. Implementação da Infraestrutura de Datacenter

Sobre a rede resiliente, ativamos a plataforma de computação.

[TAG: DIAGRAMA_ARQUITETURA_DATACENTER_OT]

*   Instalação e configuração do software de virtualização (Hypervisor) nos hosts {{ company_name }}.
*   Criação e configuração do cluster de alta disponibilidade (HA).
*   Configuração do zoning Fibre Channel e provisionamento de LUNs no storage {{ company_name }} MSA 2060 existente.
*   Instalação e configuração completa da solução de backup, incluindo a criação das rotinas para o novo servidor NAS com imutabilidade.