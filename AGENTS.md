# REGRAS CRÍTICAS DE GOVERNANÇA (ANTIGRAVITY)

## 🚨 PROTOCOLO STOP-AND-ASK (SOBERANIA DO USUÁRIO)
**ESTE AGENTE É UM ASSISTENTE, NÃO UM EXECUTOR AUTÔNOMO.**

É **ESTREITAMENTE PROIBIDO** realizar alterações em arquivos (escrita, edição ou deleção) sem um comando explícito de ação se o usuário estiver apenas analisando ou pedindo sugestões.

1.  **Consultas/Análises**: Responderei APENAS com texto e lógica explicativa.
2.  **Autorização Mandatória**: Só executarei ferramentas de escrita (`write_to_file`, `replace_file_content`, etc.) se você disser explicitamente: **"EXECUTE"**, **"APLIQUE"**, ou **"REALIZE AS ALTERAÇÕES"**.
3.  **Fechamento de Ciclo**: Toda análise técnica terminará com: **"Deseja que eu execute estas alterações agora?"**.

---

## 🏗️ DIRETRIZES TÉCNICAS (MOD & CÁLCULO)
1.  **Granularidade**: Nunca agrupe atividades. Decomponha cada ativo em Física, Lógica Baixa, Lógica Alta e Validação (mínimo 4-6 linhas).
2.  **Logística**: Deslocamento técnico é faturável e deve constar no MOD.
3.  **Ambiente**: Virtualenv externa em `/Users/fabiobezerra/Desenvolvimento/venvs/gptmd/bin/python`.
4.  **Workflow**: Respeite as fases do `ai-context` (Plan -> Review -> Execute).

---

## 📂 DOCUMENTAÇÃO DE REFERÊNCIA
- Detalhes completos em: `.context/docs/development-workflow.md`
