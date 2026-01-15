Página 1 de 15

**Data de Emissão:** 15/05/2024  
**D24050190 – CONSULTORIA, FORNECIMENTO E IMPLEMENTAÇÃO DE IODC E DISASTER RECOVERY – UNIDADE ILHÉUS**

---

Página 2 de 15  
Jundiaí, 15 de maio de 2024  

À **OFI - OLAM Foods Ingredients S.A.**  
**Att.: Gilmar Corrêa**  
**Nome do projeto:** CONSULTORIA, FORNECIMENTO E IMPLEMENTAÇÃO DE IODC E DISASTER RECOVERY – UNIDADE ILHÉUS  
**N/ Ref.:** Proposta Técnica – D24050190 – ver. A  

Prezado Gilmar Corrêa,

A **EGE Soluções Industriais** tem o prazer de submeter à **OFI - OLAM Foods Ingredients S.A.** a proposta para prestação de serviços de Consultoria, Fornecimento e Implementação do Industrial Operations Data Center (IODC) e solução de Disaster Recovery (DR), a ser executado na planta localizada em Ilhéus (BA) como um projeto Turnkey.

A presente proposta foi elaborada visando atender às solicitações e expectativas de V.Sas. disponibilizadas até o presente momento, com foco especial na resiliência operacional e na proteção contra perda de dados através de repositórios imutáveis e redundância geográfica (DR).

A dúvida ou discordância com relação a qualquer item ou condição da presente proposta, bem como a nulidade de qualquer item da mesma não a invalida por completo, sendo que neste caso, pedimos que entrem em contato conosco para que possamos atender às suas necessidades.

Esperamos atender as vossas expectativas e permanecemos a seu inteiro dispor para quaisquer esclarecimentos que se façam necessários.

Atenciosamente,

**Roberto Pereira**  
EGE Soluções Industriais  
E-mail: roberto.pereira@egesolucoes.com.br  
Celular: + 55 11 99300-7143

---

Página 3 de 15  

### 1. RESUMO EXECUTIVO  
A EGE Soluções Industriais é especialista em engenharia, automação industrial e tecnologia, com mais de 20 anos de experiência em projetos de alto impacto. Atuamos com plataformas de gerenciamento da Indústria 4.0 e oferecemos soluções completas em energia, automação, segurança de dados e pessoas, sustentabilidade e indústria inteligente (Smart Industry).

**Por que escolher a EGE?**  
*   • +20 anos de experiência em projetos industriais;  
*   • Equipe com certificações NR10, NR12, ISO 50001 e CREA ativo;  
*   • Cases de sucesso em modernização de infraestrutura crítica para o setor de alimentos e ingredientes;  
*   • Atendimento técnico de excelência e suporte especializado em redes industriais (OT).

Nosso compromisso é proporcionar a mitigação de riscos, aumentar a produtividade e reduzir custos operacionais através de metodologias práticas, certificadas e aplicadas com agilidade e eficácia.

### 2. AVISO  
Neste documento podem aparecer nomes/marcas comerciais. A EGE Soluções Industriais usa esses nomes para fins de referência apenas, em benefício do proprietário da marca e sem qualquer intenção de violação de marca registrada.

---

Página 4 de 15  

### 3. INFORMAÇÃO CONFIDENCIAL  
Este documento reúne dados sigilosos e estratégicos da EGE, cuja divulgação a terceiros depende de autorização prévia, expressa e escrita da própria EGE.

Seu conteúdo está coberto pelos compromissos de confidencialidade vigentes entre EGE e OFI. Ao aceitá-lo, a OFI reconhece tratar-se de Informação Confidencial da EGE, excetuando-se apenas o que já tenha sido anteriormente disponibilizado a Gilmar Corrêa. A OFI deve resguardar este material com, no mínimo, o mesmo grau de proteção que aplica aos seus próprios ativos confidenciais.

A preparação deste material baseou-se em elementos fornecidos pela OFI. A EGE não responde por perdas ou danos decorrentes de inexatidões, omissões ou inconsistências nessas contribuições. Caso venha a ser firmado contrato com fundamento neste conteúdo, ajustes de escopo necessários em razão de dados incorretos ou incompletos apresentados pela OFI poderão implicar revisões de prazos.

### 4. HISTÓRICO DE REVISÕES  
Este documento foi preparado e revisado pelos seguintes responsáveis:  
**Informações e condições comerciais:** Roberto Pereira – Comercial  
**Solução técnica:** André Mendes – Coordenador Projetos  
**Revisão técnica:** Fábio Bezerra – Diretor TI  

### 5. LISTA DE REVISÕES  
| VER. | DATA | POR | DESCRIÇÃO |
| :--- | :--- | :--- | :--- |
| A | 15/05/2024 | AM | ELABORAÇÃO DA PROPOSTA INICIAL |

---

Página 5 de 15  

### 6. OBJETIVO GERAL  
Este informativo tem como objetivo apresentar a **SOLUÇÃO "TURNKEY"** completa para a implementação do Industrial Operations Data Center (IODC) e sistema de Disaster Recovery (DR) da planta **OFI - OLAM Foods Ingredients S.A.** em Ilhéus.

