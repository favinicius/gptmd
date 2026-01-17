
import json
import uuid
import sys
from pathlib import Path
from typing import List, Dict, Any

DB_MOD_PATH = Path("data/db_mod.json")
LOG_PATH = Path("data/discoveries_log.json")

def load_json(path: Path) -> Any:
    if not path.exists(): return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path: Path, data: Any):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def approve_discovery(index: int):
    # Load data
    log_data = load_json(LOG_PATH)
    db_data = load_json(DB_MOD_PATH)
    
    if index < 0 or index >= len(log_data):
        print(f"[!] Índice invalido: {index}")
        return

    entry = log_data[index]
    if entry.get("status") == "approved":
        print("[!] Item já aprovado.")
        return

    print(f"[*] Aprovando: {entry['trigger_term']}")
    
    # 1. Create Bundle Logic
    new_bundle = {
        "trigger_keyword": entry["trigger_term"],
        "required_activities": []
    }
    
    # 2. Add Activities to Library and Link to Bundle
    for item in entry["suggested_wbs"]:
        # Generate a unique ID if it conflicts, or use provided
        # But usually we want stable IDs. Let's make a hash or increment
        # Simple strategy: Use ID from log but prefix if needed? 
        # Actually, let's just append header ID
        
        # Check if ID exists in DB
        existing_ids = {a["id"] for a in db_data["activity_library"]}
        new_id = item["id"]
        
        if new_id in existing_ids:
            # Generate new random ID
            new_id = f"RES_{uuid.uuid4().hex[:6].upper()}"
        
        # Add to Library
        new_activity = {
            "id": new_id,
            "category": item["category"],
            "name": item["name"],
            "description": item.get("description", "Importado via Research Engine"),
            "role": item["role"],
            "setup_hours": item.get("setup_hours", 0.0),
            "unit_hours": item.get("unit_hours", 1.0),
            "unit_measure": "unidade",
            "tags": ["research_import"]
        }
        
        db_data["activity_library"].append(new_activity)
        new_bundle["required_activities"].append(new_id)
        
    # 3. Add Bundle
    db_data["bundle_logic"].append(new_bundle)
    
    # 4. Save DB
    save_json(DB_MOD_PATH, db_data)
    
    # 5. Update Log
    entry["status"] = "approved"
    entry["approved_at"] = "now"
    save_json(LOG_PATH, log_data)
    
    print(f"[OK] Bundle '{entry['trigger_term']}' integrado ao db_mod.json com sucesso!")

def list_discoveries():
    data = load_json(LOG_PATH)
    print(f"\n--- Descobertas Pendentes ({len(data)}) ---")
    for i, entry in enumerate(data):
        status = entry.get("status", "unknown")
        marker = "✅" if status == "approved" else "⏳"
        print(f"[{i}] {marker} {entry['trigger_term']} ({len(entry.get('suggested_wbs', []))} items)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        list_discoveries()
        print("\nUso: python review_discoveries.py [list | approve <ID>]")
    else:
        cmd = sys.argv[1]
        if cmd == "list":
            list_discoveries()
        elif cmd == "approve" and len(sys.argv) > 2:
            try:
                approve_discovery(int(sys.argv[2]))
            except ValueError:
                print("ID deve ser um número inteiro.")
