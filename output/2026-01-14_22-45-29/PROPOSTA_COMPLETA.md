# PROPOSTA TÉCNICA E COMERCIAL

**Data de Emissão:** 24/05/2024  
**N/ Ref.:** Proposta Técnica – D24050980 – ver. A  
**Projeto:** Implantação de Datacenter de Operações Industriais (IODC)

---

Jundiaí, 24 de maio de 2024

À **OFI - OLAM Foods Ingredients S.A.**  
**Apresentado a:** Sr. Gilmar Corrêa  

**Prezado Sr. Gilmar,**

A **EGE Soluções Industriais** tem o prazer de submeter à **OFI - OLAM Foods Ingredients S.A.** a proposta para prestação de serviços de engenharia visando a **Implantação do Datacenter de Operações Industriais (IODC)**. Este projeto foi concebido para dotar a planta de uma infraestrutura robusta, resiliente e preparada para os desafios da Indústria 4.0.

A presente proposta foi elaborada visando atender às solicitações e expectativas de V.Sas. disponibilizadas até o presente momento. A dúvida ou discordância com relação a qualquer item ou condição da presente proposta, bem como a nulidade de qualquer item da mesma, não a invalida por completo; neste caso, pedimos que entrem em contato conosco para que possamos realizar os ajustes necessários.

Esperamos atender às vossas expectativas e permanecemos a seu inteiro dispor para quaisquer esclarecimentos.

Atenciosamente,

**Roberto Pereira**  
EGE Soluções Industriais  
E-mail: roberto.pereira@egesolucoes.com.br  
Celular: + 55 11 99300-7143

---

### 1. RESUMO EXECUTIVO
A EGE Soluções Industriais é especialista em engenharia, automação industrial e tecnologia, com mais de 20 anos de experiência em projetos de alto impacto. Atuamos com plataformas de gerenciamento da Indústria 4.0 e oferecemos soluções completas em energia, automação, segurança de dados e pessoas, sustentabilidade e indústria inteligente (Smart Industry).

**Por que escolher a EGE?**
*   +20 anos de experiência em projetos industriais;
*   Equipe com certificações NR10, NR12, ISO 50001 e CREA ativo;
*   Cases de sucesso com alta disponibilidade e segurança cibernética;
*   Atendimento técnico de excelência e suporte consultivo.

Nosso compromisso é proporcionar a mitigação de riscos, aumentar a produtividade e reduzir custos operacionais através de metodologias práticas, certificadas e aplicadas com agilidade e eficácia.

### 2. AVISO
Neste documento podem aparecer nomes/marcas comerciais. A EGE Soluções Industriais usa esses nomes para fins de referência apenas, em benefício do proprietário da marca e sem qualquer intenção de violação de marca registrada.

### 3. INFORMAÇÃO CONFIDENCIAL
Este documento reúne dados sigilosos e estratégicos da EGE, cuja divulgação a terceiros depende de autorização prévia, expressa e escrita da própria EGE. Seu conteúdo está coberto pelos compromissos de confidencialidade vigentes entre EGE e OFI. Ao aceitá-lo, a OFI reconhece tratar-se de Informação Confidencial da EGE.

A preparação deste material baseou-se em elementos fornecidos pela OFI. A EGE não responde por perdas ou danos decorrentes de inexatidões ou omissões nessas contribuições. Ajustes de escopo necessários em razão de dados incorretos apresentados poderão implicar revisões de prazos e valores.

### 4. HISTÓRICO DE REVISÕES
Este documento foi preparado e revisado pelos seguintes responsáveis:
*   **Informações e condições comerciais:** Roberto Pereira – Comercial
*   **Solução técnica:** André Mendes – Coordenador Projetos
*   **Revisão técnica:** Fábio Bezerra – Diretor TI

### 5. LISTA DE REVISÕES
| VER. | DATA | POR | DESCRIÇÃO |
| :--- | :--- | :--- | :--- |
| A | 24/05/2024 | AM | ELABORAÇÃO INICIAL DA PROPOSTA IODC |
| B | - | - | - |

---

### 6. OBJETIVO GERAL
Este informativo tem como objetivo apresentar a solução técnica para a **Implantação do Datacenter de Operações Industriais (IODC)** para a unidade da **OFI - OLAM Foods Ingredients S.A.**

O foco central é a criação de um ambiente de missão crítica que integre a **Rede de Automação Industrial**, infraestrutura de servidores virtualizados em alta disponibilidade e sistemas de armazenamento de alto desempenho. A solução visa garantir a convergência segura entre as redes OT/IT, seguindo as melhores práticas de cibersegurança e resiliência operacional.

