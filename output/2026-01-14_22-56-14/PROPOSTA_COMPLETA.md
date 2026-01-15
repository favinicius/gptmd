Página 1 de 12

**Data de Emissão:** 22/05/2024
**D24050220 – PROJETO DETALHADO E IMPLANTAÇÃO IODC**

---

Página 2 de 12

Jundiaí, 22 de maio de 2024

À **OFI - OLAM Foods Ingredients S.A.**
Nome do projeto: **PROJETO DETALHADO E IMPLANTAÇÃO IODC**
N/ Ref.: Proposta Técnica – D24050220 – ver. A
Apresentado a: **Gilmar Corrêa**

Prezado,

A **EGE Soluções Industriais** tem o prazer de submeter à **Gilmar Corrêa** a proposta para prestação de serviços para **Projeto Detalhado e Implantação IODC** a ser executado na planta da **OFI - OLAM Foods Ingredients S.A.** como um projeto Turnkey de engenharia e implementação. A presente proposta foi elaborada visando atender às solicitações e expectativas de V.Sas. disponibilizadas até o presente momento.

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
*   +20 anos de experiência em projetos industriais;
*   Equipe com certificações NR10, NR12, ISO 50001 e CREA ativo;
*   Cases de sucesso com economias comprovadas (até R$ 3 milhões/ano em alguns clientes);
*   Atendimento técnico de excelência e suporte 24h.

Nosso compromisso é proporcionar a mitigação de riscos, aumentar a produtividade e reduzir custos operacionais através de metodologias práticas, certificadas e aplicadas com agilidade e eficácia.

### 2. AVISO
Neste documento podem aparecer nomes/marcas comerciais. A EGE Soluções Industriais usa esses nomes para fins de referência apenas, em benefício do proprietário da marca e sem qualquer intenção de violação de marca registrada.

---

Página 4 de 12

### 3. INFORMAÇÃO CONFIDENCIAL
Este documento reúne dados sigilosos e estratégicos da EGE, cuja divulgação a terceiros depende de autorização prévia, expressa e escrita da própria EGE.

Seu conteúdo está coberto pelos compromissos de confidencialidade vigentes entre EGE e OFI. Ao aceitá-lo, a OFI reconhece tratar-se de Informação Confidencial da EGE, excetuando-se apenas o que já tenha sido anteriormente disponibilizado a Gilmar Corrêa. A OFI deve resguardar este material com, no mínimo, o mesmo grau de proteção que aplica aos seus próprios ativos confidenciais.

A preparação deste material baseou-se em elementos fornecidos pela OFI. A EGE não responde por perdas ou danos decorrentes de inexatidões, omissões ou inconsistências nessas contribuições. Caso venha a ser firmado contrato com fundamento neste conteúdo, ajustes de escopo necessários em razão de dados incorretos ou incompletos apresentados pela OFI poderão implicar revisões de prazos.

### 4. HISTÓRICO DE REVISÕES
Este documento foi preparado e revisado pelos seguintes responsáveis:
*   **Informações e condições comerciais:** Roberto Pereira – Comercial
*   **Solução técnica:** André Mendes – Coordenador Projetos
*   **Revisão técnica:** Fábio Bezerra – Diretor TI

### 5. LISTA DE REVISÕES
| VER. | DATA | POR | DESCRIÇÃO |
| :--- | :--- | :--- | :--- |
| A | 22/05/2024 | AM | ELABORAÇÃO DA PROPOSTA |
| B | | | |

---

Página 5 de 12

### 6. OBJETIVO GERAL
Este informativo tem como objetivo apresentar a **SOLUÇÃO DE ENGENHARIA E IMPLANTAÇÃO** para o novo **IODC (Industrial Operational Data Center)** da planta **OFI** em colaboração com Gilmar Corrêa.

O objetivo primordial é o desenvolvimento do projeto detalhado e a execução técnica da infraestrutura lógica e virtualizada, garantindo a interconexão segura com a Rede IACS. A solução visa entregar um ambiente de alta performance através de um cluster de virtualização industrial, storage de alto desempenho e uma estrutura de backup resiliente, assegurando a continuidade operacional e a integridade dos dados críticos de manufatura conforme os requisitos da Indústria 4.0.

### 7. BENEFÍCIOS
A implementação da nossa solução integrada trará para a OFI uma transformação completa em sua capacidade operacional de TI/TA:

**BENEFÍCIOS DE CONFIABILIDADE**
*   **Arquitetura de Alta Disponibilidade:** Implementação de Cluster de Virtualização garantindo que falhas de hardware não interrompam os serviços críticos da planta.
*   **Imutabilidade de Dados:** Estrutura de backup desenhada para proteção contra Ransomware e falhas catastróficas.
*   **Segurança IACS:** Interconexão padronizada entre a rede de automação e o IODC, mitigando riscos de acessos não autorizados e propagação de ameaças.

