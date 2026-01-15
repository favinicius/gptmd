import unittest
from src.calculator import PricingEngine
from src.models import Intent, LogisticsOverride

class TestCalculatorPhase2(unittest.TestCase):
    def setUp(self):
        self.engine = PricingEngine()

    def test_fuzzy_matching(self):
        # O banco tem "Switch Gerenciável Scalance XC206 (6 portas)"
        # Vamos testar buscas genéricas
        match1 = self.engine.find_best_match("XC206", self.engine.db.hardware)
        self.assertIsNotNone(match1)
        self.assertEqual(match1.partnumber, "6GK5206-2BS00-2AC2")
        
        match2 = self.engine.find_best_match("Switch", self.engine.db.hardware)
        self.assertIsNotNone(match2)
        
    def test_supply_only_logic(self):
        intent = Intent(
            client_name="Test",
            company_name="Test Co",
            project_name="Project",
            scope_items=["XC206"],
            hardware_supply_by_client=True,
            logistics_override=LogisticsOverride()
        )
        proposal = self.engine.calculate_proposal(intent)
        
        # Hardware deve estar zerado na venda (total_hardware = 0)
        self.assertEqual(proposal.total_hardware, 0.0)
        
        # Deve ter adicionado Consultoria em Labor
        consulting_items = [l for l in proposal.labor_table if "Consultoria" in l.activity]
        self.assertTrue(len(consulting_items) > 0)
        # Horas devem ser 16h (pois horas técnicas de um switch são poucas, 10% seria < 8h)
        self.assertEqual(consulting_items[0].hours, 16)

    def test_complex_logistics(self):
        intent = Intent(
            client_name="Test",
            company_name="Test Co",
            project_name="Project",
            scope_items=["XC206"],
            hardware_supply_by_client=False,
            logistics_override=LogisticsOverride(travel_segments=[5, 5, 15])
        )
        proposal = self.engine.calculate_proposal(intent)
        
        # Total days = 5+5+15 = 25
        # Total trips = 3
        
        hospedagem = [e for e in proposal.expense_table if "Hospedagem" in e.description]
        self.assertEqual(hospedagem[0].qty, 25)
        
        deslocamento = [e for e in proposal.expense_table if "Deslocamento" in e.description]
        # viagens (3) * 500km = 1500km
        self.assertEqual(deslocamento[0].qty, 1500)

    def test_team_size_logistics(self):
        intent = Intent(
            client_name="Test",
            company_name="Test Co",
            project_name="Project",
            scope_items=["XC206"],
            hardware_supply_by_client=False,
            logistics_override=LogisticsOverride(travel_segments=[35], team_size=3)
        )
        proposal = self.engine.calculate_proposal(intent)
        
        # Total days = 35 * 3 = 105 diárias
        hospedagem = [e for e in proposal.expense_table if "Hospedagem" in e.description]
        self.assertEqual(hospedagem[0].qty, 105)
        
        alimentacao = [e for e in proposal.expense_table if "Alimentação" in e.description]
        self.assertEqual(alimentacao[0].qty, 105)

if __name__ == '__main__':
    unittest.main()
