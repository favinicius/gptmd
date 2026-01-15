---

# PROPOSTA TÉCNICA E COMERCIAL

**Página 1 de 12**

**Data de Emissão:** 23/10/2023  
**Ref.:** OFI-241023-01  
**PROJETO:** MIGRAÇÃO DE DATACENTER INDUSTRIAL – COCA-COLA

---

**Página 2 de 12**

Jundiaí, 23 de outubro de 2023

À **COCA-COLA**.  
**Nome do projeto:** MIGRAÇÃO DE DATACENTER INDUSTRIAL  
**N/ Ref.:** Proposta Técnica – OFI-241023-01 – ver. A  
**Apresentado a:** Gestão de Infraestrutura TI/OT  

Prezado,

A **OFI** tem o prazer de submeter à **COCA-COLA** a proposta para prestação de serviços para **Migração de Datacenter Industrial**, a ser executado conforme as premissas de modernização e alta disponibilidade. A presente proposta foi elaborada visando atender às solicitações e expectativas de V.Sas. disponibilizadas até o presente momento.

A dúvida ou discordância com relação a qualquer item ou condição da presente proposta, bem como a nulidade de qualquer item da mesma não a invalida por completo, sendo que neste caso, pedimos que entrem em contato conosco para que possamos atender às suas necessidades.

Esperamos atender as vossas expectativas e permanecemos a seu inteiro dispor para quaisquer esclarecimentos que se façam necessários.

Atenciosamente,

**Equipe de Engenharia**  
OFI  
E-mail: comercial@ofi.com.br  

---

**Página 3 de 12**

### 1. RESUMO EXECUTIVO
A **OFI** é especialista em engenharia, automação industrial e tecnologia, com vasta experiência em projetos de alto impacto no setor de bebidas e manufatura. Atuamos com plataformas de gerenciamento da Indústria 4.0 e oferecemos soluções completas em energia, automação, segurança de dados e integração de sistemas (OT/IT).

**Por que escolher a OFI?**
*   Experiência consolidada em ambientes industriais críticos;
*   Equipe multidisciplinar com certificações técnicas e de segurança;
*   Metodologia de migração focada em *Zero Downtime* e mitigação de riscos;
*   Atendimento técnico de excelência e suporte consultivo.

Nosso compromisso é proporcionar a mitigação de riscos, aumentar a produtividade e reduzir custos operacionais através de metodologias práticas, certificadas e aplicadas com agilidade e eficácia.

### 2. AVISO
Neste documento podem aparecer nomes/marcas comerciais. A **OFI** usa esses nomes para fins de referência apenas, em benefício do proprietário da marca e sem qualquer intenção de violação de marca registrada.

---

**Página 4 de 12**

### 3. INFORMAÇÃO CONFIDENCIAL
Este documento reúne dados sigilosos e estratégicos da **OFI**, cuja divulgação a terceiros depende de autorização prévia, expressa e escrita da própria **OFI**.

Seu conteúdo está coberto pelos compromissos de confidencialidade vigentes entre **OFI** e **COCA-COLA**. Ao aceitá-lo, a **COCA-COLA** reconhece tratar-se de Informação Confidencial da **OFI**. A **COCA-COLA** deve resguardar este material com, no mínimo, o mesmo grau de proteção que aplica aos seus próprios ativos confidenciais.

A preparação deste material baseou-se em elementos fornecidos pela **COCA-COLA**. A **OFI** não responde por perdas ou danos decorrentes de inexatidões, omissões ou inconsistências nessas contribuições. Caso venha a ser firmado contrato com fundamento neste conteúdo, ajustes de escopo necessários em razão de dados incorretos ou incompletos apresentados pela **COCA-COLA** poderão implicar revisões de prazos e valores.

