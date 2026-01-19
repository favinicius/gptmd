"""
Configuração dos Coeficientes Comerciais para CAPEX.
Estes valores são utilizados para converter CUSTO em VALOR DE VENDA.
"""

# --- MÃO DE OBRA (MOD / SERVIÇOS) ---
# FIXO_DIVISOR_MOD: Engloba Impostos (ISS, PIS, COFINS, etc) e Margem de Lucro Desejada.
# Fórmula: Venda = Custo / (1 - FIXO_DIVISOR_MOD - (TAXA_FINANCEIRA_DIARIA_MOD * Dias))
FIXO_DIVISOR_MOD = 0.5079031
TAXA_FINANCEIRA_DIARIA_MOD = 0.00047623

# PRAZO_PADRAO_DIAS: Prazo de faturamento padrão utilizado se não especificado.
PRAZO_PADRAO_DIAS = 30

# --- MATERIAIS (MAT) ---
# FIXO_DIVISOR_MAT = 0.0  # Pendente
# TAXA_FINANCEIRA_DIARIA_MAT = 0.0 # Pendente

# --- SERVIÇOS E DESPESAS (SET / DIV) ---
# Coeficientes derivados de regressão linear para margens menores.
# Base: Markup Fixo ~25% e Taxa Financeira uniforme.
FIXO_DIVISOR_SET_DIV = 0.250768
TAXA_FINANCEIRA_DIARIA_SET_DIV = 0.00047614
