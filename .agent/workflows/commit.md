---
description: Realiza git add e git commit das alterações atuais
---

Este workflow agiliza o processo de salvar o progresso no Git, sugerindo ou aplicando uma mensagem de commit baseada no contexto.

// turbo-all
## Passos para Commit

1. Adicionar todas as alterações (ignorando arquivos indesejados via .gitignore)
```bash
git add .
```

2. Mostrar o que será commitado para confirmação visual
```bash
git status
```

3. Realizar o commit
> [!NOTE]
> Se você estiver executando este workflow, eu (Antigravity) vou gerar uma mensagem de commit descritiva baseada nas alterações acima. Se você quiser uma mensagem específica, me avise antes de rodar o workflow.

```bash
# Exemplo de comando que eu executarei após analisar o status:
# git commit -m "feat: implement research engine and project optimization"
```

4. Mostrar log final
```bash
git log -n 1
```