### 4. HISTÓRICO DE REVISÕES
Este documento foi preparado e revisado pelos seguintes responsáveis:
*   **Informações e condições comerciais:** Gestão Comercial OFI
*   **Solução técnica:** Sr. AI Engineer / Coordenador de Projetos
*   **Revisão técnica:** Diretoria de Engenharia OFI

### 5. LISTA DE REVISÕES
| VER. | DATA | POR | DESCRIÇÃO |
| :--- | :--- | :--- | :--- |
| A | 23/10/2023 | OFI | ELABORAÇÃO DA PROPOSTA INICIAL |

---

**Página 5 de 12**

### 6. OBJETIVO GERAL
Este informativo tem como objetivo apresentar a solução técnica para a **Migração do Datacenter Industrial** da planta **COCA-COLA**. 

O foco central é a modernização da infraestrutura através da migração de servidores físicos para virtuais (P2V), atualização da camada de core switching e upgrade dos sistemas de segurança de perímetro (Firewalls). O projeto visa garantir máxima resiliência, performance e segurança para as operações críticas de manufatura, criando uma base escalável para as demandas de Indústria 4.0.

### 7. BENEFÍCIOS
A implementação desta solução trará para a **COCA-COLA** uma transformação em sua capacidade operacional de TI/TA:

**BENEFÍCIOS: CONFIABILIDADE**
*   **Virtualização e Disponibilidade:** Redução do risco de falhas de hardware físico através da migração de 26 servidores para um ambiente virtualizado moderno.
*   **Resiliência de Rede:** Implantação de 5 novos switches core configurados para alta performance e redundância.
*   **Segurança Reforçada:** Upgrade de firewalls para proteção contra ameaças cibernéticas industriais, alinhando a planta aos padrões globais de segurança.

---

**Página 6 de 12**

**BENEFÍCIOS: OPERACIONAIS**
*   **Gestão Centralizada:** Facilidade no gerenciamento das máquinas virtuais e dos ativos de rede, reduzindo o tempo médio de reparo (MTTR).
*   **Otimização de Espaço e Energia:** Consolidação de servidores físicos, resultando em menor consumo de energia e menor dissipação térmica no datacenter.
*   **Documentação Atualizada:** Entrega de Data Book completo contendo as configurações lógicas e topologias físicas implementadas.

**BENEFÍCIOS: FINANCEIROS**
*   **Redução de CAPEX/OPEX:** Menor custo com manutenção de hardware legado e redução de paradas não planejadas que afetam a linha de produção.
*   **Proteção do Investimento:** Upgrade estratégico de ativos (Firewalls) e infraestrutura de rede que suportarão o crescimento da planta nos próximos anos.

---

**Página 7 de 12**

### 8. VISÃO GERAL DA SOLUÇÃO PROPOSTA
Nossa abordagem consiste em um projeto estruturado em quatro pilares principais para garantir uma transição suave e segura:

1.  **Migração P2V (Physical-to-Virtual):** Execução da migração de 26 máquinas físicas para o ambiente virtualizado, incluindo a instalação física, apoio logístico e configuração lógica das instâncias.
2.  **Modernização de Core Switching:** Instalação e configuração de 5 Switches Core, garantindo o backbone de comunicação da planta com alta taxa de transferência.
3.  **Segurança e Perímetro:** Upgrade de firmware e reconfiguração de 2 Firewalls, assegurando que as políticas de segurança estejam atualizadas frente a novas vulnerabilidades.
4.  **Gestão e Consultoria Técnica:** Acompanhamento rigoroso de supply chain, gestão de projeto em tempo integral e consultoria de engenharia para garantir que o "As-Built" reflita a excelência planejada.

### 9. RELAÇÃO DE EQUIPAMENTOS E SOFTWARES FORNECIDOS
Esta seção consolida os ativos envolvidos no projeto. Conforme premissas estabelecidas, o hardware será fornecido pela **COCA-COLA** (Client Supply), cabendo à **OFI** a responsabilidade técnica pela instalação, configuração e integração.

