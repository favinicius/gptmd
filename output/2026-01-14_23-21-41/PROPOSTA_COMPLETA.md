# PROPOSTA TÉCNICA E COMERCIAL: PROJETO DE MIGRAÇÃO COCA-COLA

Página 1 de 12

**Data de Emissão:** 24/05/2024
**Nº da Proposta:** CC-240524-01
**PROJETO:** MIGRAÇÃO DE INFRAESTRUTURA E CORE NETWORKING COCA-COLA

---

Página 2 de 12

Jundiaí, 24 de maio de 2024

À **Coca-Cola**.
Nome do projeto: **PROJETO DE MIGRAÇÃO (VMs E SWITCHES CORE)**
N/ Ref.: Proposta Técnica – CC-240524-01 – ver. A
Apresentado a: Gestão de Infraestrutura Coca-Cola

Prezado,

A **EGE Soluções Industriais** tem o prazer de submeter à **Coca-Cola** a proposta para prestação de serviços para a **Migração de Máquinas Virtuais e Switches Core**, a ser executado conforme os requisitos de alta disponibilidade e performance. A presente proposta foi elaborada visando atender às solicitações e expectativas de V.Sas. disponibilizadas até o presente momento.

A dúvida ou discordância com relação a qualquer item ou condição da presente proposta, bem como a nulidade de qualquer item da mesma não a invalida por completo, sendo que neste caso, pedimos que entrem em contato conosco para que possamos atender às suas necessidades.

Esperamos atender as vossas expectativas e permanecemos a seu inteiro dispor para quaisquer esclarecimentos que se façam necessários.

Atenciosamente,

**Roberto Pereira**
EGE Soluções Industriais
E-mail: roberto.pereira@egesolucoes.com.br
Celular: + 55 11 99300-7143

---

Página 3 de 12

### 1. RESUMO EXECUTIVO
A EGE Soluções Industriais é especialista em engenharia, automação industrial e tecnologia, com mais de 20 anos de experiência em projetos de alto impacto. Atuamos com plataformas de gerenciamento da Indústria 4.0 e oferecemos soluções completas em energia, automação, segurança de dados e pessoas, sustentabilidade e indústria inteligente (Smart Industry).

**Por que escolher a EGE?**
* +20 anos de experiência em projetos industriais;
* Equipe com certificações de alto nível e conformidade técnica;
* Cases de sucesso com economias comprovadas e alta disponibilidade;
* Atendimento técnico de excelência e suporte consultivo.

Nosso compromisso é proporcionar a mitigação de riscos, aumentar a produtividade e reduzir custos operacionais através de metodologias práticas, certificadas e aplicadas com agilidade e eficácia no ambiente da Coca-Cola.

---

Página 4 de 12

### 2. AVISO
Neste documento podem aparecer nomes/marcas comerciais. A EGE Soluções Industriais usa esses nomes para fins de referência apenas, em benefício do proprietário da marca e sem qualquer intenção de violação de marca registrada.

### 3. INFORMAÇÃO CONFIDENCIAL
Este documento reúne dados sigilosos e estratégicos da EGE, cuja divulgação a terceiros depende de autorização prévia, expressa e escrita da própria EGE. Seu conteúdo está coberto pelos compromissos de confidencialidade vigentes entre EGE e Coca-Cola. Ao aceitá-lo, a Coca-Cola reconhece tratar-se de Informação Confidencial da EGE.

### 4. HISTÓRICO DE REVISÕES
Este documento foi preparado e revisado pelos seguintes responsáveis:
* **Informações e condições comerciais:** Roberto Pereira – Comercial
* **Solução técnica:** André Mendes – Coordenador Projetos
* **Revisão técnica:** Fábio Bezerra – Diretor TI

### 5. LISTA DE REVISÕES
| VER. | DATA | POR | DESCRIÇÃO |
| :--- | :--- | :--- | :--- |
| A | 24/05/2024 | AM | ELABORAÇÃO DA PROPOSTA |

---

Página 5 de 12

### 6. OBJETIVO GERAL
Este informativo tem como objetivo apresentar a **SOLUÇÃO DE MIGRAÇÃO TÉCNICA** para modernizar a infraestrutura de TI da Coca-Cola.

O objetivo central é realizar a **Migração P2V (Physical-to-Virtual) de 26 instâncias**, garantindo a continuidade operacional e a integridade dos dados, além da **instalação e configuração de 05 Switches Core**, estabelecendo uma infraestrutura de rede resiliente, segura e de alta performance para suportar as demandas críticas da operação.

### 7. BENEFÍCIOS
A implementação da nossa solução integrada trará para a Coca-Cola uma transformação em sua capacidade de infraestrutura:

**BENEFÍCIOS DE CONFIABILIDADE**
* **Estabilidade do Ambiente Virtualizado:** A migração de 26 VMs para um ambiente controlado reduz falhas de hardware legado e centraliza a gestão.
* **Rede de Core de Alta Performance:** A implantação dos 5 Switches Core elimina gargalos de comunicação e garante redundância física e lógica (N+1).
* **Segurança de Dados:** Processos de migração P2V validados para evitar perda de dados e garantir o "go-live" sem retrocessos.

---

Página 6 de 12

