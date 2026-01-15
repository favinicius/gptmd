# 🏆 PDR Vencedor

### **GPTA: Plataforma de Geração de Propostas - PRD Evolutivo v1.3**

**Nota Estratégica do Arquiteto:** Este documento abandona a ideia de um único lançamento monolítico em favor de um **plano de entregas evolutivo**. Iremos construir e lançar a plataforma em fases (épicos), onde cada fase entrega um conjunto coeso de funcionalidades, valida uma hipótese de negócio específica e informa a próxima etapa. A arquitetura, centrada no **Repository Pattern**, foi projetada desde o início para suportar essa evolução, garantindo que a complexidade seja adicionada de forma incremental e sustentável. Nosso mantra é: **Validar. Construir. Evoluir.**

---

### **O Caminho Evolutivo: Do Gerador à Plataforma**

- **ÉPICO 1 (MVP): O Gerador.** Foco absoluto em validar a qualidade e o valor da geração automática. Hipótese: "A IA pode criar um rascunho de proposta bom o suficiente a partir de múltiplos contextos para economizar tempo dos usuários?"
- **ÉPICO 2 (Pós-MVP): A Bancada de Edição.** Foco em reter o usuário na plataforma. Hipótese: "Uma vez que o rascunho é gerado, os usuários preferem fazer edições rápidas na própria ferramenta em vez de exportar imediatamente?"
- **ÉPICO 3 (Pós-MVP): O Painel de Controle.** Foco em capacitar usuários avançados. Hipótese: "Existe uma demanda real por customização profunda de templates e prompts para justificar a complexidade de gerenciamento?"

---

### **ÉPICO 1 (MVP): O Gerador - Validando a Proposta de Valor Central**

**1. Objetivo do Épico**
Lançar a funcionalidade mais essencial do produto: a capacidade de transformar múltiplos contextos de texto em um rascunho de proposta coeso. Todo o esforço está concentrado em provar que o "motor" de IA da plataforma gera resultados valiosos.

**2. Hipótese a Validar**
Acreditamos que, ao fornecer uma ferramenta que analisa múltiplos campos de texto (RFQ, notas estratégicas) e os transforma em uma proposta estruturada, conseguiremos validar que a automação economiza tempo suficiente para ser adotada pelas equipes de Vendas e Engenharia.

**3. Requisitos Funcionais do Épico 1**

- **US-1.1: Gerar Proposta a partir de Múltiplos Contextos**: Como um Engenheiro de Vendas, quero ter campos de texto separados para "Requisitos do Cliente", "Minhas Notas Estratégicas" e "Outras Informações", para que a plataforma use todo esse contexto para gerar uma única proposta coesa e inteligente.
- **US-1.2: Visualizar e Exportar a Proposta Gerada**: Como um Engenheiro de Vendas, quero visualizar a proposta gerada em uma interface limpa e ter um botão "Copiar para Área de Transferência" (preservando a formatação básica), para que eu possa facilmente movê-la para o Word ou Google Docs para finalização.
- **US-1.3: Acessar o Histórico de Propostas da Sessão**: Como um usuário, quero ver uma lista simples das propostas que gerei durante minha sessão atual, para poder revisitar e comparar os resultados.

**4. Arquitetura e Requisitos Não-Funcionais para o Épico 1**

- **Stack:** Backend em **Node.js**, Frontend em **ReactJS**.
- **Infraestrutura:** Implantação em PaaS (Vercel/Heroku), sem contêineres.
- **Estratégia de Persistência:**
    - Toda a lógica de negócio **DEVE** usar o **Repository Pattern**.
    - O histórico de propostas da sessão (US-1.3) será implementado com um **repositório em memória (mock)**.
    - Os prompts e o template da proposta serão **fixos (hardcoded)** no código-fonte do backend.

---

### **ÉPICO 2 (Pós-MVP): A Bancada de Edição - Aumentando o Engajamento**

**1. Objetivo do Épico**
Após validar a geração, o próximo passo é aumentar a utilidade da ferramenta, permitindo que os usuários façam ajustes finos sem sair da plataforma, transformando-a de um simples "gerador" para uma "bancada de trabalho".

**2. Hipótese a Validar**
Acreditamos que a adição de um editor de texto simples aumentará significativamente o tempo de sessão e a satisfação do usuário, validando que existe a necessidade de um fluxo de trabalho mais integrado.

**3. Requisitos Funcionais do Épico 2**

- **US-2.1: Editar a Proposta na Plataforma**: Como um Engenheiro de Vendas, após a geração da proposta, quero poder editar o texto diretamente na interface, utilizando um editor de texto simples (suporte para negrito, itálico, bullet points), para corrigir erros e refinar o conteúdo antes de exportar.

**4. Arquitetura e Requisitos Não-Funcionais para o Épico 2**

- **Frontend:** A implementação da US-2.1 exigirá a integração de uma biblioteca de editor de texto rico (ex: TipTap, Draft.js).
- **Backend:** Nenhuma mudança arquitetônica significativa é necessária. A lógica de edição será contida no estado do frontend.

---

### **ÉPICO 3 (Pós-MVP): O Painel de Controle - Capacitando a Customização**

**1. Objetivo do Épico**
Entregar o controle da qualidade e estrutura da geração para as mãos dos usuários avançados, permitindo que a plataforma se adapte a diferentes produtos, clientes e padrões da empresa.

**2. Hipótese a Validar**
Acreditamos que os usuários avançados investirão tempo para customizar templates e prompts, validando que a plataforma pode evoluir de uma ferramenta de produtividade individual para um sistema de padronização de conhecimento da equipe.

**3. Requisitos Funcionais do Épico 3**

- **US-3.1: Gerenciar Prompts do Sistema**: Como um usuário administrador, quero uma área de configurações onde eu possa editar os prompts que a IA usa, para refinar continuamente a qualidade e o tom das propostas geradas.
- **US-3.2: Gerenciar Templates de Proposta**: Como um administrador, quero poder editar a estrutura padrão das propostas (ex: adicionar, remover ou reordenar seções), para que todas as gerações sigam o formato mais atualizado da empresa.

**4. Arquitetura e Requisitos Não-Funcionais para o Épico 3**

- **Estratégia de Persistência:**
    - Para evitar a complexidade de um banco de dados, a persistência de prompts e templates será implementada através de **repositórios que leem e escrevem em arquivos físicos no servidor** (ex: `prompts.json`, `template.md`).
    - Isso cumpre a diretriz do Repository Pattern, mantendo a arquitetura desacoplada e pronta para uma futura migração para um banco de dados.

---

### **Fora do Escopo (Roadmap Futuro)**

Os seguintes épicos serão considerados após a validação e entrega bem-sucedida das três fases iniciais:

- **ÉPICO 4: Persistência e Colaboração:** Introdução de um banco de dados real (ex: PostgreSQL), contas de usuário, histórico persistente e funcionalidades de colaboração.
- **ÉPICO 5: Analytics e Insights:** Criação de um painel para monitorar métricas de uso, qualidade das propostas e performance dos prompts.

# **Plano de Arquitetura Técnica do MVP**

**Baseado no PRD Versão:** v1.3

**1. Visão Geral da Arquitetura**

A arquitetura seguirá um modelo cliente-servidor desacoplado. O backend em Node.js exporá uma API RESTful consumida por um frontend *single-page application* (SPA) em React. Conforme ditado pelo PRD, toda a persistência de dados será abstraída através do *Repository Pattern*. Para o MVP, isso suportará uma implementação de "banco de dados" puramente em memória, garantindo que a lógica de negócio permaneça agnóstica à fonte de dados e facilitando a evolução futura do produto.

**2. Estrutura do Projeto (Estrutura de Diretórios Sugerida)**

Uma estrutura de diretórios bem definida é crucial para a manutenibilidade e escalabilidade do projeto.

- **Backend (Node.js/Express):**
    - `/src/api/`: Define as rotas (endpoints) e seus respectivos controllers.
        - `routes/`: Definições de rotas (ex: `proposal.routes.js`).
        - `controllers/`: Responsáveis por receber requisições HTTP, validar a entrada e orquestrar a resposta, chamando os serviços apropriados.
    - `/src/core/`: Lógica de negócio principal da aplicação.
        - `services/`: Contém a lógica de negócio desacoplada do Express (ex: `ProposalGenerationService.js`). É aqui que a orquestração entre os repositórios e os modelos de IA acontece.
        - `repositories/`: Define as interfaces para acesso a dados (ex: `IProposalRepository.js`).
    - `/src/infra/`: Implementações concretas da infraestrutura.
        - `repositories/`: Contém a implementação do repositório em memória (ex: `InMemoryProposalRepository.js`). Futuramente, uma implementação de banco de dados (`PostgresProposalRepository.js`) residiria aqui.
    - `/src/config/`: Contém os prompts e templates *hardcoded* para o MVP (ex: `prompts.js`, `template.md`).
- **Frontend (React):**
    - `/src/components/`: Componentes de UI reutilizáveis e "burros" (ex: `Button.jsx`, `TextArea.jsx`).
    - `/src/features/`: Componentes e lógica de negócio relacionados a uma funcionalidade específica. Para o MVP, teremos:
        - `/proposal-generator/`: O formulário de entrada, o estado dos campos e a lógica para chamar o serviço da API.
        - `/session-history/`: O componente que exibe a lista de propostas geradas na sessão.
    - `/src/services/`: Módulos responsáveis pela comunicação com a API do backend (ex: `proposalApiService.js`).
    - `/src/pages/`: Componentes que representam as páginas da aplicação, montando os *features* em um layout (ex: `HomePage.jsx`).

**3. Design da API (Contrato entre Frontend e Backend)**

Os endpoints abaixo são suficientes para atender estritamente aos requisitos do Épico 1.

- **Propostas**
    - `POST /api/proposals`
        - **Objetivo:** Gera uma nova proposta com base nos contextos fornecidos.
        - **Request Body:**
            
            ```json
            {
              "customerRequirements": "string",
              "strategicNotes": "string",
              "otherInfo": "string"
            }
            
            ```
            
        - **Response (200 OK):**
            
            ```json
            {
              "id": "unique_proposal_id",
              "generatedText": "O texto formatado da proposta em Markdown..."
            }
            
            ```
            
    - `GET /api/proposals/session/:sessionId`
        - **Objetivo:** Retorna o histórico de propostas geradas para uma determinada sessão. O `sessionId` será um identificador único gerado no frontend e passado para o backend a cada requisição.
        - **Response (200 OK):**
            
            ```json
            [
              {
                "id": "proposal_id_1",
                "summary": "Um resumo ou as primeiras 100 palavras da proposta...",
                "createdAt": "timestamp"
              },
              {
                "id": "proposal_id_2",
                "summary": "Um resumo ou as primeiras 100 palavras da proposta...",
                "createdAt": "timestamp"
              }
            ]
            
            ```
            

**4. Detalhamento da Estratégia de Dados (Mock e Futuro)**

A chave para a evolução da arquitetura é a abstração correta do acesso a dados.

- **Interface do Repositório (Exemplo para Propostas):**
A interface define o contrato que a lógica de negócio espera, independentemente da implementação.
    
    ```tsx
    // Em /src/core/repositories/IProposalRepository.js
    
    interface IProposalRepository {
      save(sessionId: string, proposal: Proposal): Promise<void>;
      findBySessionId(sessionId: string): Promise<Proposal[]>;
    }
    
    // O tipo 'Proposal' seria definido em outro lugar, ex: /src/core/domain/
    type Proposal = {
      id: string;
      generatedText: string;
      summary: string;
      createdAt: Date;
    };
    
    ```
    
