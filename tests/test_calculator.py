import unittest
from src.calculator import PricingEngine
from src.models import Intent, LogisticsOverride

class TestPricingEngine(unittest.TestCase):
    def setUp(self):
        self.engine = PricingEngine()

    def test_rounding_logic(self):
        # Regra C: Ceil -> Even
        # 3.1 -> 4 -> 4 (Even)
        # 3.0 -> 3 -> 4 (Even)
        # 4.0 -> 4 -> 4 (Even)
        # 2.1 -> 3 -> 4 (Even)
        
        self.assertEqual(self.engine._calculate_hours(3.1), 4)
        self.assertEqual(self.engine._calculate_hours(3.0), 4)
        self.assertEqual(self.engine._calculate_hours(4.0), 4)
        self.assertEqual(self.engine._calculate_hours(2.1), 4)
        self.assertEqual(self.engine._calculate_hours(0.1), 2)

    def test_contingency_logic(self):
        # Regra D: 20%, min 2, even
        # 10h * 0.2 = 2h -> 2 (Even)
        # 4h * 0.2 = 0.8 -> 1 -> min 2 -> 2
        # 100h * 0.2 = 20h -> 20 (Even)
        # 105h * 0.2 = 21 -> 21 -> 22 (Even)
        
        self.assertEqual(self.engine._add_contingency(10), 2)
        self.assertEqual(self.engine._add_contingency(4), 2)
        self.assertEqual(self.engine._add_contingency(100), 20)
        self.assertEqual(self.engine._add_contingency(105), 22)
        # 0 hours -> 0 contingency
        self.assertEqual(self.engine._add_contingency(0), 0)

    def test_calculate_proposal_basic(self):
        # Mock Intent
        intent = Intent(
            client_name="Test Client",
            company_name="Test Co",
            project_name="Test Project",
            scope_items=["Test Switch"], # Assuming this won't match real DB unless I mock DB or use real one
            logistics_override=LogisticsOverride()
        )
        
        # If "Test Switch" is not in DB, it won't add hardware, but might add labor default?
        # My code: loops scope_items. if hw_match, add. 
        # For labor: uses heuristic. "Test Switch" has "Switch" -> 8h base.
        
        proposal = self.engine.calculate_proposal(intent)
        
        # Verify Labor
        # Item: "Test Switch" -> Base 8h.
        # Project Complexity: "Média" (default) -> RoleConfig Medium (Tech + Aux + Mgr 8h).
        # Tech: 8h -> 8h. Cost 50. Total 400. * 3 (Final) = 1200.
        # Tech Cont: 2h. Cost 50. Total 100. * 3 = 300.
        # Aux: 8h -> 8h. Cost 25. Total 200. * 3 = 600.
        # Aux Cont: 2h. Cost 25. Total 50. * 3 = 150.
        # Mgr: 8h. Cost 100. Total 800. * 3 = 2400.
        
        # Let's check if we have labor items
        self.assertTrue(len(proposal.labor_table) > 0)
        
        # Check defaults
        tech_rows = [r for r in proposal.labor_table if r.role == "Técnico" and not r.is_contingency]
        self.assertTrue(len(tech_rows) >= 1)
        self.assertEqual(tech_rows[0].hours, 8)

if __name__ == '__main__':
    unittest.main()
