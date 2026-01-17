## 1. CONTEXTO: MODERNIZAÇÃO E CONTINUIDADE

A evolução da infraestrutura de servidores é vital para garantir que as aplicações críticas da **{{CLIENT_NAME}}** operem com a performance e segurança exigidas pelo negócio. O projeto **{{PROJECT_NAME}}** visa realizar uma migração estruturada (Upgrade/Refresh) do ambiente computacional atual, minimizando riscos e tempo de inatividade.

---

## 2. ESTRATÉGIA DE MIGRAÇÃO (JORNADA PARA O NOVO AMBIENTE)

Nossa metodologia de migração é dividida em fases claras para garantir total controle sobre os dados e serviços.

### 2.1. Fase 1: Levantamento e Planejamento (Assessment)
Nesta etapa inicial, realizaremos o mapeamento detalhado das cargas de trabalho atuais.

*   Mapeamento de dependências de aplicações.
*   Validação de compatibilidade de SO e Drivers com o novo hardware.
*   Definição de janelas de manutenção.

### 2.2. Fase 2: Preparação da Nova Infraestrutura (Landing Zone)
<!-- IA_DYNAMIC_BLOCK_START -->
# INSTRUÇÕES:
1. Descreva a preparação do novo hardware (Servidores, Storage) listado no `scope_json`.
2. Mencione a instalação do Hypervisor (VMware/Hyper-V/Proxmox) e configuração de Cluster HA.
3. Cite a configuração de redes virtuais (vSwitches) e Storage (LUNs/Datastores).
<!-- IA_DYNAMIC_BLOCK_END -->

### 2.3. Fase 3: Migração de Cargas (Move)
A migração efetiva dos dados e aplicações seguirá o método **{{MIGRATION_METHOD}}** (P2V, V2V, ou Reinstalação), conforme adequado para cada workload.

<!-- IA_DYNAMIC_BLOCK_START -->
# INSTRUÇÕES:
1. Explique como as VMs ou Dados serão movidos (ex: Ferramentas de Converter, Replicação, Restore de Backup).
2. Se houver menção a "Veeam" ou ferramentas específicas no contexto, cite-as.
3. Detalhe o procedimento de "Virada de Chave" (Cutover).
<!-- IA_DYNAMIC_BLOCK_END -->

---

## 3. PLANO DE ROLLBACK E CONTINGÊNCIA

A segurança da operação é nossa prioridade. Para cada janela de migração, estabelecemos um plano de retorno imediato ao ambiente legado caso sejam identificadas anomalias críticas, garantindo que a operação da **{{CLIENT_NAME}}** nunca fique desamparada.

---

## 4. NOVA ARQUITETURA DE HARDWARE (ESPECIFICAÇÕES)

O novo ambiente será sustentado pelos seguintes recursos dedicados:

<!-- IA_DYNAMIC_BLOCK_START -->
# INSTRUÇÕES:
1. Liste os servidores físicos (Hosts) e Storage do `scope_json`.
2. Detalhe CPU, RAM e Capacidade de Disco de cada host.
3. Formate como uma tabela ou lista técnica clara.
<!-- IA_DYNAMIC_BLOCK_END -->
