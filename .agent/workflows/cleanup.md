---
description: Limpeza profunda do projeto (results, logs, debugs e temporários)
---

Este workflow automatiza a limpeza exaustiva do projeto para manter a performance, evitar poluição visual e garantir que apenas artefatos relevantes permaneçam.

// turbo-all
## Passos para Limpeza

1. Limpar resultados e outputs antigos (mantendo os 3 mais recentes de cada)
```bash
ls -dt output/results/*/ 2>/dev/null | tail -n +4 | xargs rm -rf 2>/dev/null || true
ls -dt output/2026-*/ 2>/dev/null | tail -n +4 | xargs rm -rf 2>/dev/null || true
```

2. Limpar benchmarks e análises antigas (mantendo os 3 mais recentes)
```bash
ls -dt output/benchmarks/*/ 2>/dev/null | tail -n +4 | xargs rm -rf 2>/dev/null || true
ls -dt output/analises/*/ 2>/dev/null | tail -n +4 | xargs rm -rf 2>/dev/null || true
```

3. Limpar arquivos de LOG, TXT e PID na raiz (respeitando o requirements.txt)
```bash
find . -maxdepth 1 -name "*.log" -delete
find . -maxdepth 1 -name "*.txt" ! -name "requirements.txt" -delete
find . -maxdepth 1 -name "*.pid" -delete
find . -maxdepth 1 -name "*.bak" -delete
```

4. Limpar diretório de debug
```bash
rm -rf output/debug/* 2>/dev/null || true
```

5. Remover arquivos temporários (.DS_Store)
```bash
find . -name ".DS_Store" -delete
```

6. Relatar status final
```bash
echo "🚀 Limpeza profunda concluída!"
echo "--- Status do Diretório Output ---"
ls -lh output/ | head -n 15
```