- **Implementação do Mock em Memória:**
A implementação inicial usará um simples objeto JavaScript (`Map` ou `{}`) para simular o armazenamento, conforme exigido pelo PRD.
    
    ```tsx
    // Em /src/infra/repositories/InMemoryProposalRepository.js
    
    class InMemoryProposalRepository implements IProposalRepository {
      private readonly proposalsBySession: Map<string, Proposal[]> = new Map();
    
      async save(sessionId: string, proposal: Proposal): Promise<void> {
        if (!this.proposalsBySession.has(sessionId)) {
          this.proposalsBySession.set(sessionId, []);
        }
        this.proposalsBySession.get(sessionId)?.push(proposal);
      }
    
      async findBySessionId(sessionId: string): Promise<Proposal[]> {
        return this.proposalsBySession.get(sessionId) || [];
      }
    }
    
    ```
    
- **Plano de Transição:**
Para o Épico 3 (armazenamento em arquivos) e Épico 4 (banco de dados), o trabalho será criar novas classes que implementam a mesma interface `IProposalRepository`.
    - `FileProposalRepository`: Leria e escreveria em um arquivo JSON.
    - `PostgresProposalRepository`: Usaria um cliente de banco de dados (ex: Prisma ou Knex) para interagir com o PostgreSQL.
    A mudança na lógica de negócio (`ProposalGenerationService`) será mínima, limitando-se à injeção da nova implementação do repositório, validando a robustez da arquitetura.

**5. Estratégia de Qualidade e Testes**

Para o MVP, o foco é garantir que a funcionalidade principal seja robusta e confiável.

- **Ferramentas:**
    - **Backend:** Jest para testes unitários e de integração.
    - **Frontend:** React Testing Library para testes de componentes e fluxos de usuário.
    - **E2E (End-to-End):** Cypress, para um único "happy path".
- **Foco:**
    - **Backend:**
        - **Testes Unitários:** Cobertura máxima no `ProposalGenerationService` para garantir que a lógica de construção do prompt a partir das entradas e a formatação da saída estejam corretas. Mockar a chamada para a API da IA e o repositório.
        - **Testes de Integração:** Testar o endpoint `POST /api/proposals` para garantir que a requisição flua corretamente pelo `controller` e `service` até o repositório em memória.
    - **Frontend:**
        - **Testes de Componentes:** Testar o formulário de geração e o display de resultados de forma isolada.
        - **Testes de Integração:** Simular o preenchimento dos campos, o clique no botão "Gerar", mockar a chamada da API e verificar se o resultado é exibido corretamente na tela e na lista de histórico da sessão.
    - **E2E:** Um único teste crítico: carregar a página, preencher todos os campos de texto, clicar em "Gerar", aguardar o resultado, verificar se o texto aparece na área de visualização e se um item é adicionado ao histórico.

# **Backlog de Produto Refatorado (Completo)**

**Filosofia de Decomposição:** Os requisitos do PRD foram "fatiados" verticalmente em Épicos que representam incrementos de valor entregáveis e testáveis. Esta decomposição reflete a arquitetura planejada, permitindo que a equipe construa a fundação (o "encanamento" da API e da UI) primeiro, e depois adicione funcionalidades de forma incremental. Cada Épico foi projetado para ser concluído em um curto período, focando no feedback rápido para validar as hipóteses de negócio.

---

### **ÉPICO 1: O Gerador - Validando a Proposta de Valor Central (MVP)**

- **Valor para o Negócio:** Entregar o fluxo de valor completo e mínimo: inserir contexto, gerar uma proposta, visualizá-la, copiá-la e ver o histórico da sessão. Este épico valida a hipótese fundamental do produto de forma testável.
- **Dependências:** Nenhuma.

**Histórias de Usuário:**

- **US-101: Implementar o Endpoint de Geração e o Repositório em Memória (Backend)**
    - **Como um** Desenvolvedor Backend, **quero** criar o endpoint `POST /api/proposals` e o `InMemoryProposalRepository`, **para que** a proposta seja gerada via IA e salva na memória da sessão.
    - **Critérios de Aceite:**
        1. O endpoint recebe os contextos de texto e invoca o `ProposalGenerationService`.
        2. O serviço usa prompts *hardcoded* para chamar a IA.
        3. O resultado é salvo com sucesso no `InMemoryProposalRepository`.
        4. A proposta gerada é retornada na resposta da API.
- **US-102: Construir a Interface de Geração e Visualização (Frontend)**
    - **Como um** Engenheiro de Vendas, **quero** uma UI com áreas de texto, um botão "Gerar" e uma área para ver o resultado, **para que** eu possa interagir com a funcionalidade principal.
    - **Critérios de Aceite:**
        1. A UI permite a inserção dos três contextos.
        2. Clicar em "Gerar" chama o endpoint `POST /api/proposals` e exibe um estado de carregamento.
        3. O `generatedText` da resposta da API é renderizado em uma área de visualização.
- **US-103: Implementar o Endpoint de Histórico da Sessão (Backend)**
    - **Como um** Desenvolvedor Backend, **quero** criar o endpoint `GET /api/proposals/session/:sessionId`, **para que** o frontend possa consultar todas as propostas geradas na sessão atual.
    - **Critérios de Aceite:**
        1. O endpoint recupera os dados do `InMemoryProposalRepository` usando o `sessionId`.
        2. A resposta é uma lista de resumos de propostas (`{id, summary, createdAt}`).
- **US-104: Finalizar o Fluxo de Valor do Usuário (Frontend)**
    - **Como um** Engenheiro de Vendas, **quero** um botão "Copiar" e uma lista de histórico da sessão, **para que** eu possa exportar meu trabalho e comparar versões anteriores.
    - **Critérios de Aceite:**
        1. Um botão "Copiar" é funcional e copia o conteúdo da área de visualização.
        2. Um componente de histórico é exibido e é populado chamando o endpoint `GET /api/proposals/session/:sessionId` após cada geração.

---

### **ÉPICO 2: A Bancada de Edição (Pós-MVP)**

- **Valor para o Negócio:** Aumentar o engajamento, permitindo edições rápidas na plataforma para validar a hipótese de que um fluxo de trabalho integrado é preferível à exportação imediata.
- **Dependências:** Épico 1.

**Histórias de Usuário:**

- **US-201: Integrar um Editor de Texto Rico (Frontend)**
    - **Como um** Engenheiro de Vendas, **quero** que a área de visualização da proposta seja um editor de texto simples, **para que** eu possa corrigir e refinar o conteúdo gerado pela IA.
    - **Critérios de Aceite:**
        1. Uma biblioteca de editor de texto (ex: TipTap) substitui a área de visualização estática.
        2. O conteúdo gerado pela API é carregado como estado inicial do editor.
        3. Funcionalidades básicas (negrito, itálico, listas) estão disponíveis.
        4. A função "Copiar" é atualizada para usar o conteúdo *editado* do editor.

---

### **ÉPICO 3: O Painel de Controle (Pós-MVP)**

- **Valor para o Negócio:** Capacitar usuários avançados a refinar a qualidade da IA, validando a hipótese de demanda por customização e transformando a ferramenta em um sistema de conhecimento.
- **Dependências:** Épico 1.

**Histórias de Usuário:**

- **US-301: Implementar Persistência de Configurações em Arquivo (Backend)**
    - **Como um** Desenvolvedor Backend, **quero** criar repositórios baseados em arquivos (ex: `FileConfigRepository`) e endpoints (`GET/PUT /api/config`), **para que** as customizações de prompts e templates possam ser salvas no servidor.
    - **Critérios de Aceite:**
        1. O novo repositório lê e escreve em arquivos como `prompts.json` e `template.md`.
        2. O `ProposalGenerationService` é refatorado para ler as configurações deste repositório.
        3. Os endpoints para gerenciar as configurações são criados e funcionais.
- **US-302: Construir a Interface de Gerenciamento de Configurações (Frontend)**
    - **Como um** usuário administrador, **quero** uma página de "Configurações" para editar os prompts e o template da proposta, **para que** eu possa controlar a estrutura e o tom das gerações.
    - **Critérios de Aceite:**
        1. Uma nova página de "Configurações" é criada.
        2. A página carrega os dados atuais do endpoint `GET /api/config`.
        3. O usuário pode modificar os prompts e o template em áreas de texto.
        4. Um botão "Salvar" envia os novos dados para o endpoint `PUT /api/config`.

---

### **ÉPICO 4: Persistência e Colaboração (Roadmap Futuro)**

- **Valor para o Negócio:** Transformar a ferramenta de um utilitário de sessão única em uma plataforma robusta com memória persistente, contas de usuário e a base para o trabalho em equipe.
- **Dependências:** Épico 1.

**Histórias de Usuário:**

- **US-401: Implementar Autenticação e Persistência de Usuário (Backend)**
    - **Como um** Desenvolvedor Backend, **quero** integrar um banco de dados (ex: PostgreSQL), adicionar tabelas de `User` e `Proposal` e criar endpoints de registro/login, **para que** os usuários possam ter contas persistentes.
    - **Critérios de Aceite:**
        1. O banco de dados está configurado e acessível via ORM (ex: Prisma).
        2. Endpoints `POST /api/auth/register` e `POST /api/auth/login` são criados.
        3. Um token JWT é retornado no login para autenticar requisições subsequentes.
- **US-402: Refatorar a Persistência de Propostas (Backend)**
    - **Como um** Desenvolvedor Backend, **quero** substituir o repositório em memória/arquivo por um `PostgresProposalRepository`, **para que** as propostas sejam salvas permanentemente e associadas a um usuário.
    - **Critérios de Aceite:**
        1. A nova classe de repositório implementa a mesma interface `IProposalRepository`.
        2. O endpoint `POST /api/proposals` agora exige autenticação e salva a proposta no banco de dados com o `userId`.
        3. O endpoint de histórico é atualizado para retornar todas as propostas do usuário autenticado.
- **US-403: Construir Fluxos de Autenticação e Histórico Persistente (Frontend)**
    - **Como um** usuário, **quero** me registrar, fazer login/logout e ver todo o meu histórico de propostas, **para que** eu possa usar a plataforma de forma segura e contínua.
    - **Critérios de Aceite:**
        1. Páginas de Login e Registro são criadas.
        2. O cliente salva o token JWT e o envia nos cabeçalhos das requisições autenticadas.
        3. A página de histórico é refatorada para exibir todos os registros do usuário logado.

---

### **ÉPICO 5: Analytics e Insights (Roadmap Futuro)**

- **Valor para o Negócio:** Fornecer dados sobre o uso e a eficácia da ferramenta, permitindo que as equipes meçam o ROI e identifiquem oportunidades de melhoria nos prompts e templates.
- **Dependências:** Épico 4 (dados persistentes e usuários são necessários para gerar métricas).

**Histórias de Usuário:**

- **US-501: Criar Endpoints de Métricas de Uso (Backend)**
    - **Como um** Desenvolvedor Backend, **quero** criar endpoints de analytics (ex: GET /api/analytics/usage) que agreguem métricas de uso, **para que** o frontend possa exibi-las.
    - **Critérios de Aceite:**
        1. O endpoint retorna estatísticas como: número total de propostas geradas, propostas por usuário, média de gerações por dia.
        2. Os cálculos são eficientes e não sobrecarregam o banco de dados.