**BENEFÍCIOS OPERACIONAIS**
* **Gestão Simplificada:** Com a infraestrutura física dos switches renovada e os servidores virtualizados, o diagnóstico de rede e a manutenção de sistemas tornam-se mais ágeis.
* **Redução do MTTR (Tempo Médio de Reparo):** Equipamentos modernos e máquinas virtuais permitem recuperações rápidas em casos de incidentes (snapshots e alta disponibilidade).

**BENEFÍCIOS FINANCEIROS**
* **Redução de OPEX:** Menor consumo de energia e menor necessidade de manutenção física de servidores antigos.
* **Proteção do Investimento:** Implementação de switches de última geração que suportam o crescimento de tráfego de rede para os próximos anos.

---

Página 7 de 12

**BENEFÍCIOS ESTRATÉGICOS**
* **Escalabilidade:** A nova base de virtualização e o core de rede permitem que a Coca-Cola adicione novos serviços e aplicações com agilidade técnica.
* **Responsabilidade Técnica:** Todo o projeto conta com coordenação especializada, garantindo que a migração não impacte a produtividade da planta.

### 8. VISÃO GERAL DA SOLUÇÃO PROPOSTA
Nossa abordagem baseia-se em quatro pilares fundamentais:

1. **Gestão e Planejamento:** Coordenação detalhada da migração para minimizar janelas de downtime.
2. **Infraestrutura e Instalação Física:** Montagem e comissionamento dos 5 novos Switches Core nos racks de destino.
3. **Configuração Lógica:** Parametrização avançada de redes (VLANs, Roteamento, Segurança) e virtualização das 26 máquinas físicas (P2V).
4. **Documentação e Entrega:** Entrega de Data Books técnicos e diagramas de rede atualizados.

---

Página 8 de 12

### 9. RELAÇÃO DE EQUIPAMENTOS E SOFTWARES FORNECIDOS
Esta seção consolida os ativos envolvidos na solução.

**COMPONENTES DE HARDWARE**
* **Hardware Fornecido pelo Cliente:** Para este projeto, o hardware necessário (Servidores para VMs e Switches Core) será fornecido pela **Coca-Cola**, ficando a cargo da EGE toda a engenharia, instalação e configuração.

**SERVIÇOS TÉCNICOS INTEGRADOS**
* **Migração de VMs:** Processamento e migração de 26 unidades via ferramenta P2V.
* **Switches Core:** Instalação física e configuração lógica de 05 unidades de alta performance.
* **Materiais de Consumo:** Insumos necessários para a instalação física (patch cords, identificadores, organizadores) conforme a necessidade de campo.

---

Página 9 de 12

### 10. ESCOPO DE SERVIÇOS (DETALHAMENTO TÉCNICO)

Com base no planejamento estratégico, os serviços estão divididos nos seguintes tópicos:

* **T-01: Migração de VMs (26 unidades)**
  - Análise de compatibilidade de hardware físico original.
  - Execução de migração P2V (Physical-to-Virtual).
  - Testes de integridade e validação de aplicações pós-migração.
  
* **T-02: Instalação de Switches Core (05 unidades)**
  - Instalação física em rack padrão 19".
  - Configuração de redundância e protocolos de rede.
  - Integração com a infraestrutura existente e testes de throughput.

* **T-00: Gestão e Documentação**
  - Gestão do projeto com acompanhamento de cronograma.
  - Elaboração de documentação técnica (As-Built).

---

Página 10 de 12

### 11. INVESTIMENTO

O investimento para a execução deste projeto na modalidade Turnkey (Serviços e Despesas) está consolidado no quadro abaixo:

| Descrição do Item | Valor Total (BRL) |
| :--- | :--- |
| **Total em Hardware e Materiais** | **R$ 0,00** |
| **Total em Serviços e Mão de Obra Especializada** | **R$ 44.208,00** |
| **Total em Despesas (Hospedagem, Alimentação, Deslocamento)** | **R$ 2.190,00** |
| **VALOR TOTAL DO PROJETO** | **R$ 46.398,00** |

**Condições Comerciais:**
* **Impostos:** Inclusos conforme legislação vigente.
* **Validade da Proposta:** 15 dias.
* **Condição de Pagamento:** A combinar (padrão 30 dias após medição).

---

Página 11 de 12

### 12. CRONOGRAMA ESTIMADO
O prazo total estimado para a execução das atividades é de aproximadamente **15 a 20 dias úteis**, condicionado à disponibilidade das janelas de manutenção e entrega dos equipamentos por parte da Coca-Cola.

* **Fase 1:** Gestão e Planejamento (2 dias)
* **Fase 2:** Instalação Física e Configuração de Switches (10 dias)
* **Fase 3:** Migração de VMs P2V (7 dias - em paralelo)
* **Fase 4:** Documentação e Encerramento (1 dia)

---

Página 12 de 12

### 13. CONSIDERAÇÕES FINAIS
A EGE Soluções Industriais reforça seu compromisso com a qualidade e segurança na entrega deste projeto para a **Coca-Cola**. Nossa equipe técnica está dimensionada com Gestores, Engenheiros e Técnicos de alta senioridade para garantir que a migração ocorra com o menor impacto possível à operação.

Permanecemos à disposição para reuniões técnicas de alinhamento e detalhamento de quaisquer pontos desta proposta.

Atenciosamente,

**EGE Soluções Industriais**
Setor de Engenharia de Projetos

---
*Gerado automaticamente pelo GPT-Md v1.1 em: 14/01/2026 23:22:02*