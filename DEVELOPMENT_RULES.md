# CONSTITUIÇÃO DE DESENVOLVIMENTO DO PROJETO v2.0 (FOCO EM MOD E LÓGICA)

Estas regras são PARAMONTES e substituem qualquer instrução anterior que favoreça a brevidade. O objetivo é "Orçamentação Defensiva" e "Visibilidade Granular".

## 1. GRANULARIDADE MANDATÓRIA (Regra "Sem Agrupamento")
**Conceito:** Um Item de Escopo ≠ Uma Linha no MOD.
**Diretriz:** É ESTREITAMENTE PROIBIDO agrupar fases técnicas distintas em uma única atividade genérica.
**Execução:**
Para cada ativo de Hardware ou Software detectado (ex: "Cluster Hyper-V", "Switch Cisco"), você DEVE instanciar o ciclo de vida completo:
   1. **Logística/Física:** Recebimento -> Inspeção -> Montagem em Rack -> Cabeamento e Identificação.
   2. **Lógica de Baixo Nível:** Atualização de Firmware -> Hardening de BIOS -> Configuração de RAID/Zoning.
   3. **Lógica de Alto Nível:** Instalação de SO -> Configuração de Rede (L2/L3) -> Setup de HA/Cluster.
   4. **Validação:** Testes de Failover -> Validação de Backup -> SAT (Teste de Aceitação de Campo).
*Resultado:* Um único servidor deve gerar pelo menos 4-6 linhas distintas na tabela MOD.

## 2. ESPELHAMENTO DE LOGÍSTICA (Viagem é Trabalho)
**Conceito:** Se a equipe está se movendo, o relógio está correndo.
**Diretriz:** Você deve injetar linhas de "Mobilização/Deslocamento Técnico (Ida/Volta)" na tabela MOD correspondentes aos segmentos logísticos.
**Execução:**
   *   SE existirem segmentos logísticos:
   *   CRIAR Atividade: "Mobilização/Deslocamento Técnico (Ida/Volta)"
   *   QUANTIDADE: Número de viagens * Tamanho da Equipe.
   *   HORAS: Duração da viagem (padrão 4h para regional, 8h para nacional se desconhecido).
   *   PAPEL: Aplicar a todos os papéis envolvidos (Engenheiros + Analistas).

## 3. ESTIMATIVA DEFENSIVA (Regra "Não Inocente")
**Conceito:** Assuma que o "Caminho Feliz" nunca acontece.
**Diretriz:** Aplique um **Multiplicador de Complexidade** às horas padrão com base em palavras-chave de contexto.
**Execução:**
   *   **Padrão:** Multiplicador 1.0x
   *   **Contextos Complexos:** Se o prompt mencionar "Disaster Recovery", "Brownfield", "Migração" ou "Nova Tecnologia":
       -> **Multiplicador FORÇADO: 1.5x em todas as horas de Configuração/Lógica.**
   *   **Buffers Implícitos:** Sempre adicione uma linha distinta para "Ineficiência/SHE" (Segurança, permissões, tempo de espera) calculada como 5-10% do total de horas técnicas.

## 4. PROVENIÊNCIA DE DADOS (Coluna Source_Ref)
**Conceito:** Confie, mas verifique.
**Diretriz:** A tabela de saída (MOD) deve incluir uma coluna chamada `Source_Ref`.
**Valores:**
   *   `DB_STD`: Valor exato do `db_mod.json`.
   *   `DB_CALC`: Calculado/Derivado da lógica do DB.
   *   `ESTIMATE`: Inferência do LLM onde os dados do DB estavam faltando.
   *   `EXPLICIT`: Forçado pelo prompt do usuário (ex: "80h de treinamento").

## 5. VISIBILIDADE DA FASE DE PLANEJAMENTO
**Diretriz:** Se uma "Fase de Planejamento" específica for solicitada (ex: 30 dias), ela NÃO deve ser uma linha única.
**Execução:** Decomponha em:
   *   Kick-off e Levantamento de Requisitos.
   *   Definição de Hardware e Validação de BOM.
   *   Design de Baixo Nível (LLD) e Criação de Planbook.
   *   Reuniões de Aprovação Executiva.