- **US-502: Construir o Painel de Métricas de Uso (Frontend)**
    - **Como um** usuário administrador, **quero** uma página de "Analytics" com gráficos sobre o uso, **para que** eu possa entender como a plataforma está sendo adotada.
    - **Critérios de Aceite:**
        1. Uma nova página de "Analytics" é adicionada à aplicação.
        2. A página consome os dados do endpoint de analytics e exibe as métricas de uso de forma clara.
- **US-503: Implementar um Mecanismo de Feedback de Qualidade (Frontend/Backend)**
    - **Como um** Engenheiro de Vendas, **quero** ter botões simples (ex: "👍 Útil" / "👎 Não útil") após cada geração, **para que** eu possa dar um feedback rápido sobre a qualidade do resultado.
    - **Critérios de Aceite:**
        1. (Frontend) Os botões de feedback são exibidos na UI após a geração de uma proposta.
        2. (Backend) Um novo endpoint (POST /api/proposals/:proposalId/feedback) é criado para registrar esse feedback no banco de dados, associado à proposta específica.
- **US-504: Exibir Métricas de Qualidade e Performance de Prompts (Frontend/Backend)**
    - **Como um** usuário administrador, **quero** ver no painel de "Analytics" a pontuação de qualidade média das propostas e quais prompts estão performando melhor, **para que** eu possa tomar decisões baseadas em dados para refinar a IA.
    - **Critérios de Aceite:**
        1. (Backend) O endpoint de analytics é expandido para calcular e retornar a taxa de feedback positivo/negativo.
        2. (Se aplicável após o Épico 3) O endpoint correlaciona o feedback com a versão do prompt usada na geração.
        3. (Frontend) O painel de Analytics é atualizado para exibir essas novas métricas de qualidade.

# Épico [1]

## US [101]

### **Plano de Implementação da História: US-101: Implementar o Endpoint de Geração e o Repositório em Memória (Backend)**

**Épico:** O Gerador - Validando a Proposta de Valor Central (MVP)
**História de Usuário:**

- **Como um** Desenvolvedor Backend, **quero** criar o endpoint `POST /api/proposals` e o `InMemoryProposalRepository`, **para que** a proposta seja gerada via IA e salva na memória da sessão.
- **Critérios de Aceite:**
    1. O endpoint recebe os contextos de texto e invoca o `ProposalGenerationService`.
    2. O serviço usa prompts *hardcoded* para chamar a IA.
    3. O resultado é salvo com sucesso no `InMemoryProposalRepository`.
    4. A proposta gerada é retornada na resposta da API.

---

### **1. Tarefas Técnicas (Technical Tasks)**

| Camada/Área | Tarefa Específica (Sub-task) | Detalhes Técnicos (Conforme Arquitetura) |
| --- | --- | --- |
| **Backend (Core/Infra)** | **BE-1:** Definir a Interface do Repositório e o Domínio. | Criar o arquivo `/src/core/repositories/IProposalRepository.js` com a interface (`save`, `findBySessionId`). Definir o tipo/classe `Proposal` em `/src/core/domain/`. |
|  | **BE-2:** Implementar o Repositório em Memória. | Criar a classe `InMemoryProposalRepository` em `/src/infra/repositories/` que implementa `IProposalRepository`. Utilizar um `Map` para armazenar as propostas por `sessionId`. |
|  | **BE-3:** Configurar Prompts e Templates. | Criar arquivos de configuração em `/src/config/` (ex: `prompts.js`) para armazenar os prompts e o template da proposta que serão usados pelo serviço. |
| **Backend (Core)** | **BE-4:** Implementar a lógica no `ProposalGenerationService`. | Criar o arquivo `/src/core/services/ProposalGenerationService.js`. A classe deve receber o repositório via injeção de dependência. O método principal irá: 1) Ler os prompts do config. 2) Construir o prompt final com as entradas do usuário. 3) **Simular/Mockar a chamada para a API da IA** e retornar um texto de exemplo. 4) Criar um objeto `Proposal` com `id`, `generatedText`, etc. 5) Chamar `repository.save()` para persistir os dados. 6) Retornar o objeto `Proposal`. |
| **Backend (API)** | **BE-5:** Criar o Controller `ProposalController`. | Criar o arquivo `/src/api/controllers/ProposalController.js`. O método do controller deve: 1) Extrair os dados (`customerRequirements`, etc.) e o `sessionId` do request. 2) Adicionar validação de entrada (ex: garantir que os campos não são vazios). 3) Chamar o `ProposalGenerationService`. 4) Formatar a resposta HTTP com os dados retornados pelo serviço, conforme o contrato da API. |
|  | **BE-6:** Criar o endpoint `POST /api/proposals`. | No arquivo de rotas `/src/api/routes/proposal.routes.js`, definir a rota `POST /proposals` e conectá-la ao método do `ProposalController`. |
| **Testes** | **TEST-1:** Escrever testes unitários para `InMemoryProposalRepository`. | Verificar se os métodos `save` e `findBySessionId` funcionam corretamente, incluindo casos de sessões novas e existentes. |
|  | **TEST-2:** Escrever testes unitários para `ProposalGenerationService`. | Testar a lógica de negócio de forma isolada. **Mockar o repositório** e a chamada da IA. Verificar se o método de salvar do repositório é chamado com os dados corretos. |
|  | **TEST-3:** Escrever teste de integração para o endpoint. | Usando `Jest` e `supertest`, criar um teste que faça uma chamada HTTP real para o endpoint `POST /api/proposals`. Verificar se o código de status é 200/201 e se o corpo da resposta corresponde ao contrato definido na arquitetura. |

---

### **2. Checklist de Definition of Done (DoD)**

- [ ]  Todas as tarefas técnicas (BE, TEST) listadas acima foram concluídas.
- [ ]  O código foi formatado e passou pelas verificações do linter.
- [ ]  Todos os testes unitários e de integração relevantes para a história estão passando no pipeline de CI, com cobertura de código dentro do limiar aceitável.
- [ ]  O Pull Request (PR) foi criado na branch `develop`/`main`, seguindo o template do projeto.
- [ ]  O PR foi revisado e aprovado por, no mínimo, um outro membro da equipe de desenvolvimento.
- [ ]  Todas as sugestões e comentários levantados durante o code review foram resolvidos.
- [ ]  A funcionalidade foi mesclada na branch principal de desenvolvimento após a aprovação.
- [ ]  A documentação da API (ex: Postman, Swagger) foi atualizada para refletir o novo endpoint.
- [ ]  A funcionalidade foi verificada manualmente por meio de uma ferramenta de API (como Postman ou Insomnia) para garantir que atende a todos os critérios de aceite.

## US [102]

### **Plano de Implementação da História: US-102: Construir a Interface de Geração e Visualização (Frontend)**

**Épico:** O Gerador - Validando a Proposta de Valor Central (MVP)
**História de Usuário:**

- **Como um** Engenheiro de Vendas, **quero** uma UI com áreas de texto, um botão "Gerar" e uma área para ver o resultado, **para que** eu possa interagir com a funcionalidade principal.
- **Critérios de Aceite:**
    1. A UI permite a inserção dos três contextos.
    2. Clicar em "Gerar" chama o endpoint `POST /api/proposals` e exibe um estado de carregamento.
    3. O `generatedText` da resposta da API é renderizado em uma área de visualização.

---

### **1. Tarefas Técnicas (Technical Tasks)**

| Camada/Área | Tarefa Específica (Sub-task) | Detalhes Técnicos (Conforme Arquitetura) |
| --- | --- | --- |
| **Frontend (React)** | **FE-1:** Criar componentes de UI genéricos. | Em `/src/components/`, criar componentes reutilizáveis, se ainda não existirem: `TextArea.jsx` e `Button.jsx`, focados em receber props e renderizar a UI. |
|  | **FE-2:** Estruturar o componente da funcionalidade `ProposalGenerator`. | Criar o arquivo `/src/features/proposal-generator/ProposalGenerator.jsx`. Este componente irá importar e usar os componentes de UI genéricos para montar o formulário com as três áreas de texto e o botão. |
|  | **FE-3:** Implementar o gerenciamento de estado local. | Dentro do `ProposalGenerator.jsx`, usar o hook `useState` para gerenciar: 1) o estado dos três campos de texto, 2) o estado de carregamento (`isLoading`), 3) o estado de erro (`error`), e 4) o resultado (`generatedText`). |
|  | **FE-4:** Implementar a chamada de serviço para a API. | Criar/atualizar o arquivo `/src/services/proposalApiService.js`. Adicionar uma função assíncrona `generateProposal(data)` que usa `axios` ou `fetch` para enviar uma requisição `POST` para `/api/proposals` com o corpo da requisição esperado. |
|  | **FE-5:** Orquestrar o fluxo de interação na UI. | No `ProposalGenerator.jsx`, criar a função `handleSubmit`. Ao ser acionada pelo clique no botão: 1) Definir `isLoading` como `true`. 2) Chamar o `proposalApiService.generateProposal`. 3) No sucesso, atualizar o estado `generatedText` com a resposta. 4) No erro, popular o estado `error`. 5) Em ambos os casos, definir `isLoading` como `false` no final. |
|  | **FE-6:** Renderizar o resultado e os estados da UI. | No JSX do `ProposalGenerator.jsx`, implementar a renderização condicional: 1) Exibir um spinner ou mensagem de "Gerando..." quando `isLoading` for `true`. 2) Desabilitar o botão "Gerar" durante o carregamento. 3) Exibir uma mensagem de erro se o estado `error` estiver preenchido. 4) Renderizar o conteúdo de `generatedText` em uma área de visualização (ex: `<div>` ou `<pre>`). |
|  | **FE-7:** Integrar o feature na página principal. | No arquivo `/src/pages/HomePage.jsx`, importar e renderizar o componente `<ProposalGenerator />` para que ele seja a primeira coisa que o usuário veja. |
| **Testes** | **TEST-1:** Escrever testes de componente para `ProposalGenerator`. | Usando a `React Testing Library`, testar a renderização inicial: verificar se os três `textarea` e o botão estão presentes na tela. |
|  | **TEST-2:** Escrever testes de integração do fluxo de UI. | Ainda com a `React Testing Library`, simular a interação do usuário: 1) Digitar texto nos campos. 2) Clicar no botão. 3) **Mockar o `proposalApiService`** para simular respostas de sucesso e erro. 4) Verificar se o estado de carregamento é exibido. 5) Verificar se o texto de resultado é renderizado no sucesso. 6) Verificar se a mensagem de erro aparece na falha. |

---

### **2. Checklist de Definition of Done (DoD)**

- [ ]  Todas as tarefas técnicas (FE, TEST) listadas acima foram concluídas.
- [ ]  O código foi formatado e passou pelas verificações do linter.
- [ ]  Todos os testes de componente e integração estão passando no pipeline de CI, atendendo aos padrões de cobertura definidos para o projeto.
- [ ]  O Pull Request (PR) foi criado, descrevendo claramente o que foi implementado e como testar.
- [ ]  O código foi revisado e aprovado por pelo menos um outro desenvolvedor da equipe.
- [ ]  A funcionalidade foi mesclada na branch principal de desenvolvimento (`develop` ou `main`).
- [ ]  A interface foi verificada manualmente em um ambiente de Staging/QA para garantir que a experiência do usuário está fluida e que todos os critérios de aceite são atendidos.
- [ ]  A UI é responsiva e se apresenta de forma aceitável em resoluções de desktop comuns.

## US [103]

### **Plano de Implementação da História: US-103: Implementar o Endpoint de Histórico da Sessão (Backend)**

**Épico:** O Gerador - Validando a Proposta de Valor Central (MVP)
**História de Usuário:**

