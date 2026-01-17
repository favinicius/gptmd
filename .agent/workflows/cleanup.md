---
description: Limpeza automática do projeto (output, debug, benchmarks e arquivos temporários)
---

Este workflow automatiza a limpeza do projeto para manter a performance e evitar travamentos por excesso de objetos indexados.

// turbo-all
## Passos para Limpeza

1. Limpar resultados antigos (mantendo os 5 mais recentes)
```bash
ls -dt output/results/*/ 2>/dev/null | tail -n +6 | xargs rm -rf 2>/dev/null || true
ls -dt output/2026-*/ 2>/dev/null | tail -n +6 | xargs rm -rf 2>/dev/null || true
```

2. Limpar benchmarks e análises antigas (mantendo os 5 mais recentes)
```bash
ls -dt output/benchmarks/*/ 2>/dev/null | tail -n +6 | xargs rm -rf 2>/dev/null || true
ls -dt output/analises/*/ 2>/dev/null | tail -n +6 | xargs rm -rf 2>/dev/null || true
```

3. Limpar diretório de debug
```bash
rm -rf output/debug/* 2>/dev/null || true
```

4. Remover arquivos temporários do sistema (.DS_Store)
```bash
find . -name ".DS_Store" -delete
```

5. Limpeza preventiva dos playbooks dos agentes (remove referências ao venv)
```bash
sed -i '' '/venv\//d' .context/agents/*.md 2>/dev/null || true
```

6. Relatar status final
```bash
echo "Limpeza concluída com sucesso!"
find . -maxdepth 1 -not -path '*/.*' | xargs -I {} sh -c 'echo "$(find "{}" | wc -l) {}"' | sort -nr
```
