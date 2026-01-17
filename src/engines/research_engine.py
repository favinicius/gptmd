import json
from datetime import datetime
from typing import Optional, Dict, Any, List
from src.models import CalculatedLabor
from src.ai_agent import AIAgent

class ResearchEngine:
    """
    Motor de Pesquisa de Atividades (v8.0)
    Responsável por estimar horas para atividades desconhecidas usando o prompt de engenharia.
    """
    def __init__(self, database, ai_agent: AIAgent):
        self.db = database
        self.ai = ai_agent

    def estimate_unknown_activity(self, activity_name: str, context: str = "") -> List[Dict[str, Any]]:
        """
        Usa o AIAgent para decompor uma atividade desconhecida seguindo o modelo de otimização de custos.
        """
        print(f"[*] Researching unknown activity: '{activity_name}'...")
        wbs = self.ai.research_technical_wbs(activity_name, context)
        
        if wbs:
            self.log_new_discovery({"activity": activity_name, "wbs": wbs})
        
        return wbs

    def log_new_discovery(self, discovery: Dict[str, Any]):
        """
        Registra descobertas para revisão humana posterior.
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "discovery": discovery
        }
        try:
            with open("data/discoveries_log.json", "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except:
             pass
