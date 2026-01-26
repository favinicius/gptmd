# Plano de Execução: Reengenharia Motor MAT v1.0

## 🎯 Objetivo
Transformar o MaterialEngine em motor determinístico, eliminando alucinações de custo e implementando margens comerciais progressivas.

## 📋 Pré-requisitos Verificados
- ✅ Código atual commitado (último: 6417e1f)
- ✅ Mudanças em data/ e input/ salvas em stash
- ✅ Sistema de QA funcionando
- ✅ Correções de identidade preservadas

## 🔍 Análise Prévia

### Estado Atual do MaterialEngine
**Arquivo:** `src/engines/material_engine.py`
**Comportamento Atual:**
- Usa heurísticas para detectar tipos de hardware
- Não consulta db_mat.json de forma estruturada
- Custos podem ser inventados pela IA
- Sem margem comercial diferenciada

### Estado Atual do db_mat.json
**Estrutura:**
```json
{
  "categories": {
    "switch": [...],
    "server": [...],
    "storage": [...],
    ...
  }
}
```

## 📝 Plano de Execução (PREVC)

### FASE P: Planejamento (30 min)
**P1.** Analisar estrutura completa do db_mat.json
**P2.** Mapear palavras-chave de detecção por categoria
**P3.** Definir coeficientes comerciais em commerce_config.py
**P4.** Desenhar fluxo de fallback (Exato → Fuzzy → Placeholder)

### FASE R: Review (15 min)
**R1.** Revisar impacto no PricingEngine
**R2.** Validar compatibilidade com templates existentes
**R3.** Verificar se não quebra QA e sanitização

### FASE E: Execução (60 min)
**E1.** Criar função `search_material_in_db()` no MaterialEngine
**E2.** Implementar lógica de busca em 3 níveis:
   - Nível 1: Match exato por Part Number
   - Nível 2: Match fuzzy por nome/descrição
   - Nível 3: Placeholder "Cotação Manual"
**E3.** Atualizar `calculate_hardware()` para usar a nova busca
**E4.** Implementar `calculate_mat_selling_price()` no PricingEngine
**E5.** Adicionar campos de venda em ProposalData

### FASE V: Verificação (30 min)
**V1.** Criar cenário de teste com itens conhecidos e desconhecidos
**V2.** Executar teste e validar:
   - Itens conhecidos: P/N correto + custo do DB
   - Itens desconhecidos: Placeholder + custo R$ 0,00
   - Margem progressiva funcionando (60 dias > 30 dias)
**V3.** Validar QA automático ainda funciona
**V4.** Validar arquivos MAT.md e MAT.csv gerados

### FASE C: Conclusão (15 min)
**C1.** Commitar mudanças com mensagem descritiva
**C2.** Atualizar CHANGELOG.md
**C3.** Marcar plano como concluído

## ⚠️ Pontos de Atenção (Não Quebrar)

1. **Sistema de QA** - Manter run_quality_check() intacto
2. **Sanitização** - Não tocar em sanitize_content()
3. **Correção de Identidade** - Preservar hardfix de provider/cliente
4. **Templates** - Manter compatibilidade com library_assembler
5. **Arquivos de Saída** - Garantir que MAT.md/csv continuam sendo gerados

## 🔄 Estratégia de Rollback
Se algo der errado:
```bash
git reset --hard HEAD
git stash pop
```

## 📊 Critérios de Sucesso
- [ ] Zero alucinações de custo (itens desconhecidos = R$ 0,00)
- [ ] Todos os itens mapeados têm P/N oficial
- [ ] Margem comercial calculada corretamente
- [ ] QA continua aprovando propostas
- [ ] Nenhuma regressão nos testes OFI

---
**Início:** 2026-01-26 17:30
**Estimativa:** 2h30min
**Status:** 🟢 PRONTO PARA INICIAR