- **Como um** Desenvolvedor Backend, **quero** criar o endpoint `GET /api/proposals/session/:sessionId`, **para que** o frontend possa consultar todas as propostas geradas na sessão atual.
- **Critérios de Aceite:**
    1. O endpoint recupera os dados do `InMemoryProposalRepository` usando o `sessionId`.
    2. A resposta é uma lista de resumos de propostas (`{id, summary, createdAt}`).

---

### **1. Tarefas Técnicas (Technical Tasks)**

| Camada/Área | Tarefa Específica (Sub-task) | Detalhes Técnicos (Conforme Arquitetura) |
| --- | --- | --- |
| **Backend (Core)** | **BE-1:** Implementar a lógica de serviço para o histórico. | No `ProposalGenerationService` (ou um novo `ProposalHistoryService`), criar um método `getHistoryBySession(sessionId)`. Este método deve: 1) Chamar `repository.findBySessionId(sessionId)`. 2) Mapear a lista de objetos `Proposal` completos para uma lista de resumos, retornando apenas os campos `{id, summary, createdAt}` para cada item. |
| **Backend (API)** | **BE-2:** Implementar o método no `ProposalController`. | Adicionar um novo método, como `getSessionHistory`, ao `ProposalController`. Ele deve: 1) Extrair o `sessionId` dos parâmetros da rota (`req.params`). 2) Invocar o método de serviço criado na tarefa anterior. 3) Enviar o array de resumos retornado como a resposta JSON da API. |
|  | **BE-3:** Criar o endpoint `GET /api/proposals/session/:sessionId`. | No arquivo `/src/api/routes/proposal.routes.js`, adicionar a nova rota `GET '/session/:sessionId'` e vinculá-la ao método `getSessionHistory` no `ProposalController`. |
| **Testes** | **TEST-1:** Escrever teste unitário para o método do serviço. | Usando Jest, criar um teste para `getHistoryBySession`. **Mockar o repositório** para retornar um array de objetos `Proposal` de teste. Verificar se o método do serviço retorna um array contendo apenas os campos `{id, summary, createdAt}`. |
|  | **TEST-2:** Escrever teste de integração para o endpoint. | Usando Jest e `supertest`: 1) Pré-popular o `InMemoryProposalRepository` com dados de teste para uma `sessionId` conhecida. 2) Fazer uma requisição HTTP `GET` para `/api/proposals/session/:sessionId_com_dados`. 3) Verificar se o status da resposta é 200 e se o corpo contém o array de resumos esperado. 4) Fazer uma requisição para uma `sessionId` que não existe e verificar se a resposta é 200 com um array vazio. |

---

### **2. Checklist de Definition of Done (DoD)**

- [ ]  Todas as tarefas técnicas (BE, TEST) listadas acima foram concluídas.
- [ ]  O código foi formatado e passou pelas verificações do linter.
- [ ]  Todos os testes unitários e de integração relevantes para a história estão passando no pipeline de CI.
- [ ]  O Pull Request (PR) foi criado, descrevendo as mudanças e como elas atendem aos critérios de aceite.
- [ ]  O código foi revisado e aprovado por pelo menos um outro desenvolvedor da equipe.
- [ ]  Todas as sugestões e comentários levantados durante o code review foram resolvidos.
- [ ]  A funcionalidade foi mesclada na branch principal de desenvolvimento (`develop` ou `main`).
- [ ]  A documentação da API (ex: Postman Collection) foi atualizada para incluir o novo endpoint.
- [ ]  O endpoint foi verificado manualmente (usando Postman ou Insomnia) para garantir que ele retorna os dados corretos após a criação de algumas propostas via `POST /api/proposals`.

## US [104]

### **Plano de Implementação da História: US-104: Finalizar o Fluxo de Valor do Usuário (Frontend)**

**Épico:** O Gerador - Validando a Proposta de Valor Central (MVP)
**História de Usuário:**

- **Como um** Engenheiro de Vendas, **quero** um botão "Copiar" e uma lista de histórico da sessão, **para que** eu possa exportar meu trabalho e comparar versões anteriores.
- **Critérios de Aceite:**
    1. Um botão "Copiar" é funcional e copia o conteúdo da área de visualização.
    2. Um componente de histórico é exibido e é populado chamando o endpoint `GET /api/proposals/session/:sessionId` após cada geração.

---

### **1. Tarefas Técnicas (Technical Tasks)**

| Camada/Área | Tarefa Específica (Sub-task) | Detalhes Técnicos (Conforme Arquitetura) |
| --- | --- | --- |
| **Frontend (React)** | **FE-1:** Implementar a funcionalidade "Copiar". | No componente `/src/features/proposal-generator/ProposalGenerator.jsx`, adicionar um botão "Copiar". Implementar um handler `onClick` que usa `navigator.clipboard.writeText()` para copiar o conteúdo do estado `generatedText` para a área de transferência. |
|  | **FE-2:** Adicionar feedback visual para a ação de copiar. | No mesmo componente, adicionar um estado (ex: `isCopied`). Ao clicar em "Copiar", mudar o estado para `true` (ex: mudando o texto do botão para "Copiado!"). Usar um `setTimeout` para reverter o estado para `false` após 2 segundos. |
|  | **FE-3:** Criar o componente de UI para o histórico (`SessionHistory`). | Criar o arquivo `/src/features/session-history/SessionHistory.jsx`. Este componente deve receber um array de itens de histórico como `props` e renderizar uma lista (`<ul>`, `<li>`) exibindo o `summary` e `createdAt` de cada item. |
|  | **FE-4:** Implementar a chamada de serviço para buscar o histórico. | No arquivo `/src/services/proposalApiService.js`, adicionar uma função assíncrona `getSessionHistory(sessionId)` que faz uma requisição `GET` para `/api/proposals/session/:sessionId` e retorna a lista de histórico. |
|  | **FE-5:** Gerenciar o estado do histórico na página principal. | No componente `/src/pages/HomePage.jsx`, adicionar um estado para armazenar a lista de histórico (ex: `const [historyItems, setHistoryItems] = useState([])`). |
|  | **FE-6:** Orquestrar a atualização do histórico. | 1. Passar uma função de callback (ex: `onGenerationSuccess`) de `HomePage.jsx` para `ProposalGenerator.jsx`. 2. Em `ProposalGenerator.jsx`, invocar essa callback após a chamada de `POST /api/proposals` ser bem-sucedida. 3. Em `HomePage.jsx`, a função de callback irá disparar a chamada ao `getSessionHistory` e atualizar o estado `historyItems` com o resultado. |
|  | **FE-7:** Integrar o componente de histórico na página. | No `HomePage.jsx`, renderizar o componente `<SessionHistory />`, passando o estado `historyItems` como prop. Posicionar o componente na layout da página (ex: em uma barra lateral ou abaixo do gerador). |
| **Testes** | **TEST-1:** Escrever testes de UI para a funcionalidade "Copiar". | Na suíte de testes do `ProposalGenerator`, simular o clique no botão "Copiar". Mockar o `navigator.clipboard` e verificar se `writeText` foi chamado com o texto correto. Verificar também se o feedback visual (texto do botão) aparece e desaparece como esperado. |
|  | **TEST-2:** Escrever teste de componente para `SessionHistory`. | Criar um teste para o componente `SessionHistory.jsx`. Passar um array de dados de histórico mockados como prop e verificar se a lista é renderizada corretamente na tela. |
|  | **TEST-3:** Escrever teste de integração para o fluxo de atualização do histórico. | Na suíte de testes da `HomePage`, renderizar o componente. Mockar as chamadas de API para `generateProposal` e `getSessionHistory`. Simular um clique bem-sucedido no botão "Gerar" e verificar se a função `getSessionHistory` foi chamada e se o componente `SessionHistory` foi atualizado com os novos dados mockados. |

---

### **2. Checklist de Definition of Done (DoD)**

- [ ]  Todas as tarefas técnicas (FE, TEST) listadas acima foram concluídas.
- [ ]  O código foi formatado e passou pelas verificações do linter.
- [ ]  Todos os testes de componente e integração estão passando no pipeline de CI, atendendo aos padrões de cobertura do projeto.
- [ ]  O Pull Request (PR) foi criado, descrevendo as funcionalidades implementadas e como elas podem ser testadas.
- [ ]  O código foi revisado e aprovado por pelo menos um outro desenvolvedor da equipe.
- [ ]  A funcionalidade foi mesclada na branch principal de desenvolvimento.
- [ ]  A funcionalidade completa do MVP (gerar, visualizar, copiar e ver histórico) foi verificada manualmente de ponta-a-ponta em um ambiente de Staging/QA, confirmando que o fluxo de valor do usuário está completo e funcional.
- [ ]  A UI se apresenta de forma coesa e sem quebras visuais em resoluções de desktop padrão.

# Épico [2]

## US [201]

### **Plano de Implementação da História: US-201: Integrar um Editor de Texto Rico (Frontend)**

**Épico:** A Bancada de Edição (Pós-MVP)
**História de Usuário:**

- **Como um** Engenheiro de Vendas, **quero** que a área de visualização da proposta seja um editor de texto simples, **para que** eu possa corrigir e refinar o conteúdo gerado pela IA.
- **Critérios de Aceite:**
    1. Uma biblioteca de editor de texto (ex: TipTap) substitui a área de visualização estática.
    2. O conteúdo gerado pela API é carregado como estado inicial do editor.
    3. Funcionalidades básicas (negrito, itálico, listas) estão disponíveis.
    4. A função "Copiar" é atualizada para usar o conteúdo *editado* do editor.

---

### **1. Tarefas Técnicas (Technical Tasks)**

| Camada/Área | Tarefa Específica (Sub-task) | Detalhes Técnicos (Conforme Arquitetura) |
| --- | --- | --- |
| **Frontend (React)** | **FE-1:** Pesquisar e instalar a biblioteca do editor. | Escolher e instalar a biblioteca de editor (ex: `tiptap-react`, `prosemirror`, `draft-js`). Adicionar as dependências necessárias ao `package.json`. |
|  | **FE-2:** Criar um componente wrapper `RichTextEditor.jsx`. | Em `/src/components/`, criar um novo componente que encapsula a lógica do TipTap. Ele deve receber o conteúdo inicial via `props` e expor uma maneira de obter o conteúdo atualizado (ex: via callback `onChange` ou `ref`). |
|  | **FE-3:** Implementar a barra de ferramentas de formatação. | Dentro do wrapper `RichTextEditor.jsx`, criar uma pequena barra de ferramentas com botões para "Negrito", "Itálico" e "Lista". Conectar os eventos `onClick` desses botões aos comandos correspondentes da API do editor (ex: `editor.chain().focus().toggleBold().run()`). |
|  | **FE-4:** Integrar o editor na feature `ProposalGenerator`. | No `/src/features/proposal-generator/ProposalGenerator.jsx`, substituir a `<div>` ou `<pre>` que exibe o `generatedText` pelo novo componente `<RichTextEditor />`. |
|  | **FE-5:** Sincronizar o estado da API com o editor. | Usar o hook `useEffect` no `ProposalGenerator.jsx` para, sempre que o `generatedText` (vindo da API) for atualizado, passar esse novo conteúdo para o componente `RichTextEditor`, reiniciando seu estado. |
|  | **FE-6:** Refatorar a funcionalidade "Copiar". | Modificar a função `handleCopy` no `ProposalGenerator.jsx`. Em vez de ler do estado `generatedText`, ela agora precisa obter o conteúdo HTML ou texto atual do componente editor (provavelmente através de uma `ref`) e passá-lo para o `navigator.clipboard`. |
| **Backend (Node.js)** | **N/A** | Nenhuma tarefa de backend é necessária para esta história, conforme especificado na arquitetura. Toda a lógica de edição é contida no estado do frontend. |
| **Testes** | **TEST-1:** Escrever testes de componente para `RichTextEditor`. | Usando a `React Testing Library`, criar testes para o wrapper. Verificar se ele renderiza o conteúdo inicial passado via `props` e se os botões da barra de ferramentas estão presentes. |
|  | **TEST-2:** Atualizar os testes de integração de `ProposalGenerator`. | Na suíte de testes do `ProposalGenerator`, modificar os testes existentes: 1) Verificar se o componente `RichTextEditor` é renderizado após uma chamada de API mockada. 2) Atualizar o teste da função "Copiar" para verificar se o conteúdo *editado* (que pode ser definido programaticamente no editor mockado) é o que está sendo copiado. |

