# Changelog - GPT-Md v5.2
 
 ## 🎯 Resumo das Implementações (27/01/2026)
 
 ### ✅ Funcionalidades Implementadas
 
 #### 1. Setup do Frontend Web (Vite + React + Tailwind)
 - Inicialização do ambiente frontend em `/frontend`
 - Configuração do Vite com suporte a React e Tailwind CSS
 - Estrutura base de componentes e layout para interface moderna
 
 #### 2. Refatoração Backend (Arquitetura de Pacotes)
 - Organização do código `src/` em pacotes semânticos:
   - `src/config/`: Gerenciamento de tokens e variáveis de ambiente
   - `src/database/`: Camada de acesso a dados (JSON e SQLite)
   - `src/routers/`: Definição de rotas para a API FastAPI
 - Correção de imports relativos e resolução de dependências circulares
 
 #### 3. Integração API-Core
 - Preparação do `main.py` para atuar como servidor de API além de CLI
 - Mockup de endpoints iniciais para integração com o frontend
 
 ### 📊 Commits Relevantes
 ```
 c81a080 - refactor: reorganize database and config into packages and fix import issues
 7a29e88 - feat(web): frontend setup (vite+react+tailwind) and base layout
 ```
 
 ---
 
 # Changelog - GPT-Md v5.1

## 🎯 Resumo das Implementações (26/01/2026)

### ✅ Funcionalidades Implementadas

#### 1. Controle de Modos de Saída (`--output-mode`)
- **`unified`** (padrão): Gera apenas a proposta completa
- **`full`**: Gera 3 versões (Unificada, Técnica e Comercial)
- **`splited`**: Gera apenas Técnica e Comercial separadas

#### 2. Proposta de NOC/OPEX Separada (`--separate-opex`)
- Gera arquivo standalone `PROPOSTA_NOC_SUSTENTACAO_*.md`
- Focado exclusivamente em serviços recorrentes
- Permite aprovação independente do CAPEX

#### 3. Correção de Identidade (Provider vs Cliente)
**Problema:** IA confundia EGE (provedor) com o cliente nos textos gerados.

**Soluções Implementadas:**
- **Hardfix no Prompt** (`src/ai_agent.py`): Instruções explícitas sobre quem é provedor e cliente
- **Correção Forçada** (`src/main.py` linha 245-255): Após ingestão, força `company_name = "EGE Soluções Industriais"`
- **Mapeamento de Contexto** (`src/engines/library_assembler.py` linhas 109, 127): `client_company` sempre aponta para `intent.client_name`
- **Sanitização de Conteúdo** (`src/main.py` função `sanitize_content`): Remove referências erradas antes de salvar

#### 4. Sistema de QA Automático
**Função:** `run_quality_check()` em `src/main.py`

**Verificações:**
- ✅ Integridade das seções da proposta
- ✅ Nome do cliente correto
- ✅ Nome do provedor (EGE) presente
- ✅ Ausência de auto-referências (EGE -> EGE)
- ✅ Tabelas de preços presentes

**Saída:** Relatório no terminal ao final da execução

#### 5. Atualização do README.md
- Documentação da estrutura de venv externo
- Comandos corretos com caminho completo do interpretador
- Exemplos práticos de uso
- Documentação dos novos parâmetros

### 🐛 Correções de Bugs

#### Bug #1: Tabelas MAT/MOD/DIV/SET não geradas
**Causa:** Código de salvamento estava com indentação incorreta (dentro da função `sanitize_content` após o `return`)
**Correção:** Movido para o lugar correto dentro do `main()` após geração das propostas
**Commit:** `034d305` - "fix: correctly place table saving code inside main()"

#### Bug #2: Títulos inconsistentes nos arquivos
**Causa:** Variável `proposal_title` não era atualizada para cada tipo de saída
**Status:** Resolvido com o mapeamento correto de contexto

### 📁 Arquivos de Saída Gerados

**Sempre:**
- `debug_intent.json` - Intent extraído pela IA
- `PROPOSTA_*.md` - Propostas conforme modo escolhido
- `MAT_*.md/csv` - Tabela de Materiais
- `MOD_*.md/csv` - Tabela de Mão de Obra
- `SET_*.md/csv` - Serviços Externos
- `DIV_*.md/csv` - Despesas de Viagem
- `TOPICS_*.md` - Índice de Tópicos
- `LOGISTICS_AUDIT.md` - Auditoria de logística
- `API_USAGE_STATS.md` - Estatísticas de uso da API

**Com `--debug`:**
- `raw_ai_interpretation.txt` - Resposta bruta da IA (interpretação)
- `raw_ai_proposal.txt` - Resposta bruta da IA (redação técnica)

### 🔧 Arquivos Modificados

1. **src/main.py**
   - Adicionado hardfix de identidade
   - Implementado `sanitize_content()`
   - Implementado `run_quality_check()`
   - Corrigida indentação do código de salvamento de tabelas
   - Adicionados parâmetros `--output-mode` e `--separate-opex`

2. **src/ai_agent.py**
   - Reforçado prompt de interpretação com regras de identidade

3. **src/engines/library_assembler.py**
   - Corrigido mapeamento de `client_company` e `company_name`
   - Implementada lógica de filtragem por `output_mode`
   - Implementada geração de proposta NOC separada

4. **src/models.py**
   - (Sem alterações estruturais)

5. **README.md**
   - Atualizado com comandos corretos
   - Documentação dos novos recursos

### 🧪 Testes Realizados

**Cenário:** OFI - Datacenter Industrial
**Parâmetros:** `--output-mode full --separate-opex --term 60 --sizing standard --contingency low`

**Resultado:**
- ✅ 4 arquivos de proposta gerados corretamente
- ✅ QA aprovado (sem auto-referências)
- ✅ Todas as tabelas (MAT, MOD, DIV, SET) geradas
- ✅ Cliente identificado corretamente como "OFI - OLAM Foods Ingredients S.A."
- ✅ Provedor identificado corretamente como "EGE Soluções Industriais"

### 📊 Commits Relevantes

```
43587c5 - feat: add provider/client identity hardfix, QA validation and update README
ceb554f - fix: restore MAT/MOD/DIV/SET table generation (indentation bug)
034d305 - fix: correctly place table saving code inside main() after proposal generation
9aab560 - feat: control output modes (unified, full, splited) and standalone NOC proposal generation
2ac2364 - docs: add README.md with usage instructions and new output controls
```

### 🎯 Próximos Passos Sugeridos

1. ✅ Testar com outros cenários (Bionovis, Maratá, etc.)
2. ⏳ Validar proposta NOC com cliente real
3. ⏳ Ajustar padrões de sanitização conforme novos casos apareçam
4. ⏳ Implementar testes automatizados para QA
