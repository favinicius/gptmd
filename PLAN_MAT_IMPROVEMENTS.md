# Plano Revisado: Melhorias Incrementais no MaterialEngine

## 🎯 Objetivo Ajustado
Melhorar a precisão do MaterialEngine sem quebrar funcionalidades existentes.

## ✅ O que JÁ funciona (NÃO TOCAR)
- Precificação comercial (PricingEngine)
- Campos de venda no ProposalData
- Lógica de fallback para itens não encontrados
- Sistema de QA e sanitização

## 🔧 Melhorias a Implementar

### 1. Busca Direta por Part Number (15 min)
**Problema:** Busca atual só procura P/N dentro de strings de contexto
**Solução:** Criar método `_search_by_partnumber()` que busca direto na lista

### 2. Busca Fuzzy por Nome (20 min)
**Problema:** Se o nome não bater exato, não encontra
**Solução:** Usar `difflib` para match por similaridade (>80%)

### 3. Logging de Mapeamento (10 min)
**Problema:** Não sabemos quais itens foram mapeados com sucesso
**Solução:** Adicionar log de debug mostrando taxa de sucesso

### 4. Validação de Disponibilidade (5 min)
**Problema:** Não verifica se item do DB está ativo
**Solução:** Adicionar campo `active: bool` no futuro (não implementar agora)

## 📝 Implementação

### Fase 1: Refatorar Busca (30 min)
```python
def _search_material(self, name: str, context: str, category: str) -> Optional[HardwareItem]:
    # 1. Busca exata por P/N
    # 2. Busca fuzzy por nome
    # 3. Fallback por categoria
    # 4. Return None se não encontrar
```

### Fase 2: Adicionar Logging (10 min)
```python
# Contador de sucessos/falhas
mapped_count = 0
manual_count = 0
```

### Fase 3: Teste (15 min)
- Rodar cenário OFI
- Verificar QA ainda passa
- Validar logs de mapeamento

## ⏱️ Tempo Total Estimado: 55 minutos

## 🔒 Proteções
- ✅ Não alterar PricingEngine
- ✅ Não alterar ProposalData
- ✅ Não alterar lógica de fallback
- ✅ Manter compatibilidade com templates

---
**Status:** Pronto para implementar
**Risco:** BAIXO (apenas melhoria interna do MaterialEngine)