---

### **2. Checklist de Definition of Done (DoD)**

- [ ]  Todas as tarefas técnicas (FE, TEST) listadas acima foram concluídas.
- [ ]  O código foi formatado e passou pelas verificações do linter.
- [ ]  Todos os testes de componente e integração estão passando no pipeline de CI, com a cobertura de código mantida ou aumentada.
- [ ]  O Pull Request (PR) foi criado, descrevendo as mudanças, a biblioteca escolhida e como testar a nova funcionalidade de edição.
- [ ]  O código foi revisado e aprovado por pelo menos um outro desenvolvedor, com atenção especial à nova dependência adicionada.
- [ ]  A funcionalidade foi mesclada na branch principal de desenvolvimento.
- [ ]  A funcionalidade foi verificada manualmente em um ambiente de Staging/QA:
    - [ ]  A edição de texto (digitar, apagar) funciona.
    - [ ]  As opções de formatação (negrito, itálico, lista) funcionam.
    - [ ]  O botão "Copiar" copia o conteúdo *depois* de ter sido editado.
    - [ ]  Gerar uma nova proposta limpa o editor e carrega o novo conteúdo corretamente.

# Épico [3]

## US [301]

### **Plano de Implementação da História: US-301: Implementar Persistência de Configurações em Arquivo (Backend)**

**Épico:** O Painel de Controle (Pós-MVP)
**História de Usuário:**

- **Como um** Desenvolvedor Backend, **quero** criar repositórios baseados em arquivos (ex: `FileConfigRepository`) e endpoints (`GET/PUT /api/config`), **para que** as customizações de prompts e templates possam ser salvas no servidor.
- **Critérios de Aceite:**
    1. O novo repositório lê e escreve em arquivos como `prompts.json` e `template.md`.
    2. O `ProposalGenerationService` é refatorado para ler as configurações deste repositório.
    3. Os endpoints para gerenciar as configurações são criados e funcionais.

---

### **1. Tarefas Técnicas (Technical Tasks)**

| Camada/Área | Tarefa Específica (Sub-task) | Detalhes Técnicos (Conforme Arquitetura) |
| --- | --- | --- |
| **Backend (Core/Infra)** | **BE-1:** Definir a Interface do Repositório de Configuração. | Criar o arquivo `/src/core/repositories/IConfigRepository.js`. A interface deve definir métodos como `getPrompts(): Promise<object>` e `savePrompts(data: object): Promise<void>`, além de métodos análogos para o template. |
|  | **BE-2:** Implementar o Repositório de Arquivo (`FileConfigRepository`). | Em `/src/infra/repositories/`, criar `FileConfigRepository.js` que implementa `IConfigRepository`. Usar o módulo `fs/promises` do Node.js para: 1) Ler `prompts.json` e fazer `JSON.parse`. 2) Ler `template.md` como texto. 3) Escrever nos mesmos arquivos, usando `JSON.stringify` para o JSON. |
|  | **BE-3:** Migrar os prompts e template iniciais para arquivos. | Mover os prompts e o template que estavam em `/src/config/` para arquivos físicos (ex: `/data/prompts.json`, `/data/template.md`) que servirão como a fonte de dados inicial para o `FileConfigRepository`. |
| **Backend (Core)** | **BE-4:** Refatorar o `ProposalGenerationService`. | Modificar o `ProposalGenerationService` para receber a implementação do `IConfigRepository` via injeção de dependência. Em vez de ler do diretório `/config/`, o serviço agora deve chamar `configRepository.getPrompts()` e `configRepository.getTemplate()` para obter os dados necessários para a geração. |
| **Backend (API)** | **BE-5:** Criar o `ConfigController` e o `ConfigService`. | Criar um novo serviço (`ConfigService`) e um novo controller (`ConfigController`). O serviço irá orquestrar as chamadas para o `FileConfigRepository` para buscar (`get`) e salvar (`update`) as configurações. |
|  | **BE-6:** Criar os endpoints `GET` e `PUT` para configurações. | Criar um novo arquivo de rotas `/src/api/routes/config.routes.js`. Definir a rota `GET /api/config` e `PUT /api/config`, conectando-as aos métodos correspondentes no `ConfigController`. O corpo do `PUT` deve ser validado para garantir que os campos esperados estão presentes. |
| **Testes** | **TEST-1:** Escrever testes unitários para `FileConfigRepository`. | Usando `jest`, mockar o módulo `fs/promises` para testar a lógica de leitura e escrita do repositório sem tocar no sistema de arquivos real. Verificar se a formatação (JSON/texto) está correta. |
|  | **TEST-2:** Atualizar testes unitários do `ProposalGenerationService`. | Modificar os testes existentes para mockar o `IConfigRepository` em vez de mockar os arquivos de config. Garantir que o serviço chame os métodos corretos do repositório. |
|  | **TEST-3:** Escrever testes de integração para os novos endpoints. | Usando `supertest`, criar testes para: 1) Chamar `GET /api/config` e verificar se os dados dos arquivos de teste são retornados. 2) Chamar `PUT /api/config` com novos dados, depois chamar `GET` novamente para garantir que os dados foram persistidos (escritos no arquivo de teste). |

---

### **2. Checklist de Definition of Done (DoD)**

- [ ]  Todas as tarefas técnicas (BE, TEST) listadas acima foram concluídas.
- [ ]  O código foi formatado e passou pelas verificações do linter.
- [ ]  Todos os testes unitários e de integração relevantes estão passando no pipeline de CI, com cobertura de código mantida ou aumentada.
- [ ]  O Pull Request (PR) foi criado, descrevendo a nova arquitetura de persistência de configuração e como ela funciona.
- [ ]  O código foi revisado e aprovado por pelo menos um outro membro da equipe, com atenção especial à refatoração do `ProposalGenerationService`.
- [ ]  A funcionalidade foi mesclada na branch principal de desenvolvimento.
- [ ]  A documentação da API foi atualizada para incluir os novos endpoints `GET` e `PUT` de `/api/config`.
- [ ]  Os endpoints foram verificados manualmente via Postman/Insomnia para confirmar que:
    - [ ]  `GET` retorna as configurações atuais.
    - [ ]  `PUT` atualiza as configurações nos arquivos `prompts.json` e `template.md`.
    - [ ]  O endpoint `POST /api/proposals` agora utiliza as configurações dos arquivos, e não mais os valores *hardcoded*.

## US [302]

### **Plano de Implementação da História: US-302: Construir a Interface de Gerenciamento de Configurações (Frontend)**

**Épico:** O Painel de Controle (Pós-MVP)
**História de Usuário:**

- **Como um** usuário administrador, **quero** uma página de "Configurações" para editar os prompts e o template da proposta, **para que** eu possa controlar a estrutura e o tom das gerações.
- **Critérios de Aceite:**
    1. Uma nova página de "Configurações" é criada.
    2. A página carrega os dados atuais do endpoint `GET /api/config`.
    3. O usuário pode modificar os prompts e o template em áreas de texto.
    4. Um botão "Salvar" envia os novos dados para o endpoint `PUT /api/config`.

---

### **1. Tarefas Técnicas (Technical Tasks)**

| Camada/Área | Tarefa Específica (Sub-task) | Detalhes Técnicos (Conforme Arquitetura) |
| --- | --- | --- |
| **Frontend (React)** | **FE-1:** Adicionar as funções de serviço para a API de configuração. | No arquivo `/src/services/proposalApiService.js` (ou um novo `configApiService.js`), adicionar duas funções: `getConfig()` para a requisição `GET` e `updateConfig(data)` para a requisição `PUT`. |
|  | **FE-2:** Criar a estrutura da página de Configurações. | Criar um novo arquivo de página em `/src/pages/SettingsPage.jsx`. Configurar o roteamento da aplicação para que essa página seja acessível (ex: através de um link no menu de navegação). |
|  | **FE-3:** Implementar o carregamento inicial dos dados. | No `SettingsPage.jsx`, usar o hook `useEffect` para chamar `getConfig()` na montagem do componente. Armazenar os dados retornados (prompts e template) em um estado local usando `useState`. |
|  | **FE--4:** Construir os componentes do formulário de edição. | Na `SettingsPage.jsx`, renderizar os campos de formulário (`<textarea>`) para cada prompt e para o template. Os valores iniciais desses campos devem ser populados a partir do estado carregado da API. |
|  | **FE-5:** Implementar a lógica de salvamento e gerenciamento de estado. | Criar uma função `handleSave`. Ao clicar no botão "Salvar": 1) Mudar para um estado de `isLoading`. 2) Chamar `updateConfig()` com os dados atuais dos campos do formulário. 3) No sucesso, exibir uma notificação de "Salvo com sucesso". 4) Em caso de erro, exibir uma mensagem de erro. 5) Em ambos os casos, resetar o estado `isLoading`. |
| **Backend (Node.js)** | **N/A** | Nenhuma tarefa de backend é necessária, pois assume-se que a US-301 (criação dos endpoints) já foi concluída. |
| **Testes** | **TEST-1:** Escrever testes para as novas funções de serviço da API. | Criar testes unitários para `getConfig` e `updateConfig`, mockando o `axios/fetch` para garantir que as requisições corretas estão sendo feitas. |
|  | **TEST-2:** Escrever testes de integração para a `SettingsPage`. | Usando a `React Testing Library`: 1) **Mockar os serviços da API**. 2) Testar o carregamento inicial: verificar se `getConfig` é chamado e se os dados mockados populam os campos do formulário. 3) Testar o salvamento: simular a edição de um campo, clicar em "Salvar" e verificar se `updateConfig` é chamado com os dados corretos. 4) Verificar se os estados de carregamento e sucesso/erro são exibidos corretamente na UI. |

---

### **2. Checklist de Definition of Done (DoD)**

- [ ]  Todas as tarefas técnicas (FE, TEST) listadas acima foram concluídas.
- [ ]  O código foi formatado e passou pelas verificações do linter.
- [ ]  Todos os testes (unitários e de integração) estão passando no pipeline de CI, com a cobertura de código mantida ou aumentada.
- [ ]  O Pull Request (PR) foi criado, descrevendo a nova página de configurações e como ela interage com a API.
- [ ]  O código foi revisado e aprovado por pelo menos um outro desenvolvedor da equipe.
- [ ]  A funcionalidade foi mesclada na branch principal de desenvolvimento.
- [ ]  A funcionalidade foi verificada manualmente em um ambiente de Staging/QA:
    - [ ]  A página carrega e exibe os prompts e template atuais do backend.
    - [ ]  A edição dos campos de texto funciona.
    - [ ]  Clicar em "Salvar" persiste as alterações (verificável recarregando a página ou inspecionando os arquivos no servidor).
    - [ ]  O feedback visual para o usuário (carregando, salvo, erro) funciona como esperado.