*   **Ativos de Virtualização:** Migração de 26 unidades de servidores (VMs).
*   **Ativos de Rede:** 05 x Switches Core (Instalação e Configuração).
*   **Ativos de Segurança:** 02 x Firewalls (Upgrade e Configuração).

---

**Página 8 de 12**

### 10. DETALHAMENTO DOS SERVIÇOS (ESCOPO)

**T-00: GESTÃO E DOCUMENTAÇÃO**
*   Gestão integral do projeto com reporte semanal de progresso.
*   Consultoria técnica e acompanhamento de Supply Chain para recebimento de ativos.
*   Elaboração de documentação técnica (Data Book) e desenhos de arquitetura.

**T-01: MIGRAÇÃO VMs (P2V) – 26 UNIDADES**
*   Execução de instalação física e migração P2V.
*   Apoio logístico para movimentação de ativos.
*   Configuração lógica e validação de conectividade pós-migração.

**T-02: SWITCHES CORE – 05 UNIDADES**
*   Instalação física em rack.
*   Configuração lógica de VLANs, roteamento e redundância.
*   Testes de failover e performance.

**T-03: FIREWALLS – 02 UNIDADES**
*   Upgrade de firmware e sistemas operacionais.
*   Revisão e migração de regras de segurança.
*   Validação de túneis VPN e perímetros industriais.

---

**Página 9 de 12**

### 11. INVESTIMENTO E RESUMO FINANCEIRO

O investimento para a execução deste projeto, contemplando toda a mão de obra especializada, consultoria, despesas de mobilização e gestão, está sumarizado no quadro abaixo:

| DESCRIÇÃO | VALOR TOTAL (R$) |
| :--- | :--- |
| **SUPRIMENTO DE HARDWARE** | **R$ 0,00** |
| **SERVIÇOS DE ENGENHARIA E MÃO DE OBRA** | **R$ 189.936,00** |
| **DESPESAS (HOSPEDAGEM, ALIMENTAÇÃO, DESLOCAMENTO)** | **R$ 9.540,00** |
| **TOTAL DO INVESTIMENTO** | **R$ 199.476,00** |

*Notas:*
*   *Valores expressos em Reais (BRL).*
*   *Hardware e licenças de software serão fornecidos pela Coca-Cola, exceto se formalizado em aditivo.*
*   *Impostos inclusos conforme legislação vigente para prestação de serviços.*

---

**Página 10 de 12**

### 12. CONDIÇÕES COMERCIAIS
*   **Prazo de Validade da Proposta:** 15 dias.
*   **Condições de Pagamento:** 30 dias após a medição dos marcos contratuais.
*   **Prazo de Execução:** Conforme cronograma a ser acordado no Kick-off (estimado em 30-45 dias).

### 13. GARANTIA
A **OFI** garante os serviços de configuração e instalação por um período de 12 (doze) meses contra vícios de execução, contados a partir da data de entrega definitiva do projeto.

### 14. CONSIDERAÇÕES FINAIS
Esta proposta foi estruturada para garantir que a **COCA-COLA** possua uma infraestrutura de Datacenter Industrial resiliente e moderna. Estamos à disposição para discussões técnicas e ajustes que se façam necessários para o sucesso pleno desta migração.

---

**Página 11 de 12**

### 15. ACEITE DA PROPOSTA

A aprovação desta proposta implica na aceitação de todos os termos aqui descritos.

**Pela COCA-COLA:**  
Nome: ____________________________________________________  
Cargo: ____________________________________________________  
Data: ____ / ____ / ________  
Assinatura: ________________________________________________

**Pela OFI:**  
Nome: ____________________________________________________  
Cargo: ____________________________________________________  
Data: ____ / ____ / ________  
Assinatura: ________________________________________________

---

**Página 12 de 12**

[FIM DO DOCUMENTO]

---
*Gerado automaticamente pelo GPT-Md v1.1 em: 14/01/2026 23:11:42*