
import unittest
import json
import os
from pathlib import Path
from src.database import Database
from src.ai_agent import AIAgent
from src.engines.research_engine import ResearchEngine
from dotenv import load_dotenv

# Load env vars for real AI calls (since we are testing the full flow including API)
load_dotenv()

class TestResearchEngineManual(unittest.TestCase):
    def setUp(self):
        self.db = Database()
        self.agent = AIAgent()
        self.engine = ResearchEngine(self.db, self.agent)
        self.log_file = Path("data/discoveries_log.json")
        
        # Backup existing log if any
        if self.log_file.exists():
            self.log_file.rename("data/discoveries_log.json.bak")

    def tearDown(self):
        # Restore backup
        if Path("data/discoveries_log.json.bak").exists():
            if self.log_file.exists():
                self.log_file.unlink()
            Path("data/discoveries_log.json.bak").rename(self.log_file)
        # Or just remove the test log if no backup existed
        elif self.log_file.exists():
            self.log_file.unlink()

    def test_research_unknown_activity(self):
        print("\n[TEST] Iniciando teste de pesquisa de atividade desconhecida...")
        
        activity_name = "Instalação e Configuração de Sistema Anti-DDoS Dedicado"
        context = "Requires appliance mounting and BGP configuration."
        
        wbs = self.engine.estimate_unknown_activity(activity_name, context)
        
        # Assertions on return
        self.assertIsNotNone(wbs, "Research Engine retornou None")
        self.assertIsInstance(wbs, list, "Research Engine não retornou uma lista")
        self.assertTrue(len(wbs) > 0, "Lista de WBS vazia")
        
        print(f"[TEST] WBS Gerado: {len(wbs)} itens.")
        for item in wbs:
            print(f" - {item['role']}: {item['name']} ({item['unit_hours']}h)")
            self.assertIn("id", item)
            self.assertIn("category", item)
            self.assertIn("role", item)
            self.assertIn("unit_hours", item)
            
        # Assertions on Log Persistence
        self.assertTrue(self.log_file.exists(), "Arquivo de log não foi criado")
        
        with open(self.log_file, "r", encoding="utf-8") as f:
            log_data = json.load(f)
            
        found = False
        for entry in log_data:
            if entry["trigger_term"] == activity_name:
                found = True
                self.assertEqual(entry["context"], context)
                self.assertEqual(entry["status"], "pending_review")
                # Check consistency between returned WBS and logged WBS
                # Note: The log saves the 'validated_wbs' which translates roles/categories
                self.assertEqual(len(entry["suggested_wbs"]), len(wbs))
                break
                
        self.assertTrue(found, "Entrada não encontrada no log JSON")
        print("[TEST] Log verificado com sucesso.")

if __name__ == "__main__":
    unittest.main()
