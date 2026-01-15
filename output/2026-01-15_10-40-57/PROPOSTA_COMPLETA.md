Página 1 de 15

Data de Emissão: 24/05/2024
D24050291 CONSULTORIA, FORNECIMENTO E IMPLEMENTAÇÃO DE IODC E DISASTER RECOVERY – UNIDADE ILHÉUS

Página 2 de 15
Jundiaí, 24 de maio de 2024
À OFI - OLAM FOODS INGREDIENTS S.A.
Nome do projeto: CONSULTORIA, FORNECIMENTO E IMPLEMENTAÇÃO DE IODC E DISASTER RECOVERY – UNIDADE ILHÉUS
N/ Ref.: Proposta Técnica – D24050291 – ver. A
Apresentado a: Diretoria de Operações e TI

Prezado,

A EGE Soluções Industriais tem o prazer de submeter à OFI - OLAM FOODS INGREDIENTS S.A. a proposta para prestação de serviços de Consultoria, Fornecimento e Implementação de Infraestrutura de Datacenter Industrial (IODC) e Disaster Recovery (DR) a ser executado na planta localizada em ILHÉUS (BA) como um projeto Turnkey. A presente proposta foi elaborada visando atender às solicitações e expectativas de V.Sas. disponibilizadas até o presente momento, com foco em resiliência geográfica e continuidade de negócio.

A dúvida ou discordância com relação a qualquer item ou condição da presente proposta, bem como a nulidade de qualquer item da mesma não a invalida por completo, sendo que neste caso, pedimos que entrem em contato conosco para que possamos atender às suas necessidades.

Esperamos atender as vossas expectativas e permanecemos a seu inteiro dispor para quaisquer esclarecimentos que se façam necessários.

Atenciosamente,

Roberto Pereira
EGE Soluções Industriais
E-mail: roberto.pereira@egesolucoes.com.br
Celular: + 55 11 99300-7143

Página 3 de 15
1. RESUMO EXECUTIVO
A EGE Soluções Industriais é especialista em engenharia, automação industrial e tecnologia, com mais de 20 anos de experiência em projetos de alto impacto. Atuamos com plataformas de gerenciamento da Indústria 4.0 e oferecemos soluções completas em energia, automação, segurança de dados e pessoas, sustentabilidade e indústria inteligente (Smart Industry).

Por que escolher a EGE?
• +20 anos de experiência em projetos industriais;
• Equipe com certificações NR10, NR12, ISO 50001 e CREA ativo;
• Expertise em ambientes de missão crítica e recuperação de desastres;
• Atendimento técnico de excelência e suporte 24h.

Nosso compromisso para a OFI é proporcionar a mitigação de riscos catastróficos, aumentar a confiabilidade da infraestrutura de TI Industrial e garantir a integridade dos dados através de uma estratégia robusta de Disaster Recovery e Imutabilidade.

2. AVISO
Neste documento podem aparecer nomes/marcas comerciais. A EGE Soluções Industriais usa esses nomes para fins de referência apenas, em benefício do proprietário da marca e sem qualquer intenção de violação de marca registrada.

Página 4 de 15
3. INFORMAÇÃO CONFIDENCIAL
Este documento reúne dados sigilosos e estratégicos da EGE, cuja divulgação a terceiros depende de autorização prévia, expressa e escrita da própria EGE.

Seu conteúdo está coberto pelos compromissos de confidencialidade vigentes entre EGE e OFI - OLAM FOODS INGREDIENTS S.A. Ao aceitá-lo, a OFI reconhece tratar-se de Informação Confidencial da EGE, excetuando-se apenas o que já tenha sido anteriormente disponibilizado. A OFI deve resguardar este material com, no mínimo, o mesmo grau de proteção que aplica aos seus próprios ativos confidenciais.

A preparação deste material baseou-se em elementos fornecidos pela OFI. A EGE não responde por perdas ou danos decorrentes de inexatidões, omissões ou inconsistências nessas contribuições. Caso venha a ser firmado contrato com fundamento neste conteúdo, ajustes de escopo necessários em razão de dados incorretos ou incompletos apresentados pela OFI poderão implicar revisões de prazos.

4. HISTÓRICO DE REVISÕES
Este documento foi preparado e revisado pelos seguintes responsáveis:
Informações e condições comerciais: Roberto Pereira – Comercial
Solução técnica: André Mendes – Coordenador Projetos
Revisão técnica: Fábio Bezerra – Diretor TI

5. LISTA DE REVISÕES
VER. DATA POR DESCRIÇÃO
A 24/05/2024 AM ELABORAÇÃO DA PROPOSTA INICIAL

