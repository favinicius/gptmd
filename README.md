# GPT-Md (Gerador de Propostas Técnicas)

O **GPT-Md** é uma ferramenta CLI avançada para geração de propostas técnicas industriais, integrando inteligência artificial (Gemini) com motores de precificação determinísticos.

## 🚀 Como Usar

Para executar o gerador, utilize o script `src/main.py` através do interpretador Python do ambiente virtual.

```bash
export PYTHONPATH=$PYTHONPATH:.
python src/main.py [OPÇÕES]
```

### 📋 Argumentos Principais

| Argumento | Descrição |
| :--- | :--- |
| `--instruction <path>` | Caminho para o arquivo `.txt` com a descrição do cenário/escopo. |
| `--use-docs <files...>` | Lista de arquivos PDF/TXT/MD de referência técnica. |
| `--term <dias>` | Prazo de faturamento/pagamento (Ex: 30, 60, 90). |
| `--sizing <mode>` | Modo de dimensionamento: `aggressive`, `standard`, `secure`, `critical`. |
| `--contingency <level>` | Nível de contingência (SHE/Buffer): `low`, `standard`, `high`. |

### 🛠️ Controles de Saída (Novidade v5.0)

Agora você pode controlar quais arquivos de proposta deseja gerar:

| Modo de Saída (`--output-mode`) | Arquivos Gerados |
| :--- | :--- |
| `unified` (Padrão) | Apenas a proposta completa (Técnica + Comercial). |
| `full` | Gera as 3 versões: Unificada, Técnica e Comercial de uma vez. |
| `splited` | Gera apenas os arquivos Técnica e Comercial separados. |

### 🛰️ Proposta de NOC/OPEX Isolada

Se o projeto incluir serviços de sustentação (NOC) e você precisar de uma proposta avulsa para aprovação independente:

```bash
python src/main.py --instruction input/cenario.txt --separate-opex
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
python src/main.py --help-metrics
```