# Épico [4]

## US [401]

### **Plano de Implementação da História: US-401: Implementar Autenticação e Persistência de Usuário (Backend)**

**Épico:** Persistência e Colaboração (Roadmap Futuro)
**História de Usuário:**

- **Como um** Desenvolvedor Backend, **quero** integrar um banco de dados (ex: PostgreSQL), adicionar tabelas de `User` e `Proposal` e criar endpoints de registro/login, **para que** os usuários possam ter contas persistentes.
- **Critérios de Aceite:**
    1. O banco de dados está configurado e acessível via ORM (ex: Prisma).
    2. Endpoints `POST /api/auth/register` e `POST /api/auth/login` são criados.
    3. Um token JWT é retornado no login para autenticar requisições subsequentes.

---

### **1. Tarefas Técnicas (Technical Tasks)**

| Camada/Área | Tarefa Específica (Sub-task) | Detalhes Técnicos (Conforme Arquitetura) |
| --- | --- | --- |
| **Infraestrutura** | **BE-1:** Configurar o ambiente do banco de dados e ORM. | 1. Instalar o PostgreSQL (localmente/Docker). 2. Adicionar o Prisma como dependência (`npm install prisma --save-dev`). 3. Iniciar o Prisma (`npx prisma init`) e configurar a string de conexão no `.env`. |
|  | **BE-2:** Definir o schema do banco de dados. | No arquivo `prisma/schema.prisma`, definir os modelos `User` (com `id`, `email`, `password`) e `Proposal` (com `id`, `content`, `userId`, etc.), estabelecendo a relação entre eles. |
|  | **BE-3:** Executar a migração do banco de dados. | Rodar o comando `npx prisma migrate dev --name init` para criar as tabelas no banco de dados com base no schema. Gerar o cliente Prisma com `npx prisma generate`. |
| **Backend (Core/Infra)** | **BE-4:** Implementar o `PostgresUserRepository`. | Em `/src/infra/repositories/`, criar `PostgresUserRepository.js` que implementa a interface `IUserRepository` (que precisará ser criada). Os métodos (`findByEmail`, `save`) usarão o cliente Prisma (`prisma.user.findUnique`, `prisma.user.create`) para interagir com o DB. |
| **Backend (Core)** | **BE-5:** Implementar o `AuthService`. | Criar o `/src/core/services/AuthService.js`. Deve ter dois métodos: 1. `register`: recebe dados do usuário, usa `bcrypt` para gerar hash da senha, chama `userRepository.save`. 2. `login`: recebe credenciais, busca o usuário por email, usa `bcrypt.compare` para verificar a senha. Se for válida, gera um token JWT usando a biblioteca `jsonwebtoken`. |
| **Backend (API)** | **BE-6:** Criar o `AuthController`. | Criar o `/src/api/controllers/AuthController.js` com métodos para `register` e `login`, que validam a entrada e chamam os métodos correspondentes no `AuthService`. |
|  | **BE-7:** Criar os endpoints de autenticação. | Criar o arquivo de rotas `/src/api/routes/auth.routes.js`. Definir as rotas `POST /register` e `POST /login`, conectando-as aos métodos do `AuthController`. |
| **Testes** | **TEST-1:** Escrever testes unitários para o `AuthService`. | Usando Jest, mockar o `UserRepository` e as bibliotecas `bcrypt`/`jsonwebtoken`. Testar a lógica de registro (hashing é chamado) e login (comparação é chamada, token é gerado no sucesso, erro em senha inválida). |
|  | **TEST-2:** Configurar um banco de dados de teste. | Configurar o Prisma para usar um banco de dados separado para os testes de integração, garantindo o isolamento. |
|  | **TEST-3:** Escrever testes de integração para os endpoints. | Usando `supertest`, criar testes que fazem chamadas HTTP reais para `/register` e `/login`. Os testes devem interagir com o banco de dados de teste para: 1) Registrar um novo usuário. 2) Tentar registrar o mesmo usuário novamente (esperando erro). 3) Fazer login com credenciais corretas (esperando token). 4) Fazer login com senha errada (esperando erro 401). |

---

### **2. Checklist de Definition of Done (DoD)**

- [ ]  Todas as tarefas técnicas (BE, TEST, Infra) listadas acima foram concluídas.
- [ ]  O código foi formatado e passou pelas verificações do linter.
- [ ]  Todos os testes unitários e de integração estão passando no pipeline de CI, que agora inclui a inicialização do serviço de banco de dados de teste.
- [ ]  O Pull Request (PR) foi criado, com uma descrição detalhada da nova configuração do banco de dados, o schema e as novas dependências.
- [ ]  O código foi revisado e aprovado por pelo menos um outro desenvolvedor, com foco especial em segurança (hashing de senha, uso de JWT).
- [ ]  As migrações do Prisma foram revisadas e aprovadas.
- [ ]  A funcionalidade foi mesclada na branch principal de desenvolvimento.
- [ ]  A documentação da API (Postman/Swagger) foi atualizada para incluir os novos endpoints de autenticação.
- [ ]  A funcionalidade foi verificada manualmente em um ambiente de Staging/QA:
    - [ ]  O registro de um novo usuário funciona.
    - [ ]  O login com credenciais corretas retorna um token JWT válido.
    - [ ]  O login com credenciais incorretas retorna um erro apropriado.

## US [402]

### **Plano de Implementação da História: US-402: Refatorar a Persistência de Propostas (Backend)**

**Épico:** Persistência e Colaboração (Roadmap Futuro)
**História de Usuário:**

- **Como um** Desenvolvedor Backend, **quero** substituir o repositório em memória/arquivo por um `PostgresProposalRepository`, **para que** as propostas sejam salvas permanentemente e associadas a um usuário.
- **Critérios de Aceite:**
    1. A nova classe de repositório implementa a mesma interface `IProposalRepository`.
    2. O endpoint `POST /api/proposals` agora exige autenticação e salva a proposta no banco de dados com o `userId`.
    3. O endpoint de histórico é atualizado para retornar todas as propostas do usuário autenticado.

---

### **1. Tarefas Técnicas (Technical Tasks)**

| Camada/Área | Tarefa Específica (Sub-task) | Detalhes Técnicos (Conforme Arquitetura) |
| --- | --- | --- |
| **Backend (Core/Infra)** | **BE-1:** Adaptar a Interface `IProposalRepository`. | Modificar a interface em `/src/core/repositories/IProposalRepository.js`. O método `save` agora deve aceitar um `userId`, e o `findBySessionId` será substituído por `findByUserId(userId)`. |
|  | **BE-2:** Implementar o `PostgresProposalRepository`. | Em `/src/infra/repositories/`, criar `PostgresProposalRepository.js` que implementa a `IProposalRepository` atualizada. Usar o cliente Prisma: `prisma.proposal.create` para o `save` e `prisma.proposal.findMany` com uma cláusula `where` para o `findByUserId`. |
| **Backend (Core)** | **BE-3:** Refatorar o `ProposalGenerationService`. | Atualizar a injeção de dependência para usar o `PostgresProposalRepository` em vez do `InMemory` ou `File` repository. Ajustar as chamadas aos métodos do repositório para passar o `userId`. |
| **Backend (API)** | **BE-4:** Criar um middleware de autenticação (`ensureAuthenticated`). | Criar um middleware que verifica a presença e a validade do token JWT no cabeçalho `Authorization`. Se válido, ele decodifica o token para extrair o `userId` e o anexa ao objeto `request` (ex: `req.user = { id: userId }`) antes de chamar o próximo handler. |
|  | **BE-5:** Proteger o endpoint `POST /api/proposals`. | No arquivo `/src/api/routes/proposal.routes.js`, adicionar o middleware `ensureAuthenticated` à rota `POST /proposals`. |
|  | **BE-6:** Atualizar o `ProposalController` para usar o `userId`. | No método que lida com a criação de propostas, extrair o `userId` do objeto `req.user` (adicionado pelo middleware) e passá-lo para o `ProposalGenerationService`. |
|  | **BE-7:** Atualizar o endpoint de histórico. | Modificar a rota `GET /api/proposals/session/:sessionId` para `GET /api/proposals/history`. Protegê-la com o middleware `ensureAuthenticated`. Atualizar o método do controller para chamar o serviço que busca o histórico por `userId` (do `req.user`). |
| **Testes** | **TEST-1:** Escrever testes unitários para o `PostgresProposalRepository`. | Usando Jest, **mockar o cliente Prisma** (`PrismaClient`). Testar os métodos do repositório para garantir que eles chamam as funções corretas do Prisma com os argumentos apropriados (ex: `where: { userId }`). |
|  | **TEST-2:** Escrever testes de integração para os endpoints protegidos. | Usando `supertest` e o banco de dados de teste: 1) Tentar acessar `POST /api/proposals` sem um token JWT (esperar erro 401). 2) Obter um token válido (do endpoint de login), fazer a chamada com o token e verificar se a proposta é criada no banco de dados associada ao usuário correto. 3) Repetir o processo para o endpoint de histórico. |
|  | **BE-8:** Remover código legado. | Após a implementação e testes, remover o antigo `InMemoryProposalRepository` e as rotas de sessão para manter a base de código limpa. |

---

### **2. Checklist de Definition of Done (DoD)**

- [ ]  Todas as tarefas técnicas (BE, TEST) listadas acima foram concluídas.
- [ ]  O código foi formatado e passou pelas verificações do linter.
- [ ]  Todos os testes unitários e de integração (incluindo casos de falha de autenticação) estão passando no pipeline de CI.
- [ ]  O Pull Request (PR) foi criado, detalhando a significativa refatoração da camada de persistência e a introdução da autenticação nos endpoints.
- [ ]  O código foi revisado e aprovado por pelo menos um outro membro da equipe, com foco na segurança e na correta implementação do padrão de repositório.
- [ ]  A funcionalidade foi mesclada na branch principal de desenvolvimento.
- [ ]  A documentação da API foi atualizada para refletir as mudanças: os endpoints agora exigem um cabeçalho `Authorization: Bearer <token>`.
- [ ]  A funcionalidade foi verificada manualmente via Postman/Insomnia:
    - [ ]  Chamadas sem token para os endpoints de propostas falham com 401.
    - [ ]  A criação de uma proposta com um token válido a salva no banco de dados com o `userId` correto.
    - [ ]  A busca de histórico com um token válido retorna apenas as propostas daquele usuário.

## US [403]

### **Plano de Implementação da História: US-403: Construir Fluxos de Autenticação e Histórico Persistente (Frontend)**

**Épico:** Persistência e Colaboração (Roadmap Futuro)
**História de Usuário:**

- **Como um** usuário, **quero** me registrar, fazer login/logout e ver todo o meu histórico de propostas, **para que** eu possa usar a plataforma de forma segura e contínua.
- **Critérios de Aceite:**
    1. Páginas de Login e Registro são criadas.
    2. O cliente salva o token JWT e o envia nos cabeçalhos das requisições autenticadas.
    3. A página de histórico é refatorada para exibir todos os registros do usuário logado.

---

### **1. Tarefas Técnicas (Technical Tasks)**