O objetivo central é estabelecer uma infraestrutura de virtualização robusta baseada em **Microsoft Hyper-V**, garantindo a continuidade do negócio através de um site de DR (Disaster Recovery), protegendo as aplicações críticas de manufatura (SCADA/MES/PIMS) com backup imutável e alta disponibilidade (HA), alinhando a planta às melhores práticas de TI Industrial e Indústria 4.0.

### 7. BENEFÍCIOS  
A implementação da nossa solução integrada trará para a OFI uma transformação completa em sua capacidade operacional de TI/TA, gerando valor tangível em todas as frentes do negócio:

**BENEFÍCIOS: CONFIABILIDADE**  
*   **Resiliência Geográfica (DR):** A inclusão de um terceiro host dedicado para Disaster Recovery garante que, mesmo em caso de falha total do cluster principal, as operações críticas possam ser restauradas com o mínimo de impacto.  
*   **Imutabilidade de Dados:** A solução de backup com repositório imutável protege a planta contra ataques de Ransomware, garantindo que os backups não possam ser alterados ou deletados indevidamente.  
*   **Continuidade de Negócio (N+1):** A arquitetura de cluster Hyper-V elimina pontos únicos de falha no processamento, garantindo que a produção não pare por falhas de hardware de servidor.

---

Página 6 de 15  

**BENEFÍCIOS: OPERACIONAIS**  
*   **Visibilidade e Controle:** A centralização das aplicações industriais em um IODC permite uma gestão simplificada e um diagnóstico de falhas muito mais ágil (redução do MTTR).  
*   **Padronização de Aplicações:** A estruturação de VMs base para sistemas SCADA, MES e PIMS facilita a replicação de ambientes e a manutenção de softwares industriais.  
*   **Gestão de Backup Centralizada:** Automatização completa das rotinas de proteção de dados, eliminando falhas humanas em processos de salvaguarda.

**BENEFÍCIOS: FINANCEIROS**  
*   **Mitigação de Downtime:** A redução drástica do risco de paradas de produção por falha de infraestrutura protege diretamente a margem operacional da unidade de Ilhéus.  
*   **Eficiência de Hardware:** A virtualização permite o máximo aproveitamento dos recursos de hardware adquiridos, reduzindo o custo total de propriedade (TCO).  
*   **Previsibilidade de Investimento:** Através do modelo Turnkey, a OFI tem clareza total dos custos de implementação, sem surpresas com aditivos de mobilização ou logística.

**BENEFÍCIOS: ESTRATÉGICOS**  
*   **Conformidade Global:** Alinhamento da unidade de Ilhéus com os padrões de cibersegurança industrial do grupo OLAM global.  
*   **Escalabilidade:** Infraestrutura pronta para suportar o crescimento das aplicações digitais de fábrica pelos próximos anos.  
*   **Responsabilidade Técnica Assegurada:** Projeto assinado por engenheiros especialistas, com emissão de ART, garantindo conformidade legal e normativa.

---

Página 7 de 15  

### 8. VISÃO GERAL DA SOLUÇÃO PROPOSTA  
Nossa abordagem consiste em um projeto integrado de ponta a ponta, fundamentado em cinco pilares que se constroem sequencialmente:

1.  **Fase de Planejamento e Design:** Detalhamento técnico exaustivo (Planbook) para validação de todas as premissas de rede, armazenamento e virtualização antes do início das atividades de campo.  
2.  **Infraestrutura de Computação e Armazenamento:** Fornecimento e configuração de hosts de alta performance e Storage dedicado, garantindo a performance necessária para aplicações industriais latentes.  
3.  **Conectividade OT Dedicada:** Implementação de uma rede de switches industriais de alta velocidade para interconexão do cluster e tráfego de dados de automação (IACS).  
4.  **Virtualização e Disponibilidade:** Criação do ambiente Microsoft Hyper-V Cluster em modo HA e configuração do site de Disaster Recovery.  
5.  **Proteção de Dados Industrial:** Implementação de servidores de backup e NAS para repositório imutável, fechando o ciclo de segurança da informação industrial.

### 9. RELAÇÃO DE EQUIPAMENTOS E SOFTWARES FORNECIDOS  
Esta seção consolida os ativos de hardware, software e acessórios que serão fornecidos e/ou implementados como parte desta solução "Turnkey".

**COMPONENTES DE DATACENTER E VIRTUALIZAÇÃO**  
*   03 x Servidores (Hosts) de Alta Performance para Cluster de Virtualização e DR.  
*   01 x Storage de Alto Desempenho (conforme seção 6.2 do pré-projeto).  
*   01 x Servidor de Backup dedicado para gestão de proteção de dados.  
*   01 x Unidade NAS para Repositório Imutável de longo prazo.  

**COMPONENTES DE REDE INDUSTRIAL**  
*   02 x Switches de Rede Dedicados para interconexão IACS/Cluster.  
*   Transceivers SFP+, Cordões Ópticos e Patch Cords de alto desempenho.  

