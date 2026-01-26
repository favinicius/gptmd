# GPT-Md (Gerador de Propostas Técnicas)

O **GPT-Md** é uma ferramenta CLI avançada para geração de propostas técnicas industriais, integrando inteligência artificial (Gemini) com motores de precificação determinísticos.

## ⚙️ Configuração do Ambiente

Este projeto utiliza **venv externo** para melhor performance e organização:

```bash
# Estrutura de diretórios
~/Desenvolvimento/
├── gptmd/              # Código do projeto
└── venvs/
    └── gptmd/          # Ambiente virtual (externo)
```

### Ativação do Ambiente (Opcional)
```bash
source ../venvs/gptmd/bin/activate
```

## 🚀 Como Usar

### Execução Direta (Recomendado)
Use o interpretador Python do venv diretamente:

```bash
export PYTHONPATH=$PYTHONPATH:.
../venvs/gptmd/bin/python src/main.py [OPÇÕES]
```

### Exemplo Completo
```bash
export PYTHONPATH=$PYTHONPATH:.
../venvs/gptmd/bin/python src/main.py \
  --instruction input/cenario-ofi-datacenter.txt \
  --use-docs input/docs/OFI_Pre-Projeto.pdf \
  --term 60 \
  --sizing standard \
  --contingency standard \
  --output-mode full \
  --separate-opex
```

### 📋 Argumentos Principais

| Argumento | Descrição |
| :--- | :--- |
| `--instruction <path>` | Caminho para o arquivo `.txt` com a descrição do cenário/escopo. |
| `--use-docs <files...>` | Lista de arquivos PDF/TXT/MD de referência técnica. |
| `--term <dias>` | Prazo de faturamento/pagamento (Ex: 30, 60, 90). |
| `--sizing <mode>` | Modo de dimensionamento: `aggressive`, `standard`, `secure`, `critical`. |
| `--contingency <level>` | Nível de contingência (SHE/Buffer): `low`, `standard`, `high`. |

### 🛠️ Controles de Saída (v5.0)

Controle quais arquivos de proposta deseja gerar:

| Modo de Saída (`--output-mode`) | Arquivos Gerados |
| :--- | :--- |
| `unified` (Padrão) | Apenas a proposta completa (Técnica + Comercial). |
| `full` | Gera as 3 versões: Unificada, Técnica e Comercial. |
| `splited` | Gera apenas os arquivos Técnica e Comercial separados. |

### 🛰️ Proposta de NOC/OPEX Isolada

Para gerar proposta de sustentação separada (aprovação independente):

```bash
../venvs/gptmd/bin/python src/main.py \
  --instruction input/cenario.txt \
  --separate-opex
```
Isso gerará o arquivo `PROPOSTA_NOC_SUSTENTACAO_...md` além das propostas CAPEX.

---

## 🏗️ Estrutura do Projeto

*   `src/`: Motores de cálculo e lógica de montagem.
*   `data/`: Catálogos de materiais e mão de obra (JSON).
*   `templates/`: Blocos de texto Markdown utilizados na montagem.
*   `output/`: Diretório onde os resultados (MD, CSV, Auditoria) são salvos por timestamp.

## 📊 Métricas e Benchmarks
Para visualizar a tabela de multiplicadores de esforço e contingência:
```bash
../venvs/gptmd/bin/python src/main.py --help-metrics
```

## 🔍 Verificação de Qualidade
O sistema inclui QA automático que verifica:
- Integridade das seções da proposta
- Nomes de cliente e provedor corretos
- Ausência de auto-referências (EGE -> EGE)