**BENEFÍCIOS OPERACIONAIS**
*   **Gestão Centralizada:** Console único para gestão de VMs, servidores e storage, reduzindo o tempo de resposta da equipe de suporte.
*   **Escalabilidade Industrial:** Dimensionamento planejado para suportar o crescimento da planta sem necessidade de reestruturação física imediata.
*   **Padronização Técnica:** Documentação detalhada (As-Built) e planejamento técnico que facilitam manutenções futuras.

**BENEFÍCIOS FINANCEIROS**
*   **Redução de Downtime:** A mitigação de paradas não planejadas reflete diretamente na preservação da margem de produção.
*   **Otimização de Hardware:** Uso eficiente dos recursos de processamento e memória através de virtualização avançada.

---

Página 6 de 12

### 8. VISÃO GERAL DA SOLUÇÃO PROPOSTA
Nossa abordagem para a OFI baseia-se em um fluxo de implementação técnica dividido em pilares estratégicos:

1.  **Engenharia de Detalhamento:** Elaboração de toda a documentação técnica, diagramas de rede e planejamento de migração.
2.  **Fundação Lógica (Virtualização):** Criação do Cluster de Virtualização Industrial e dimensionamento preciso de Servidores e Máquinas Virtuais (VMs).
3.  **Core de Performance:** Configuração de Storage de alto desempenho e Switches dedicados para garantir baixa latência no tráfego de dados industriais.
4.  **Conectividade Segura:** Interconexão estruturada com a rede IACS (Industrial Automation and Control Systems).
5.  **Proteção e Continuidade:** Implantação da camada de Backup e políticas de imutabilidade de dados.

### 9. ESCOPO TÉCNICO E SERVIÇOS
Esta seção descreve os tópicos de atuação técnica que serão cobertos pela equipe de engenharia da EGE:

*   **T-01: Elaboração de Projeto Detalhado:** Documentação completa da arquitetura IODC.
*   **T-02: Consultoria e Planejamento Técnico:** Alinhamento de requisitos e definição de premissas de projeto.
*   **T-03: Cluster de Virtualização Industrial:** Configuração de alta disponibilidade para servidores host.
*   **T-04: Interconexão com Rede IACS:** Configuração de roteamento, VLANs e segurança entre zonas OT.
*   **T-05: Dimensionamento de Servidores e VMs:** Otimização de recursos computacionais para aplicações industriais.
*   **T-06: Storage de Alto Desempenho:** Configuração de LUNs, volumes e políticas de acesso a dados.
*   **T-07: Switches Dedicados de Performance:** Parametrização de ativos de rede core para o IODC.
*   **T-08: Estrutura de Backup e Imutabilidade:** Implementação de rotinas de proteção e guarda segura.

*Nota: Conforme premissas do projeto, o fornecimento de hardware físico não compõe o valor desta proposta de serviços de engenharia.*

---

Página 7 de 12

### 10. INVESTIMENTO
Abaixo apresentamos o resumo consolidado do investimento para a execução do projeto Turnkey de Engenharia e Implantação:

| Descrição do Item | Valor Total (BRL) |
| :--- | :--- |
| **Fornecimento de Hardware e Software** | **R$ 0,00** |
| **Serviços de Engenharia e Mão de Obra Especializada** | **R$ 54.336,00** |
| **Despesas Operacionais (Hospedagem, Alimentação, Deslocamento)** | **R$ 31.590,00** |
| **INVESTIMENTO TOTAL DO PROJETO** | **R$ 85.926,00** |

**Condições Comerciais:**
*   **Impostos:** Inclusos conforme legislação vigente.
*   **Validade da Proposta:** 15 dias.
*   **Condição de Pagamento:** A combinar (Sugestão: 30% Mobilização, 40% Entrega Técnica, 30% Aceite Final).

### 11. CRONOGRAMA ESTIMADO
O prazo estimado para a execução total do projeto é de aproximadamente **4 a 6 semanas**, condicionado à disponibilidade do hardware no site e liberação de acessos pela equipe da OFI.

---

Página 8 de 12

### 12. CONSIDERAÇÕES FINAIS
A EGE Soluções Industriais reafirma seu compromisso com a excelência técnica e o sucesso operacional da **OFI - OLAM Foods Ingredients S.A.** Estamos à disposição para refinamentos de escopo e ajustes necessários para o início imediato deste projeto estratégico.

Atenciosamente,

**EGE Soluções Industriais**

---
*Gerado automaticamente pelo GPT-Md v1.1 em: 14/01/2026 22:56:40*