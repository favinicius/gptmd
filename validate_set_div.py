from src.engines.pricing_engine import PricingEngine

def validate_math():
    base_cost = 100.00
    reference_table = [
        (0, 133.47),
        (1, 133.55), # Não explicitado no código, mas inferido
        (7, 134.07),
        (14, 134.67),
        (30, 136.06),
        (45, 137.40),
        (60, 138.76),
        (90, 141.57),
        (120, 144.49),
        (150, 147.53),
        (180, 150.71)
    ]

    print(f"Validating Pricing Logic for Cost R$ {base_cost:.2f}")
    print(f"{'Prazo':<5} | {'Ref Venda':<10} | {'Calc Venda':<10} | {'Diff':<10}")
    print("-" * 45)

    for days, ref_price in reference_table:
        calc_price = PricingEngine.calculate_set_div_selling_price(base_cost, days)
        diff = calc_price - ref_price
        print(f"{days:<5} | {ref_price:<10.2f} | {calc_price:<10.2f} | {diff:<10.2f}")

if __name__ == "__main__":
    validate_math()