| Camada/Área | Tarefa Específica (Sub-task) | Detalhes Técnicos (Conforme Arquitetura) |
| --- | --- | --- |
| **Frontend (Core)** | **FE-1:** Criar um `AuthContext` e Provider. | Usar a Context API do React para criar um `AuthContext` que irá gerenciar o estado de autenticação (token, dados do usuário) e expor funções como `login`, `logout` em toda a aplicação. |
|  | **FE-2:** Implementar a lógica de gerenciamento de token. | No `AuthProvider`, implementar a lógica para: 1) Salvar o token JWT no `localStorage` após o login/registro. 2) Ler o token do `localStorage` ao carregar a aplicação. 3) Remover o token no logout. |
|  | **FE-3:** Configurar o interceptador de API. | Configurar um interceptador do `axios` (ou wrapper de `fetch`) que automaticamente anexa o token JWT do `AuthContext`/`localStorage` ao cabeçalho `Authorization` de todas as requisições para a API. |
| **Frontend (UI)** | **FE-4:** Criar as páginas de Registro e Login. | Criar os componentes `/src/pages/RegisterPage.jsx` e `/src/pages/LoginPage.jsx`. Cada um conterá um formulário simples (email/senha) e a lógica para chamar os respectivos serviços da API. |
|  | **FE-5:** Implementar o fluxo de redirecionamento. | Usar uma biblioteca de roteamento (ex: `react-router-dom`) para: 1) Proteger rotas (como a página principal), redirecionando para `/login` se não houver autenticação. 2) Redirecionar para a página principal após um login/registro bem-sucedido. |
|  | **FE-6:** Adicionar o botão e a função de Logout. | Adicionar um botão de "Logout" em um local apropriado (ex: header). O `onClick` deve chamar a função `logout` do `AuthContext`, que limpará o token e redirecionará para a página de login. |
| **Frontend (Refactor)** | **FE-7:** Refatorar o serviço de API de propostas. | Modificar o `/src/services/proposalApiService.js` para usar o novo endpoint de histórico. Substituir a função `getSessionHistory(sessionId)` por `getProposalHistory()`, que chamará `GET /api/proposals/history` (sem precisar de sessionId, pois o backend usará o token). |
|  | **FE-8:** Refatorar a exibição do histórico. | Modificar a `HomePage` ou onde o histórico é exibido. A chamada para buscar o histórico agora deve ser feita usando a nova função `getProposalHistory()` e só deve ser acionada quando o usuário estiver autenticado. |
| **Testes** | **TEST-1:** Escrever testes de integração para as páginas de Login/Registro. | Usando `React Testing Library`, testar os fluxos: 1) Mockar os serviços da API. 2) Simular o preenchimento dos formulários e o clique no botão. 3) Verificar se o serviço de API correto é chamado. 4) Verificar se o `AuthContext` (mockado) tem sua função de login chamada e se ocorre o redirecionamento. |
|  | **TEST-2:** Atualizar testes de integração da página principal/histórico. | Modificar os testes existentes para rodar dentro de um `AuthProvider` mockado. Verificar se, em um estado autenticado, a função `getProposalHistory` é chamada para carregar os dados. |

---

### **2. Checklist de Definition of Done (DoD)**

- [ ]  Todas as tarefas técnicas (FE, TEST) listadas acima foram concluídas.
- [ ]  O código foi formatado e passou pelas verificações do linter.
- [ ]  Todos os testes de integração para os novos fluxos de autenticação e para as páginas refatoradas estão passando no pipeline de CI.
- [ ]  O Pull Request (PR) foi criado, descrevendo a implementação completa do fluxo de autenticação no frontend.
- [ ]  O código foi revisado e aprovado por pelo menos um outro membro da equipe, com atenção especial ao gerenciamento de estado global e segurança do token.
- [ ]  A funcionalidade foi mesclada na branch principal de desenvolvimento.
- [ ]  A funcionalidade foi verificada manualmente em um ambiente de Staging/QA, cobrindo todo o ciclo de vida do usuário:
    - [ ]  Registro de uma nova conta funciona.
    - [ ]  Redirecionamento para a página principal após registro.
    - [ ]  Logout funciona e redireciona para o login.
    - [ ]  Login com a conta criada funciona.
    - [ ]  A criação de propostas funciona (enviando o token automaticamente).
    - [ ]  O histórico exibido pertence *apenas* ao usuário logado.
    - [ ]  O acesso direto a rotas protegidas sem login redireciona para a página de login.

# Épico [5]

## US [501]

### **Plano de Implementação da História: US-501: Criar Endpoints de Métricas de Uso (Backend)**

**Épico:** Analytics e Insights (Roadmap Futuro)
**História de Usuário:**

- **Como um** Desenvolvedor Backend, **quero** criar endpoints de analytics (ex: `GET /api/analytics/usage`) que agreguem métricas de uso, **para que** o frontend possa exibi-las.
- **Critérios de Aceite:**
    1. O endpoint retorna estatísticas como: número total de propostas geradas, propostas por usuário, média de gerações por dia.
    2. Os cálculos são eficientes e não sobrecarregam o banco de dados.

---

### **1. Tarefas Técnicas (Technical Tasks)**

| Camada/Área | Tarefa Específica (Sub-task) | Detalhes Técnicos (Conforme Arquitetura) |
| --- | --- | --- |
| **Backend (Core/Infra)** | **BE-1:** Implementar métodos de agregação no `PostgresProposalRepository`. | Adicionar novos métodos ao `IProposalRepository` e à sua implementação. Estes métodos usarão as funcionalidades de agregação do Prisma (ex: `_count`, `groupBy`) para calcular as métricas diretamente no banco de dados. Ex: `getTotalCount()`, `getCountByUser()`. |
| **Backend (Core)** | **BE-2:** Criar o `AnalyticsService`. | Criar um novo `/src/core/services/AnalyticsService.js`. Este serviço irá orquestrar as chamadas aos novos métodos do `PostgresProposalRepository` e combinar os resultados em um único objeto de resposta para o controller. |
| **Backend (API)** | **BE-3:** Criar o `AnalyticsController`. | Criar um novo `/src/api/controllers/AnalyticsController.js` com um método (ex: `getUsageMetrics`) que chama o `AnalyticsService` e formata a resposta HTTP. |
|  | **BE-4:** Criar o endpoint de analytics e protegê-lo. | Criar um novo arquivo de rotas `/src/api/routes/analytics.routes.js`. Definir a rota `GET /usage` e conectá-la ao `AnalyticsController`. **Proteger esta rota** com um middleware que verifique se o usuário tem um papel de "administrador" (assumindo que esta funcionalidade será adicionada ou que pode ser simulada por enquanto). |
| **Testes** | **TEST-1:** Escrever testes unitários para o `AnalyticsService`. | Usando Jest, mockar o `PostgresProposalRepository`. Chamar o método do serviço e verificar se ele chama os métodos corretos do repositório e formata os dados de retorno como esperado. |
|  | **TEST-2:** Escrever testes de integração para o endpoint. | Usando `supertest` e um banco de dados de teste: 1) Popular o banco de dados com vários usuários e propostas. 2) Fazer uma chamada `GET` para `/api/analytics/usage` (com um token de admin). 3) Verificar se as métricas retornadas (contagens, agrupamentos) correspondem exatamente aos dados inseridos no banco. 4) Testar o acesso sem um token de admin (esperar erro 403 Forbidden). |
| **Documentação** | **DOC-1:** Otimização e Indexação do Banco de Dados. | Documentar a necessidade de adicionar índices nas colunas `userId` e `createdAt` da tabela `Proposal` para garantir que as consultas de agregação permaneçam eficientes à medida que os dados crescem. Adicionar os índices no `schema.prisma`. |

---

### **2. Checklist de Definition of Done (DoD)**

- [ ]  Todas as tarefas técnicas (BE, TEST, DOC) listadas acima foram concluídas.
- [ ]  O código foi formatado e passou pelas verificações do linter.
- [ ]  Todos os testes unitários e de integração (incluindo casos de autorização) estão passando no pipeline de CI.
- [ ]  O schema do Prisma foi atualizado com os índices necessários e uma nova migração foi gerada.
- [ ]  O Pull Request (PR) foi criado, descrevendo o novo endpoint de analytics e a estratégia para garantir a performance das consultas.
- [ ]  O código foi revisado e aprovado por pelo menos um outro membro da equipe, com foco na eficiência das consultas ao banco de dados.
- [ ]  A funcionalidade foi mesclada na branch principal de desenvolvimento.
- [ ]  A documentação da API (Postman/Swagger) foi atualizada para incluir o novo endpoint `GET /api/analytics/usage` e os requisitos de autorização.
- [ ]  O endpoint foi verificado manualmente em um ambiente de Staging/QA com dados de teste para garantir a precisão das métricas retornadas.

## US [502]

### **Plano de Implementação da História: US-502: Construir o Painel de Métricas de Uso (Frontend)**

**Épico:** Analytics e Insights (Roadmap Futuro)
**História de Usuário:**

- **Como um** usuário administrador, **quero** uma página de "Analytics" com gráficos sobre o uso, **para que** eu possa entender como a plataforma está sendo adotada.
- **Critérios de Aceite:**
    1. Uma nova página de "Analytics" é adicionada à aplicação.
    2. A página consome os dados do endpoint de analytics e exibe as métricas de uso de forma clara.

---

### **1. Tarefas Técnicas (Technical Tasks)**

| Camada/Área | Tarefa Específica (Sub-task) | Detalhes Técnicos (Conforme Arquitetura) |
| --- | --- | --- |
| **Frontend (React)** | **FE-1:** Instalar uma biblioteca de gráficos. | Pesquisar e instalar uma biblioteca leve para visualização de dados (ex: `recharts`, `chart.js` com wrapper para React). Adicionar a dependência ao `package.json`. |
|  | **FE-2:** Criar o serviço de API para Analytics. | No `/src/services/` (em `analyticsApiService.js`), adicionar a função `getUsageMetrics()` que faz uma requisição `GET` autenticada para o endpoint `/api/analytics/usage`. |
|  | **FE-3:** Criar a página `AnalyticsPage`. | Criar o arquivo `/src/pages/AnalyticsPage.jsx` e adicionar a rota correspondente. Esta página deve ser protegida para ser acessível apenas por usuários administradores. |
|  | **FE-4:** Implementar o carregamento de dados e estados. | No `AnalyticsPage.jsx`, usar `useEffect` para chamar `getUsageMetrics()` na montagem. Gerenciar os estados de `isLoading`, `error` e os dados das métricas com `useState`. |
|  | **FE-5:** Criar componentes de visualização de métricas. | Criar componentes menores em `/src/features/analytics/` para exibir as métricas. Ex: 1) `MetricCard.jsx` para exibir números únicos (ex: "Total de Propostas"). 2) `ProposalsByUserChart.jsx` para renderizar um gráfico de barras com os dados de propostas por usuário. |
|  | **FE-6:** Integrar os componentes de visualização na página. | No `AnalyticsPage.jsx`, após o carregamento dos dados, passar os dados apropriados como props para os componentes `MetricCard` e `ProposalsByUserChart` e renderizá-los. |
| **Backend (Node.js)** | **N/A** | Nenhuma tarefa de backend é necessária, pois assume-se que a US-501 (criação dos endpoints) já foi concluída. |
| **Testes** | **TEST-1:** Escrever testes de componente para os componentes de métricas. | Para `MetricCard` e `ProposalsByUserChart`, criar testes que recebem dados mockados via `props` e verificam se eles são renderizados corretamente. Para o gráfico, pode-se verificar a presença de eixos ou barras, dependendo da biblioteca. |
|  | **TEST-2:** Escrever testes de integração para `AnalyticsPage`. | Usando `React Testing Library`: 1) **Mockar o serviço `analyticsApiService`**. 2) Renderizar a página e verificar se a função `getUsageMetrics` é chamada. 3) Simular uma resposta de sucesso e verificar se os componentes de métricas são renderizados com os dados corretos. 4) Simular uma resposta de erro e verificar se uma mensagem de erro é exibida. |

