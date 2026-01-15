Página 1 de 9

**Data de Emissão:** 22 de maio de 2024
**IT-20240522-01**
**IMPLEMENTAÇÃO DE DATACENTER E REDE INDUSTRIAL**

---

Página 2 de 9

Jundiaí, 22 de maio de 2024

À **Teste de Engenharia**.
Nome do projeto: **IMPLEMENTAÇÃO DE DATACENTER E REDE INDUSTRIAL**
N/ Ref.: Proposta Técnica – IT-20240522-01 – ver. A

Apresentado a: **Gestão de Projetos**

Prezado,

A **Industrial Tech S.A.** tem o prazer de submeter à **Teste de Engenharia** a proposta para prestação de serviços para Implementação de Datacenter e Rede Industrial a ser executado em suas instalações como um projeto Turnkey. A presente proposta foi elaborada visando atender às solicitações e expectativas de V.Sas. disponibilizadas até o presente momento.

A dúvida ou discordância com relação a qualquer item ou condição da presente proposta, bem como a nulidade de qualquer item da mesma não a invalida por completo, sendo que neste caso, pedimos que entrem em contato conosco para que possamos atender às suas necessidades.

Esperamos atender as vossas expectativas e permanecemos a seu inteiro dispor para quaisquer esclarecimentos que se façam necessários.

Atenciosamente,

**Senior AI Engineer**
Industrial Tech S.A.
E-mail: contato@industrialtech.com.br
Celular: + 55 11 99999-9999

---

Página 3 de 9

### 1. RESUMO EXECUTIVO
A **Industrial Tech S.A.** é especialista em engenharia, automação industrial e tecnologia, com vasta experiência em projetos de alto impacto. Atuamos com plataformas de gerenciamento da Indústria 4.0 e oferecemos soluções completas em energia, automação, segurança de dados e infraestrutura para indústria inteligente (Smart Industry).

**Por que escolher a Industrial Tech S.A.?**
*   Equipe técnica altamente qualificada com foco em ambientes críticos;
*   Metodologia de execução Turnkey para redução de gaps de comunicação;
*   Expertise em convergência IT/OT (Tecnologia da Informação e Tecnologia da Operação);
*   Compromisso com a mitigação de riscos e alta disponibilidade operacional.

Nosso compromisso é proporcionar a mitigação de riscos, aumentar a produtividade e reduzir custos operacionais através de metodologias práticas, certificadas e aplicadas com agilidade e eficácia.

### 2. AVISO
Neste documento podem aparecer nomes/marcas comerciais. A **Industrial Tech S.A.** usa esses nomes para fins de referência apenas, em benefício do proprietário da marca e sem qualquer intenção de violação de marca registrada.

---

Página 4 de 9

### 3. INFORMAÇÃO CONFIDENCIAL
Este documento reúne dados sigilosos e estratégicos da **Industrial Tech S.A.**, cuja divulgação a terceiros depende de autorização prévia, expressa e escrita da própria empresa.

Seu conteúdo está coberto pelos compromissos de confidencialidade vigentes entre **Industrial Tech S.A.** e **Teste de Engenharia**. Ao aceitá-lo, a **Teste de Engenharia** reconhece tratar-se de Informação Confidencial, resguardando este material com o mesmo grau de proteção que aplica aos seus próprios ativos confidenciais.

A preparação deste material baseou-se em elementos fornecidos pelo cliente. A **Industrial Tech S.A.** não responde por perdas ou danos decorrentes de inexatidões, omissões ou inconsistências nessas contribuições.

### 4. HISTÓRICO DE REVISÕES
Este documento foi preparado e revisado pelos seguintes responsáveis:
**Informações e condições comerciais:** Senior AI Engineer – Industrial Tech S.A.
**Solução técnica:** Equipe de Engenharia de Redes e Datacenter
**Revisão técnica:** Coordenação de Projetos TI/OT

### 5. LISTA DE REVISÕES
| VER. | DATA | POR | DESCRIÇÃO |
| :--- | :--- | :--- | :--- |
| A | 22/05/2024 | IT | ELABORAÇÃO DA PROPOSTA INICIAL |

---

Página 5 de 9

### 6. OBJETIVO GERAL
Este informativo tem como objetivo apresentar a **SOLUÇÃO "TURNKEY"** completa para a implementação da infraestrutura de Datacenter e Rede Industrial da **Teste de Engenharia**.

O foco do projeto é estabelecer um Cluster de Virtualização resiliente, realizar a migração de cargas de trabalho críticas e implantar uma topologia de rede industrial segura e de alta performance. A solução visa garantir máxima disponibilidade (N+1) para as operações, criando uma base escalável para as demandas da Indústria 4.0.

### 7. BENEFÍCIOS
A implementação da nossa solução integrada trará para a **Teste de Engenharia** uma transformação em sua capacidade operacional:

**CONFIABILIDADE**
*   **Alta Disponibilidade:** Arquitetura de cluster (N+1) que elimina pontos únicos de falha no processamento de dados.
*   **Resiliência de Rede:** Topologia em anel (MRP/DLR) nos switches core e acesso, garantindo convergência rápida em caso de falhas de link.
*   **Continuidade de Negócio:** Rotinas de backup e imutabilidade configuradas para proteção contra incidentes de dados.

