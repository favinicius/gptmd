from src.config.commerce_config import (
    FIXO_DIVISOR_MOD, 
    TAXA_FINANCEIRA_DIARIA_MOD, 
    FIXO_DIVISOR_SET_DIV, 
    TAXA_FINANCEIRA_DIARIA_SET_DIV, 
    PRAZO_PADRAO_DIAS
)

class PricingEngine:
    """
    Motor de Precificação Comercial. 
    Converte custos técnicos em valores de venda mandatórios para o template comercial.
    """

    @staticmethod
    def calculate_generic_selling_price(cost: float, term_days: int, fixed_markup: float, daily_rate: float) -> float:
        """
        Método genérico de cálculo de venda.
        Regra: Venda = Custo / (1 - Markup_Fixo - (Taxa_Financeira_Diaria * Dias))
        """
        if cost <= 0:
            return 0.0
            
        divisor = 1.0 - fixed_markup - (daily_rate * term_days)
        
        if divisor <= 0.01: 
            divisor = 0.01
            
        selling_price = cost / divisor
        return round(selling_price, 2)

    @staticmethod
    def calculate_mod_selling_price(cost: float, term_days: int = PRAZO_PADRAO_DIAS) -> float:
        """
        Calcula o valor de venda para Mão-de-Obra (MOD).
        """
        return PricingEngine.calculate_generic_selling_price(
            cost, term_days, FIXO_DIVISOR_MOD, TAXA_FINANCEIRA_DIARIA_MOD
        )

    @staticmethod
    def calculate_set_div_selling_price(cost: float, term_days: int = PRAZO_PADRAO_DIAS) -> float:
        """
        Calcula o valor de venda para Serviços e Despesas (SET/DIV).
        """
        return PricingEngine.calculate_generic_selling_price(
            cost, term_days, FIXO_DIVISOR_SET_DIV, TAXA_FINANCEIRA_DIARIA_SET_DIV
        )

    @staticmethod
    def calculate_proposal_selling_prices(proposal_data, term_days: int = PRAZO_PADRAO_DIAS):
        """
        Ajusta todos os totais da proposta para valores de venda comercial.
        """
        # MOD (Mão de Obra)
        proposal_data.total_labor_venda = PricingEngine.calculate_mod_selling_price(
            proposal_data.total_labor, 
            term_days
        )

        # SET (Serviços) e DIV (Despesas)
        proposal_data.total_services_venda = PricingEngine.calculate_set_div_selling_price(
            proposal_data.total_services,
            term_days
        )
        proposal_data.total_expenses_venda = PricingEngine.calculate_set_div_selling_price(
            proposal_data.total_expenses,
            term_days
        )
        
        # Grand total comercial (soma dos valores de venda)
        # Nota: MAT (Hardware) ainda entra pelo total normal (custo ou markup fixo antigo se houver)
        proposal_data.grand_total_venda = (
            proposal_data.total_labor_venda + 
            proposal_data.total_hardware + 
            proposal_data.total_services_venda + 
            proposal_data.total_expenses_venda
        )