---

### **2. Checklist de Definition of Done (DoD)**

- [ ]  Todas as tarefas técnicas (FE, TEST) listadas acima foram concluídas.
- [ ]  O código foi formatado e passou pelas verificações do linter.
- [ ]  Todos os testes de componente e integração estão passando no pipeline de CI.
- [ ]  O Pull Request (PR) foi criado, descrevendo a nova página de analytics, a biblioteca de gráficos escolhida e como testar as visualizações.
- [- O código foi revisado e aprovado por pelo menos um outro membro da equipe.
- [ ]  A funcionalidade foi mesclada na branch principal de desenvolvimento.
- [ ]  A funcionalidade foi verificada manualmente em um ambiente de Staging/QA por um usuário com perfil de administrador:
    - [ ]  A página de Analytics carrega sem erros.
    - [ ]  Os números e gráficos exibidos correspondem aos dados do banco de dados de teste.
    - [ ]  Um estado de carregamento é exibido enquanto os dados estão sendo buscados.
    - [ ]  A página é visualmente clara e os dados são fáceis de interpretar. página é visualmente clara e os dados são fáceis de interpretar.

## US [503]

### **Plano de Implementação da História: US-503: Implementar um Mecanismo de Feedback de Qualidade (Frontend/Backend)**

**Épico:** Analytics e Insights (Roadmap Futuro)
**História de Usuário:**

- **Como um** Engenheiro de Vendas, **quero** ter botões simples (ex: "👍 Útil" / "👎 Não útil") após cada geração, **para que** eu possa dar um feedback rápido sobre a qualidade do resultado.
- **Critérios de Aceite:**
    1. (Frontend) Os botões de feedback são exibidos na UI após a geração de uma proposta.
    2. (Backend) Um novo endpoint (`POST /api/proposals/:proposalId/feedback`) é criado para registrar esse feedback no banco de dados, associado à proposta específica.

---

### **1. Tarefas Técnicas (Technical Tasks)**

| Camada/Área | Tarefa Específica (Sub-task) | Detalhes Técnicos (Conforme Arquitetura) |
| --- | --- | --- |
| **Backend (DB/Infra)** | **BE-1:** Atualizar o schema do banco de dados. | No `prisma/schema.prisma`, adicionar um novo campo na tabela `Proposal`, como `qualityFeedback` (pode ser um `String` ou `Enum` com valores 'GOOD', 'BAD', 'NONE'). Executar a migração (`npx prisma migrate dev`). |
|  | **BE-2:** Implementar o método de repositório para salvar o feedback. | No `IProposalRepository` e sua implementação `PostgresProposalRepository`, adicionar um novo método `saveFeedback(proposalId: string, feedback: string)`. Este método usará `prisma.proposal.update` para definir o valor do novo campo. |
| **Backend (Core/API)** | **BE-3:** Criar o serviço e controller para o feedback. | Criar um novo `FeedbackService` que valida o input (garante que o feedback é 'GOOD' ou 'BAD') e chama o método do repositório. Criar um `FeedbackController` para orquestrar a requisição. |
|  | **BE-4:** Criar o endpoint de feedback. | No arquivo `/src/api/routes/proposal.routes.js`, adicionar a nova rota `POST /:proposalId/feedback`. Protegê-la com o middleware de autenticação para garantir que apenas o dono da proposta possa dar feedback (uma verificação de propriedade deve ser feita no serviço). |
| **Frontend (React)** | **FE-5:** Criar o componente de UI `FeedbackButtons`. | Em `/src/features/proposal-generator/`, criar um componente que exibe os botões "👍" e "👎". Ele deve receber o `proposalId` como prop e uma callback para quando o feedback for enviado. Adicionar um estado para desabilitar os botões após o clique. |
|  | **FE-6:** Adicionar a função de serviço da API de feedback. | No `/src/services/proposalApiService.js`, adicionar a função `submitFeedback(proposalId, feedback)` que faz uma requisição `POST` para o novo endpoint. |
|  | **FE-7:** Integrar os botões de feedback na UI. | No `ProposalGenerator.jsx`, após uma geração de proposta bem-sucedida (quando se recebe o `id` da proposta na resposta), renderizar o componente `FeedbackButtons`, passando o `proposalId` recebido. |
| **Testes** | **TEST-1:** Escrever testes unitários para o `FeedbackService`. | Mockar o repositório. Testar a lógica de validação (rejeitar feedback inválido) e verificar se o método do repositório é chamado corretamente. |
|  | **TEST-2:** Escrever teste de integração para o endpoint de feedback. | Usando `supertest` e um banco de dados de teste: 1) Criar um usuário e uma proposta. 2) Chamar o endpoint de feedback com o token do usuário e verificar se o campo no banco de dados é atualizado. 3) Tentar enviar feedback com um token de outro usuário (esperar erro 403 Forbidden). |
|  | **TEST-3:** Escrever teste de integração para o componente `FeedbackButtons`. | Usando `React Testing Library`, renderizar o componente. Simular o clique em um botão, mockar a chamada da API e verificar se o serviço `submitFeedback` é chamado com os argumentos corretos. Verificar se os botões são desabilitados após o clique. |

---

### **2. Checklist de Definition of Done (DoD)**

- [ ]  Todas as tarefas técnicas (BE, FE, TEST) listadas acima foram concluídas.
- [ ]  O código foi formatado e passou pelas verificações do linter.
- [ ]  Todos os testes unitários e de integração (full-stack) estão passando no pipeline de CI.
- [ ]  Uma nova migração de banco de dados foi criada e revisada.
- [ ]  O Pull Request (PR) foi criado, descrevendo a nova funcionalidade de feedback e as mudanças no schema do DB.
- [ ]  O código foi revisado e aprovado por pelo menos um outro membro da equipe.
- [ ]  A funcionalidade foi mesclada na branch principal de desenvolvimento.
- [ ]  A documentação da API foi atualizada para incluir o novo endpoint de feedback.
- [ ]  A funcionalidade foi verificada manualmente em um ambiente de Staging/QA:
    - [ ]  Após gerar uma proposta, os botões de feedback aparecem.
    - [ ]  Clicar em um botão envia o feedback para o backend (verificável no DB).
    - [ ]  Após o clique, os botões mudam de estado (ex: ficam desabilitados ou mostram uma mensagem de "Obrigado").
    - [ ]  A ação é registrada corretamente na tabela `Proposal` do banco de dados.

## US [504]

### **Plano de Implementação da História: US-504: Exibir Métricas de Qualidade e Performance de Prompts (Frontend/Backend)**

**Épico:** Analytics e Insights (Roadmap Futuro)
**História de Usuário:**

- **Como um** usuário administrador, **quero** ver no painel de "Analytics" a pontuação de qualidade média das propostas e quais prompts estão performando melhor, **para que** eu possa tomar decisões baseadas em dados para refinar a IA.
- **Critérios de Aceite:**
    1. (Backend) O endpoint de analytics é expandido para calcular e retornar a taxa de feedback positivo/negativo.
    2. (Se aplicável após o Épico 3) O endpoint correlaciona o feedback com a versão do prompt usada na geração.
    3. (Frontend) O painel de Analytics é atualizado para exibir essas novas métricas de qualidade.

---

### **1. Tarefas Técnicas (Technical Tasks)**

| Camada/Área | Tarefa Específica (Sub-task) | Detalhes Técnicos (Conforme Arquitetura) |
| --- | --- | --- |
| **Backend (DB/Infra)** | **BE-1:** Adicionar rastreamento de versão de config à proposta. | No `schema.prisma`, adicionar um campo na tabela `Proposal`, como `configVersionId` (String, opcional). Este campo será usado para armazenar um identificador da versão do `prompts.json`/`template.md` usada na geração. Executar a migração. |
| **Backend (Core)** | **BE-2:** Atualizar o `ProposalGenerationService` para salvar a versão. | Modificar o serviço para, ao gerar uma proposta, salvar também a `configVersionId` (pode ser um hash do conteúdo dos arquivos de config ou um timestamp da última modificação). |
|  | **BE-3:** Expandir o `AnalyticsService` com cálculos de qualidade. | No `AnalyticsService`, adicionar lógica para: 1) Chamar um novo método do repositório que calcula a contagem de feedback 'GOOD' vs 'BAD'. 2) Calcular a taxa percentual de feedback positivo. 3) Retornar essa taxa na sua resposta. |
| **Backend (API)** | **BE-4:** Expandir a resposta do endpoint de analytics. | Modificar o `AnalyticsController` para incluir os novos dados de qualidade (ex: `qualityMetrics: { positiveFeedbackRate: 0.85 }`) no objeto JSON de resposta do endpoint `GET /api/analytics/usage`. |
| **Frontend (React)** | **FE-5:** Criar o componente de UI `QualityMetrics`. | Em `/src/features/analytics/`, criar um novo componente `QualityMetrics.jsx`. Ele deve ser capaz de receber a taxa de feedback e exibi-la de forma clara (ex: com um anel de progresso ou um cartão "Nota de Qualidade: 85%"). |
|  | **FE-6:** Atualizar a `AnalyticsPage` para exibir as novas métricas. | No `/src/pages/AnalyticsPage.jsx`, modificar a lógica para extrair os `qualityMetrics` da resposta da API e passá-los como props para o novo componente `<QualityMetrics />`. |
| **Testes** | **TEST-1:** Atualizar os testes do `ProposalGenerationService`. | Modificar os testes para garantir que o serviço agora salva a `configVersionId` corretamente ao criar uma proposta. |
|  | **TEST-2:** Atualizar os testes de integração do endpoint de analytics. | Modificar a configuração do teste para incluir propostas com feedback. Chamar o endpoint `GET /api/analytics/usage` e verificar se o campo `qualityMetrics` com a taxa correta está presente na resposta. |
|  | **TEST-3:** Escrever testes de componente para `QualityMetrics`. | Usando `React Testing Library`, passar diferentes taxas (ex: 0.85, 0.5) como props e verificar se o componente renderiza a porcentagem correta ("85%", "50%"). |
|  | **TEST-4:** Atualizar os testes de integração da `AnalyticsPage`. | Modificar o mock da API para incluir os `qualityMetrics`. Verificar se, após o carregamento, o componente `QualityMetrics` é renderizado na página. |

---

### **2. Checklist de Definition of Done (DoD)**

- [ ]  Todas as tarefas técnicas (BE, FE, TEST) listadas acima foram concluídas.
- [ ]  O código foi formatado e passou pelas verificações do linter.
- [ ]  Todos os testes unitários e de integração foram atualizados e estão passando no pipeline de CI.
- [ ]  A migração do banco de dados (se aplicável) foi gerada e revisada.
- [ ]  O Pull Request (PR) foi criado, descrevendo como os dados de qualidade são calculados e exibidos.
- [ ]  O código foi revisado e aprovado por pelo menos um outro membro da equipe.
- [ ]  A funcionalidade foi mesclada na branch principal de desenvolvimento.
- [ ]  A documentação da API foi atualizada para refletir a adição dos `qualityMetrics` na resposta do endpoint de analytics.
- [ ]  A funcionalidade foi verificada manualmente em um ambiente de Staging/QA:
    - [ ]  O painel de Analytics agora exibe a seção de "Métricas de Qualidade".
    - [ ]  A taxa de feedback positivo exibida corresponde aos dados de feedback registrados no banco de dados.
    - [ ]  A página continua funcionando corretamente mesmo se não houver propostas com feedback (ex: exibindo "N/A" ou 0%).