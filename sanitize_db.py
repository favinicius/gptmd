import json
import os
from pathlib import Path

def sanitize_db():
    db_path = Path("data/db_mod.json")
    if not db_path.exists():
        print(f"Erro: {db_path} não encontrado.")
        return

    with open(db_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    project_keywords = [
        "design", "planejamento", "kick-off", "as-built", "lld", "hld", 
        "gestão de stakeholders", "documentação", "design lld", "levantamento",
        "projeto lógico", "projeto físico", "reunião formal", "databook",
        "transferência de conhecimento", "organização e etiquetas" # Este pode ser discutível, mas em cluster costuma ser global
    ]

    count = 0
    for activity in data.get("activity_library", []):
        name_lower = activity.get("name", "").lower()
        desc_lower = activity.get("description", "").lower()
        
        should_be_project = False
        for kw in project_keywords:
            if kw in name_lower or kw in desc_lower:
                should_be_project = True
                break
        
        # Casos específicos de IDs que sabemos serem globais
        if activity.get("id", "").startswith("PLAN_") or activity.get("id", "").startswith("VAL_002"):
            should_be_project = True

        if should_be_project and activity.get("unit_measure") != "projeto":
            print(f"[*] Ajustando: {activity.get('name')} -> projeto")
            activity["unit_measure"] = "projeto"
            count += 1

    if count > 0:
        with open(db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\nSucesso: {count} atividades saneadas no db_mod.json.")
    else:
        print("\nNenhuma atividade precisou de ajuste.")

if __name__ == "__main__":
    sanitize_db()