Página 5 de 15
6. OBJETIVO GERAL
Este informativo tem como objetivo apresentar a SOLUÇÃO "TURNKEY" completa para a modernização e implementação da infraestrutura de TI Industrial (IODC) e Disaster Recovery da planta OFI em Ilhéus, Bahia.

O objetivo central é estabelecer um cluster Hyper-V de alta performance, integrado a um sistema de storage centralizado e uma estratégia de backup imutável. Além disso, o projeto contempla a criação de uma sala de Disaster Recovery geograficamente redundante dentro da planta, garantindo que as operações críticas de manufatura da OLAM Foods Ingredients possuam resiliência contra falhas sistêmicas ou incidentes físicos no Datacenter principal, suportando as demandas atuais e futuras da Indústria 4.0.

7. BENEFÍCIOS
A implementação da nossa solução integrada trará para a OFI uma transformação na continuidade de seu negócio:

BENEFÍCIOS CONFIABILIDADE
• Redundância Geográfica (DR): Mitigação de riscos de parada total da planta através de uma sala de Disaster Recovery equipada e configurada para assumir a carga de trabalho em caso de sinistro no IODC principal.
• Continuidade de Negócio com Cluster HA: A arquitetura Hyper-V com 3 hosts garante que a falha de um servidor físico não interrompa as máquinas virtuais, realizando o failover automático.
• Proteção contra Ransomware: A implementação de repositórios NAS com imutabilidade assegura que os backups da OFI não possam ser deletados ou criptografados por agentes maliciosos, garantindo o recovery em qualquer cenário.

Página 6 de 15
BENEFÍCIOS OPERACIONAIS
• Gestão Centralizada e Escalável: Infraestrutura baseada em switches Cisco de alto desempenho e virtualização Microsoft, permitindo uma expansão modular e simplificada.
• Redução do MTTR (Tempo Médio de Reparo): Com ambientes documentados (As-Built) e redundantes, o tempo de resposta a incidentes críticos é drasticamente reduzido.

BENEFÍCIOS FINANCEIROS
• Proteção do Patrimônio de Dados: O custo de uma parada de produção ou perda de dados em uma unidade processadora de alimentos como a de Ilhéus supera largamente o investimento em sistemas de DR.
• Eficiência em Hardware: Utilização de storage de alto desempenho para consolidar cargas de trabalho, reduzindo o consumo de energia e espaço físico em rack.

BENEFÍCIOS ESTRATÉGICOS
• Conformidade com Padrões Globais: Alinhamento da planta de Ilhéus às diretrizes globais de segurança da informação e resiliência cibernética da OLAM.
• Visão de Futuro (Ready for IoT): A nova rede industrial e o cluster de virtualização fornecem o "compute" necessário para futuras implementações de análise de dados em tempo real e IA na borda.

Página 7 de 15
8. VISÃO GERAL DA SOLUÇÃO PROPOSTA
Nossa abordagem consiste em um projeto integrado de ponta a ponta, fundamentado em cinco pilares estratégicos para a OFI:

1. Planejamento e Design (Planbook): Fase dedicada à definição técnica detalhada, cronograma executivo e validação de diretrizes com a diretoria, garantindo que o projeto nasça com 100% de aderência às necessidades da OLAM.
2. Infraestrutura de Processamento e Alta Disponibilidade: Fornecimento e configuração de 03 Hosts de alta performance para o cluster Hyper-V, garantindo o poder de processamento necessário.
3. Backbone de Conectividade Industrial: Implementação de switches Cisco de alto desempenho, configurados para máxima vazão e segmentação de rede.
4. Armazenamento e Proteção de Dados: Centralização de dados em Storage de alto desempenho e garantia de recuperação através de servidores de backup com repositórios NAS imutáveis.
5. Redundância Geográfica (DR Site): Ativação de uma segunda sala técnica (Disaster Recovery) preparada para sustentar a operação em cenários de contingência.

9. RELAÇÃO DE EQUIPAMENTOS E SOFTWARES FORNECIDOS
Esta seção consolida os ativos que serão fornecidos e implementados na unidade de Ilhéus.

COMPONENTES DE PROCESSAMENTO E ARMAZENAMENTO
• 03 x Servidores Host de Alta Performance (configurados para Cluster Hyper-V).
• 01 x Storage de Alto Desempenho (Sistemas de discos redundantes e alta IOPS).
• 02 x Servidores de Backup dedicados.
• 02 x Unidades de Repositório NAS com suporte a Imutabilidade de dados.

COMPONENTES DE REDE E CONECTIVIDADE
• 03 x Switches Cisco de Alto Desempenho (Camada de Core/Acesso Industrial).
• Transceivers SFP/SFP+ e cabos Twinax para interconexão de alta velocidade (10Gbps+).
• Kits de montagem em Rack e acessórios de organização.

