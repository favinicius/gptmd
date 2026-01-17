
from typing import Optional, List, Dict, Any
from src.database import Database
from src.ai_agent import AIAgent
import json
import difflib

class ResearchEngine:
    """
    Engine responsável pela inferência de atividades desconhecidas (Missed Bundles).
    Utiliza IA para decompor macro-atividades em WBS técnicos granulares.
    """
    def __init__(self, db: Database, agent: AIAgent):
        self.db = db
        self.agent = agent
        self.cache = {} # Cache em memória para evitar chamadas repetidas na mesma execução
        # Cache de roles válidos para validação rápida
        self.valid_roles = [r.role for r in self.db.labor.roles] if self.db.labor else ["Auxiliar de Redes", "Analista de Infra", "Gestor de Projetos", "Engenheiro de Redes", "Arquiteto de Soluções"]

    def _find_best_role_match(self, suggested_role: str) -> str:
        """Encontra o role válido mais próximo do sugerido pela IA."""
        suggested_clean = suggested_role.strip()
        
        # Tentativa exata (case insensitive)
        for role in self.valid_roles:
            if role.lower() == suggested_clean.lower():
                return role
                
        # Tentativa por similaridade
        matches = difflib.get_close_matches(suggested_clean, self.valid_roles, n=1, cutoff=0.6)
        if matches:
            return matches[0]
            
        # Fallback inteligente baseada em keywords
        lower_sug = suggested_clean.lower()
        if "gerente" in lower_sug or "gestor" in lower_sug:
            return "Gestor de Projetos"
        if "engenheiro" in lower_sug or "arquiteto" in lower_sug:
            return "Engenheiro de Redes"
        if "auxiliar" in lower_sug or "ajudante" in lower_sug:
            return "Auxiliar de Redes"
            
        return "Analista de Infra" # Default safe

    def estimate_unknown_activity(self, activity_name: str, context_note: str = ""):
        """
        Tenta decompor uma atividade desconhecida usando IA.
        Retorna uma lista de dicionários com chaves compatíveis com ActivityLibraryItem.
        """
        cache_key = f"{activity_name}|{context_note}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        print(f"[*] Research Engine: Investigando '{activity_name}'...")
        
        try:
            # Chama o método especializado do agente
            # Passamos a lista de roles válidos no contexto para guiar a IA
            roles_context = ", ".join(self.valid_roles)
            raw_wbs = self.agent.research_technical_wbs(activity_name, f"{context_note}. Roles permitidos: {roles_context}")
            
            if not raw_wbs:
                return None
            
            # Validação e Normalização
            validated_wbs = []
            for item in raw_wbs:
                suggested_role = item.get("role", "Analista")
                metric_role = self._find_best_role_match(suggested_role)
                
                # Garante custo (deve existir pois o role foi validado contra o DB)
                role_cost = self.db.get_role_cost(metric_role)
                
                validated_wbs.append({
                    "id": item.get("id", "RES_999"),
                    "category": self._map_category(item.get("category", "PHASE_2")),
                    "name": item.get("name", "Atividade Pesquisada"),
                    "role": metric_role,
                    "unit_hours": float(item.get("unit_hours", 1.0)),
                    "description": item.get("description", ""),
                    "setup_hours": 0.0,
                    "tags": ["research", "ai-generated"]
                })
            
            self.cache[cache_key] = validated_wbs
            
            # Log discovery for human review (v8.1 - Active Learning Staging)
            self._log_discovery(activity_name, context_note, validated_wbs)
            
            return validated_wbs

        except Exception as e:
            print(f"[!] Erro no ResearchEngine: {e}")
            return None

    def _log_discovery(self, term: str, context: str, wbs: List[Dict]):
        """Salva a descoberta em um arquivo de log para revisão humana posterior."""
        import json
        from pathlib import Path
        from datetime import datetime

        log_file = Path("data/discoveries_log.json")
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "trigger_term": term,
            "context": context,
            "suggested_wbs": wbs,
            "status": "pending_review"
        }

        try:
            # Append to list or create new
            if log_file.exists():
                with open(log_file, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        data = []
            else:
                data = []

            # Check for duplicates (simple check by term)
            # Update existing if pending, otherwise append
            existing_idx = next((i for i, x in enumerate(data) if x["trigger_term"] == term and x["status"] == "pending_review"), None)
            
            if existing_idx is not None:
                data[existing_idx] = entry
            else:
                data.append(entry)

            with open(log_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                
            print(f"[*] Research Engine: Descoberta salva em '{log_file}' para revisão.")

        except Exception as e:
            print(f"[!] Falha ao logar descoberta: {e}")

    def _map_category(self, ai_category: str) -> str:
        """Mapeia categorias retornadas pela IA para os nomes internos"""
        mapping = {
            "PHASE_1": "Planejamento",
            "PHASE_2": "Execução",  # Físico
            "PHASE_3": "Execução",  # Lógico/Rede -> Execução
            "PHASE_4": "Validação",
            "PHASE_5": "Gerenciamento"
        }
        # Tenta mapear, se falhar retorna a própria string ou Execução default
        norm = ai_category.strip().upper()
        for k, v in mapping.items():
            if k in norm: return v
        
        return "Execução"
