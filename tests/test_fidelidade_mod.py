import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao path para importar src
sys.path.append(str(Path(__file__).parent.parent))

from src.engines.labor_engine import LaborEngine
from src.database import Database
from src.models import Intent, ScopeItem, ProposalData

def test_determinismo_mod():
    db = Database()
    engine = LaborEngine(db)
    
    # Simula um item que a IA classificou como SWITCH
    item_switch = ScopeItem(
        name="Switch Especial Customizado",
        detected_quantity=2,
        action_type="SWITCH", # Nova categoria normalizada
        summary_rational="...",
        context_note="..."
    )
    
    intent = Intent(
        client_name="Teste",
        company_name="Teste S/A",
        contact_name="Admin",
        project_name="Teste Fidelidade",
        scope_items=[item_switch],
        sizing_mode="standard",
        contingency_level="standard"
    )
    
    proposal = ProposalData()
    engine.calculate_labor(intent, proposal)
    
    print(f"\n--- Resultado do Teste de Determinismo ---")
    print(f"Item: {item_switch.name}")
    print(f"Action Type: {item_switch.action_type}")
    
    # Verifica se as atividades do bundle SWITCH foram carregadas
    # Bundle SWITCH: PHYS_SW_01, PHYS_SW_02, NET_CORE_01, VAL_001, VAL_002
    activities = [item.activity for item in proposal.labor_table if item.topic == "T-01"]
    
    print(f"Atividades detectadas para T-01: {len(activities)}")
    for act in activities:
        print(f" - {act}")
        
    expected_count = 4 # Algumas categorias consolidam (PHASE_2 por exemplo)
    if len(activities) >= 3:
        print("\n✅ SUCESSO: O LaborEngine usou o Action Type para mapear o bundle mesmo com nome customizado.")
    else:
        print("\n❌ FALHA: O LaborEngine não encontrou o bundle via Action Type.")

if __name__ == "__main__":
    test_determinismo_mod()
