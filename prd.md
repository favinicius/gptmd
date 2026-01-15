# 📄 PRD: GPT-Md (Gerador de Propostas Técnicas em Markdown)
**Versão:** MVP 1.0  
**Stack:** Python 3.10+ | Google Gemini API | Pandas  
**Contexto:** Engenharia de Precificação Turnkey (EGE Soluções)

## 1. Visão do Produto
O **GPT-Md** é uma ferramenta de automação de engenharia de vendas (CLI/Script) que utiliza IA Generativa (Gemini) orquestrada por Python.
Seu objetivo é ler documentos de entrada (RFQs/Ativos), interpretar instruções em linguagem natural (ex: regras de logística específicas) e gerar uma **Proposta Técnica completa em Markdown**, garantindo precisão matemática nos cálculos através de tabelas pré-definidas (JSON).

## 2. Arquitetura da Solução

O sistema não será um "chat" solto. Ele funcionará como um **Pipeline de Dados** com 3 estágios principais:

1.  **Ingestão & Compreensão (AI + OCR):** Lê PDFs e a instrução do usuário.
2.  **Motor de Cálculo (Python Determinístico):** Cruza os itens identificados com os JSONs (`db_mat`, `db_mod`, etc.) e aplica as regras de negócio (`logic_business_rules.js` traduzido para Python). **A IA não faz contas, ela seleciona itens.**
3.  **Geração de Documento (AI + Template):** Monta o texto final em Markdown usando os dados calculados e o tom de voz dos exemplos.

## 3. Estrutura de Diretórios (File System)

O projeto será organizado da seguinte forma no seu ambiente (Antigravity/Local):

```text
GPT-Md/
├── data/
│   ├── db_mat.json         # Catálogo Materiais (Hardware/Licenças)
│   ├── db_mod.json         # Catálogo Mão de Obra
│   ├── db_set.json         # Catálogo Serviços Externos
│   └── db_div.json         # Catálogo Despesas/Logística
├── input/
│   ├── docs/               # PDFs do cliente (RFQs, Listas)
│   └── instruction.txt     # O prompt de instrução natural (ex: Cenário "João")
├── output/
│   ├── debug/              # Logs intermediários (itens extraídos)
│   └── proposta_final.md   # O resultado final
├── src/
│   ├── context_loader.py   # Carrega JSONs e PDFs
│   ├── ai_agent.py         # Wrapper para chamadas ao Gemini API
│   ├── calculator.py       # Lógica de negócio (tradução do logic_business_rules.js)
│   └── main.py             # Orquestrador
├── templates/
│   └── proposal_structure.md # Esqueleto base da proposta (baseado nos exemplos)
├── requirements.txt
└── .env                    # GEMINI_API_KEY
```

## 4. Requisitos Funcionais (O Workflow)

### 4.1. Módulo de Interpretação (Agente 1)
*   **Entrada:** Arquivos na pasta `input/docs` + Texto em `input/instruction.txt`.
*   **Processamento:** O Gemini deve ler o texto bruto e extrair uma **Lista de Intenções Estruturada**.
*   **Saída Esperada (JSON Intermediário):**
    ```json
    {
      "client_name": "João - Máquinas Agrícolas",
      "scope_items": ["Switch Core", "Cabling", "Serviço de Fusão"],
      "logistics_override": {
        "transport_provider": "client", // Cliente compra equipamentos
        "consulting": true,             // Consultoria deve ser cobrada
        "travel_segments": 5,
        "stay_duration_days": [5, 5, 5, 5, 15]
      }
    }
    ```

### 4.2. Motor de Precificação (Agente 2 - Python Puro)
*   **Entrada:** Lista de Intenções + JSONs de Banco de Dados.
*   **Regras de Negócio (Hardcoded em Python):**
    *   **Regra A/E:** Se tem hardware, verifica se precisa de `MISC_PCT` (10%).
    *   **Regra C/F:** Se a complexidade é "Alta", adiciona horas de Gestor e Engenheiro automaticamente.
    *   **Regra D:** Se tem fibra/cabeamento, adiciona item de "Certificação" (Custo SET + MOD).
    *   **Regra Logística (Custom):** Aplica a regra do "João": zera custo de frete de material (cliente compra), mas adiciona horas de consultoria de especificação. Calcula diárias de hotel e deslocamento baseadas no array `[5, 5, 5, 5, 15]`.
*   **Saída:** Dataframes Pandas (MAT, MOD, SET, DIV) com valores finais calculados.

### 4.3. Gerador de Proposta (Agente 3)
*   **Entrada:** Dataframes calculados + Template Markdown + Exemplos de Estilo (`gpta-produto-completo.md` e PDFs de exemplo).
*   **Processamento:** O Gemini preenche o template. Ele **não inventa preços**, apenas formata os dados que o Python calculou e escreve os textos descritivos (Objetivo, Benefícios, Escopo).
*   **Saída:** Arquivo `.md` pronto.

## 5. Mapeamento de Regras de Negócio (JS -> Python)

A lógica contida no seu arquivo `logic_business_rules.js` será migrada para `src/calculator.py`:

| Regra Original (JS) | Implementação Python |
| :--- | :--- |
| `CONTINGENCY_PCT = 0.20` | Constante no script. Aplicada sobre total de horas. |
| `calculateHours(base)` | Função `math.ceil` com lógica de arredondamento par. |
| `item.hardware.push(MISC)` | Função que itera sobre DataFrame MAT e insere linha extra se `cost_net > 0`. |
| `roleMap` (Low/Med/High) | Dicionário Python mapeando complexidade -> horas de engenharia/gestão. |
| Seleção de Switch (Rockwell vs Siemens) | Lógica condicional: Se instrução diz "Padrão Aberto" -> Siemens; Se "Brownfield" -> Rockwell. |

## 6. Instruções para o "Prompt Poderoso" (Etapa Seguinte)

Para criar os scripts na próxima etapa, utilizaremos um prompt de sistema para o Gemini que conterá:
1.  **Role:** Senior Python Dev.
2.  **Context:** O conteúdo integral dos JSONs (para ele saber os campos) e do `workflow_v14.md` (para ele entender a lógica de seleção).
3.  **Task:** Gerar o código Python modularizado conforme a estrutura acima.