### 7. BENEFÍCIOS
A implementação desta solução trará para a OFI uma transformação em sua capacidade de processamento e armazenamento industrial:

*   **CONFIABILIDADE:** Arquitetura de Cluster de Virtualização com Alta Disponibilidade (N+1), eliminando paradas por falhas simples de hardware.
*   **SEGURANÇA DE DADOS:** Implementação de uma estrutura de Backup Imutável e NAS dedicado, protegendo a operação contra ataques de Ransomware e perda de dados.
*   **PERFORMANCE:** Uso de switches dedicados de alta performance e storages de baixo tempo de resposta para aplicações críticas de IACS.
*   **PADRONIZAÇÃO:** Interconexão estruturada com a rede IACS, garantindo visibilidade e governança sobre os ativos industriais.
*   **ESCALABILIDADE:** Infraestrutura projetada para suportar o crescimento modular da planta conforme demandas de expansão futura.

### 8. VISÃO GERAL DA SOLUÇÃO PROPOSTA
Nossa abordagem para a OFI é baseada na integração de oito pilares fundamentais:

1.  **Rede de Automação Industrial:** Estruturação lógica e física para tráfego industrial.
2.  **Virtualização:** Camada de software para otimização de recursos de hardware.
3.  **Alta Disponibilidade:** Configuração de Cluster para continuidade de serviço.
4.  **Convergência IACS:** Interconexão segura entre o chão de fábrica e o Datacenter Industrial.
5.  **Storage:** Subsistema de armazenamento centralizado para bases de dados e aplicações.
6.  **Switches de Performance:** Core de rede de baixa latência.
7.  **Backup Imutável:** Camada de segurança para restauração garantida em caso de incidentes.
8.  **NAS Industrial:** Armazenamento secundário e repositório de longa duração.

### 9. RELAÇÃO DE EQUIPAMENTOS E SOFTWARES
**Nota Importante:** Conforme definição estratégica do projeto, o fornecimento de todos os itens de hardware e licenciamento de software será de responsabilidade da **OFI**. A EGE Soluções Industriais atuará na instalação física, configuração lógica, engenharia e comissionamento de:

*   Servidores para o Cluster de Virtualização;
*   Unidades de Storage de Alto Desempenho;
*   Switches Industriais e de Core de Performance;
*   Servidor de Backup e Unidade NAS;
*   Ativos de Rede para Interconexão IACS.

### 10. ESCOPO DE SERVIÇOS (ENGINEERING & LABOR)
O escopo detalhado contempla as seguintes atividades técnicas, executadas por nosso time multidisciplinar:

*   **Gestão de Projeto:** Planejamento, cronograma, coordenação de frentes e reporte.
*   **Instalação Física:** Montagem de racks, fixação de ativos, cabeamento interno ao datacenter e organização de infraestrutura.
*   **Configuração Lógica (Engenharia):** Configuração de vSphere/Hyper-V, configuração de Switches L2/L3, setup de Storage, definição de VLANs industriais e políticas de Backup.
*   **Apoio Logístico:** Movimentação de materiais na planta e suporte à implantação.
*   **Documentação e "As-Built":** Entrega de diagramas de rede, manuais de operação e relatórios de comissionamento.

---

### 11. INVESTIMENTO
O investimento total para a execução deste projeto, considerando a mobilização de equipe especializada, engenharia, documentação e despesas de campo, é apresentado no quadro resumo abaixo:

| CATEGORIA | VALOR TOTAL (BRL) |
| :--- | :--- |
| **FORNECIMENTO DE HARDWARE** | **R$ 0,00 (Pelo Cliente)** |
| **SERVIÇOS DE ENGENHARIA E MÃO DE OBRA** | **R$ 69.360,00** |
| **DESPESAS (HOSPEDAGEM, ALIMENTAÇÃO, TRANSPORTE)** | **R$ 31.590,00** |
| **TOTAL GERAL DO PROJETO** | **R$ 100.950,00** |

### 12. CONDIÇÕES COMERCIAIS
*   **Validade da Proposta:** 15 dias a partir desta data.
*   **Condições de Pagamento:** 30% no aceite (sinal), 40% durante a execução e 30% na entrega final do projeto.
*   **Impostos:** Todos os impostos inclusos conforme legislação vigente (ISS/PIS/COFINS).
*   **Garantia de Serviços:** 12 meses contra defeitos de instalação ou configuração.

---

**Esperamos que esta proposta esteja em conformidade com suas necessidades e aguardamos seu breve retorno para iniciarmos o planejamento deste projeto estratégico para a OFI.**

---
*Gerado automaticamente pelo GPT-Md v1.1 em: 14/01/2026 22:45:49*