**OPERACIONAIS**
*   **Visibilidade Total:** Infraestrutura de rede gerenciável facilitando o diagnóstico e reduzindo o tempo médio de reparo (MTTR).
*   **Padronização:** Documentação As-Built detalhada para facilitar futuras manutenções e expansões.

**FINANCEIROS E ESTRATÉGICOS**
*   **Proteção de Ativos:** Hardening e atualizações de firmware protegem os investimentos contra vulnerabilidades.
*   **Prontidão para o Futuro:** Base tecnológica preparada para integração de novas aplicações de IIoT e Big Data Analytics.

---

Página 6 de 9

### 8. VISÃO GERAL DA SOLUÇÃO PROPOSTA
Nossa abordagem consiste em um projeto integrado fundamentado em quatro pilares sequenciais:

1.  **Fundação e Cluster de Virtualização:** Instalação física, atualização e configuração de Hosts e Storage SAS para formar o núcleo de computação de alta disponibilidade.
2.  **Espinha Dorsal de Rede (Core e Acesso):** Implementação de switches Core L3 e Acesso L2 com segmentação de VLANs e protocolos de resiliência industrial.
3.  **Migração e Continuidade:** Planejamento e execução da migração P2V (Physical-to-Virtual) de 26 máquinas virtuais, assegurando a transição dos serviços com o mínimo de downtime.
4.  **Comissionamento e Governança:** Realização de testes de aceitação em campo (SAT), testes de resiliência e entrega de documentação técnica completa sob rigorosa gestão de projeto.

---

Página 7 de 9

### 9. ESCOPO TÉCNICO DETALHADO
Esta seção consolida os itens de serviço e as frentes de trabalho que serão executadas como parte desta solução "Turnkey".

**IMPLEMENTAÇÃO DE DATACENTER (VIRTUALIZAÇÃO)**
*   Recebimento, inspeção física e montagem de Hosts e Storage SAS.
*   Atualização de Firmware/BIOS e Hardening dos ativos.
*   Instalação e configuração de Hypervisor e Storage SAS.
*   Configuração de Cluster HA (High Availability) e Failover.
*   Implementação de rotinas de Backup e Imutabilidade de dados.

**REDE INDUSTRIAL (CORE E ACESSO)**
*   Instalação e configuração de 02 Switches Core L3.
*   Instalação e configuração de 08 Switches de Acesso L2.
*   Segmentação de VLANs e configuração de protocolos de redundância industrial (MRP/DLR).
*   Testes de resiliência e performance de rede.

**MIGRAÇÃO DE CARGAS DE TRABALHO**
*   Design e Planejamento da migração.
*   Migração de 26 Máquinas Virtuais (VMs) via técnica P2V (Windows e Linux).

**EXECUÇÃO E GOVERNANÇA**
*   Montagem física em Racks, incluindo infraestrutura e organização de cabos.
*   Testes de Aceitação em Campo (SAT) assistidos.
*   Documentação técnica final (As-Built).
*   Gestão de projeto com reuniões de Kick-off, Dailies e Status semanais.

*Nota: O hardware será fornecido pelo cliente, sendo a Industrial Tech S.A. responsável pela execução total dos serviços de engenharia e configuração.*

---

Página 8 de 9

### 10. INVESTIMENTO
O investimento total para a execução dos serviços descritos nesta proposta está consolidado no quadro abaixo.

**QUADRO RESUMO DE INVESTIMENTO**

| DESCRIÇÃO | VALOR TOTAL (R$) |
| :--- | :--- |
| **Hardware e Software (Fornecimento Cliente)** | **R$ 0,00** |
| **Serviços de Engenharia e Labor** | **R$ 100.548,00** |
| **Despesas de Deslocamento e Estadia** | **R$ 12.120,00** |
| **TOTAL DO INVESTIMENTO** | **R$ 112.668,00** |

**Considerações Comerciais:**
*   **Impostos:** Todos os impostos aplicáveis já estão inclusos nos valores acima.
*   **Validade da Proposta:** 15 dias a partir da data de emissão.
*   **Condições de Pagamento:** A definir conforme cronograma de medição de marcos contratuais.

---

Página 9 de 9

### 11. CRONOGRAMA E CONDIÇÕES GERAIS
O projeto está estimado para ser executado em um período de aproximadamente 8 semanas, seguindo o rigor das normas de segurança e qualidade da **Industrial Tech S.A.**.

**Responsabilidades da Teste de Engenharia:**
*   Disponibilização do hardware no local da instalação.
*   Acesso físico às áreas de intervenção e acesso lógico aos servidores e rede.
*   Acompanhamento das janelas de migração para validação das aplicações.

**Garantia:**
A **Industrial Tech S.A.** oferece garantia de 12 meses sobre os serviços de configuração e instalação realizados, contados a partir da assinatura do termo de encerramento do projeto.

Esperamos que esta proposta esteja em conformidade com suas necessidades e permanecemos à disposição para eventuais ajustes ou esclarecimentos técnicos.

**Industrial Tech S.A.**

---
*Gerado automaticamente pelo GPT-Md v1.1 em: 14/01/2026 23:52:32*