"""
Configuração dos Coeficientes Comerciais para CAPEX.
Estes valores são utilizados para converter CUSTO em VALOR DE VENDA.
"""

# --- MÃO DE OBRA (MOD / SERVIÇOS) ---
# Fórmula: Venda = Custo / (FIXO_DIVISOR_MOD - (TAXA_FINANCEIRA_DIARIA_MOD * Dias))
# Divisor de 0.4920969 equivale a uma margem/impostos de ~50.79%
FIXO_DIVISOR_MOD = 0.4920969
TAXA_FINANCEIRA_DIARIA_MOD = 0.00047623

# PRAZO_PADRAO_DIAS: Prazo de faturamento padrão utilizado se não especificado.
PRAZO_PADRAO_DIAS = 30

# --- MATERIAIS (MAT) ---
# Baseado na tabela progressiva: R$ 1000 (custo) -> R$ 1688,92 (venda 30 dias)
# Divisor de 0.6063823 equivale a uma margem/impostos de ~39.36%
FIXO_DIVISOR_MAT = 0.6063823
TAXA_FINANCEIRA_DIARIA_MAT = 0.00047622

# --- SERVIÇOS E DESPESAS (SET / DIV) ---
# Divisor de 0.749232 equivale a uma margem/impostos de ~25.07%
FIXO_DIVISOR_SET_DIV = 0.749232
TAXA_FINANCEIRA_DIARIA_SET_DIV = 0.00047614
