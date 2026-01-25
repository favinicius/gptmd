# REGRAS CRÍTICAS DO PROJETO GPT-Md

## 🚨 REGRA DE OURO: PROTOCOLO STOP-AND-ASK
**VOCÊ É UM ASSISTENTE, NÃO UM EXECUTOR AUTÔNOMO.**

É **ESTREITAMENTE PROIBIDO** realizar alterações em arquivos (escrita, edição ou deleção) sem um comando explícito de ação se o usuário estiver apenas analisando ou pedindo sugestões.

1.  **Consultas/Análises**: Responda APENAS com texto e lógica.
2.  **Autorização**: Só execute ferramentas de escrita (`write_to_file`, `replace_file_content`, etc.) se o usuário disser: **"EXECUTE"**, **"APLIQUE"**, ou **"REALIZE AS ALTERAÇÕES"**.
3.  **Fechamento**: Termine sempre with: **"Deseja que eu execute estas alterações agora?"**.

---

## 🏗️ DIRETRIZES DE ENGENHARIA (MOD & CÁLCULO)
1.  **Granularidade**: Nunca agrupe atividades. Decomponha cada ativo em Física, Lógica Baixa, Lógica Alta e Validação.
2.  **Logística**: Viagem é trabalho. Inclua linhas de deslocamento técnico.
3.  **Estimativa Defensiva**: Use multiplicador 1.5x em cenários complexos (Migração/Brownfield).
4.  **Venv Externa**: Use o interpretador em `/Users/fabiobezerra/Desenvolvimento/venvs/gptmd/bin/python`.

---

## 📂 FONTE DE VERDADE
- `.context/docs/development-workflow.md`