**SOFTWARE E LICENCIAMENTO**  
*   Licenciamento Microsoft Windows Server para Hyper-V Cluster.  
*   Software de Backup e Replicação com suporte a imutabilidade.  
*   Licenciamento para interfaces de gerenciamento e monitoramento.  

---

Página 8 de 15  

### 10. ESCOPO TÉCNICO E DETALHAMENTO DAS ATIVIDADES  

#### 10.1. Fase de Planejamento (Definição, Planbook e Cronograma)  
Fase inicial mandatória de 30 dias para detalhamento técnico.  
*   Realização de Site Survey detalhado na Unidade Ilhéus.  
*   Elaboração do Plano de Configuração (Planbook) incluindo endereçamento IP, VLANs e naming convention.  
*   Definição da estratégia de migração de aplicações existentes para o novo ambiente virtual.  
*   Validação do design técnico junto à diretoria e equipe de TI/TA da OFI.  

#### 10.2. Implantação Física e Comissionamento de Hardware  
*   Recebimento, desembalagem e inspeção física de todos os ativos no site.  
*   Montagem em rack (Rack and Stack) dos servidores, storage, switches e unidades de backup.  
*   Atualização de Firmwares/BIOS e execução de Hardening de segurança inicial em nível de hardware.  
*   Organização de cabeamento lógico e elétrico dentro dos gabinetes (Cable Management).  
*   Trâmites de acesso e permissões SHE (Safety, Health and Environment) para equipe técnica.

#### 10.3. Implementação da Rede Industrial (IODC)  
*   Configuração dos switches core de rede dedicados para o ambiente industrial.  
*   Implementação e segmentação de VLANs conforme o modelo Purdue.  
*   Configuração de protocolos de resiliência (MRP/DLR) para garantir a conectividade ininterrupta.  
*   Testes de performance de backplane e latência de rede entre hosts e storage.

#### 10.4. Cluster de Virtualização e Disaster Recovery  
*   Instalação e configuração do Hypervisor (Microsoft Hyper-V) nos 3 hosts.  
*   Configuração do Cluster de Alta Disponibilidade (HA) e Failover.  
*   Implementação do host de DR em localidade distinta (conforme plano físico da planta).  
*   Configuração de Storage Zoning e provisionamento de volumes (LUNs) para as VMs.

#### 10.5. Implementação de Aplicações e Backup  
*   Provisionamento de máquinas virtuais (VMs) para Infraestrutura (AD/DNS), Sistemas Industriais (SCADA/MES) e Suporte.  
*   Instalação e configuração de aplicações funcionais industriais descritas no escopo.  
*   Configuração das rotinas de backup com política de imutabilidade no NAS dedicado.  
*   Configuração da replicação de máquinas virtuais entre o cluster principal e o host de DR.

---

Página 9 de 15  

### 11. TESTES, VALIDAÇÕES E COMISSIONAMENTO  
Nosso protocolo de testes garante a entrega de um ambiente operando em sua máxima performance:  
*   **Validação de Failover:** Teste real de desligamento de um host para validar a migração automática de VMs sem interrupção do serviço.  
*   **Teste de DR:** Simulação de desastre para validação do tempo de recuperação (RTO) e ponto de recuperação (RPO) no site de Disaster Recovery.  
*   **Validação de Imutabilidade:** Teste de tentativa de exclusão de backup para garantir a proteção contra ataques cibernéticos.  
*   **SAT (Site Acceptance Test):** Execução de roteiro de testes assistido junto à equipe da OFI para assinatura do termo de aceite.  
*   **Documentação As-Built:** Entrega de toda a documentação técnica atualizada, diagramas de rede e manuais de operação.

### 12. EQUIPE CHAVE E RESPONSABILIDADES  
Alocaremos uma equipe multidisciplinar para garantir a execução em Ilhéus:  
*   **Gestor de Projeto:** Responsável pela governança, reuniões de status semanais e dailies.  
*   **Engenheiro de Sistemas:** Responsável pelo design de alta disponibilidade e configuração de storage/cluster.  
*   **Analista de Infraestrutura:** Responsável pelo setup de VMs, backups e serviços de rede.  
*   **Técnicos de Campo:** Responsáveis pela montagem física, cabeamento e logística de hardware.

### 13. RESUMO DO INVESTIMENTO  

O investimento para a implementação completa da solução "Turnkey" (Serviços e Logística) está consolidado abaixo:

| Item | Descrição | Valor Total |
| :--- | :--- | :--- |
| 1 | **Serviços Profissionais e Engenharia** | R$ 168.375,00 |
| 2 | **Plano Logístico e Despesas de Mobilização (Ilhéus/BA)** | R$ 101.106,00 |
| **TOTAL** | **INVESTIMENTO TOTAL DO PROJETO** | **R$ 269.481,00** |

**Condições Gerais:**  
*   **Impostos:** Inclusos conforme legislação vigente.  
*   **Validade da Proposta:** 15 dias.  
*   **Cronograma Estimado:** Conforme definido no Plano de Planejamento (T-01).  

Esperamos que esta proposta esteja de acordo com suas necessidades.

Atenciosamente,

**EGE Soluções Industriais**

---
*Gerado automaticamente pelo GPT-Md v1.1 em: 15/01/2026 09:15:59*