INFRAESTRUTURA DE SALA DE DR
• Racks de TI padrão 19" para a Sala de Disaster Recovery.
• Componentes de manobra e terminação óptica/metálica (DIO/Patch Panels).

Página 8 de 15
10. ESCOPO TÉCNICO E DETALHAMENTO DAS ATIVIDADES

10.1. Fase de Planejamento, Planbook e Cronograma (T-01)
Fase mandatória de 30 dias dedicada à estruturação do projeto:
• Reuniões de Kick-off e alinhamento de expectativas.
• Levantamento detalhado (Site Survey) das salas técnica e de DR em Ilhéus.
• Elaboração do Planbook (Projeto Executivo) com topologias lógicas e físicas.
• Aprovação do cronograma detalhado junto à diretoria da OFI.

10.2. Implementação do Cluster Hyper-V (T-02)
Configuração da camada de processamento principal:
• Recebimento, inspeção e montagem física dos 03 servidores host.
• Atualização de Firmwares, BIOS e aplicação de Hardening de segurança.
• Instalação e configuração do Hypervisor Microsoft Hyper-V.
• Configuração de Storage e Zoning Fibre Channel/iSCSI.
• Implementação do Cluster HA (High Availability) e Failover.
• Provisionamento de VMs (Templates/Clones) e rotinas de backup iniciais.
• Testes de Aceitação em Campo (SAT) assistidos.

10.3. Implementação da Rede Cisco (T-03)
Espinha dorsal de conectividade:
• Instalação física dos switches Cisco de alto desempenho.
• Configuração de empilhamento (Stack) ou redundância de agregação.
• Implementação e segmentação de VLANs conforme melhores práticas industriais.
• Testes de resiliência de anel (MRP/DLR ou Spanning Tree otimizado).
• Organização e identificação de todo o cabeamento estruturado de rede.

10.4. Implementação de Storage e Proteção de Dados (T-04 e T-05)
Garantia de integridade e armazenamento:
• Montagem em rack e configuração do Storage central de alta performance.
• Implementação da estrutura de backup completa.
• Configuração dos repositórios NAS imutáveis (proteção contra deleção acidental/maliciosa).
• Definição e teste das rotinas de retenção de dados e RPO/RTO.

10.5. Implementação da Sala de Disaster Recovery (T-06)
Resiliência geográfica na unidade de Ilhéus:
• Montagem física da infraestrutura na sala de DR decidida pelo cliente.
• Configuração lógica da redundância de rede para o site secundário.
• Validação da sincronização de dados entre o site principal e o site de DR.

Página 9 de 15
11. TESTES, VALIDAÇÕES E COMISSIONAMENTO
O sucesso da implementação na OFI será validado através de:
• Validação Física: Certificação de cabeamento e inspeção de montagem.
• Testes de Failover: Simulação de queda de um host físico para validar a continuidade das VMs.
• Teste de Disaster Recovery: Simulação de perda do site principal e ativação do site de contingência (DR).
• Teste de Imutabilidade: Validação da proteção dos backups contra tentativas de exclusão.
• Documentação As-Built (T-00): Entrega de toda a documentação técnica final, diagramas e senhas.

12. EQUIPE CHAVE E RESPONSABILIDADES
Para este projeto na OFI, alocaremos:
• Gerente de Projeto: Gestão de cronograma e governança (Status Semanal/Dailies).
• Engenheiro de Redes/Sistemas: Responsável pela configuração Cisco e Cluster Hyper-V.
• Analista de Infraestrutura: Responsável por virtualização, backup e imutabilidade.
• Equipe Técnica de Campo: Montagem física, trâmites de SHE (Segurança, Higiene e Meio Ambiente) e integração.

13. RESUMO DO INVESTIMENTO
O investimento total para este projeto turnkey (Serviços + Logística) está consolidado abaixo:

DESCRIÇÃO VALOR TOTAL (BRL)
Total de Mão de Obra Especializada (Engenharia e Implementação) R$ 129.972,00
Total de Despesas Logísticas (Aéreos, Hospedagem, Mobilização) R$ 52.620,00
VALOR TOTAL DO PROJETO R$ 182.592,00

NOTAS GERAIS:
• Local de Execução: Unidade OFI - Ilhéus/BA.
• Prazo Estimado: Conforme cronograma a ser validado no Planbook.
• Condições de Pagamento: A definir em contrato (Eventos de Medição).

---
*Gerado automaticamente pelo GPT-Md v1.1 em: 15/01/2026 10:41:26*