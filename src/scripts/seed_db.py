import json
import sys
from pathlib import Path
from sqlmodel import Session, select

# Adjust path to include src
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.database.config import create_db_and_tables, engine
from src.database.models import HardwareTable, LaborRoleTable, ActivityTable, LogisticsItemTable, SettingsTable

DATA_DIR = Path(__file__).parent.parent.parent / "data"

def load_hardware(session: Session):
    print("Loading Hardware...")
    try:
        with open(DATA_DIR / "db_mat.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            count = 0
            for item in data:
                # Check for duplications based on unique constraint (optional) or just simple logic
                # Here we just insert. Ideally check ID or PartNumber.
                # Assuming empty DB for initial seed.
                hw = HardwareTable(**item)
                session.add(hw)
                count += 1
            print(f"  - Loaded {count} hardware items.")
    except Exception as e:
        print(f"  ! Error loading hardware: {e}")

def load_labor(session: Session):
    print("Loading Labor & Activities...")
    try:
        with open(DATA_DIR / "db_mod.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            
            # Roles
            roles = data.get("roles", [])
            count_roles = 0
            for r in roles:
                role_entry = LaborRoleTable(**r)
                session.add(role_entry)
                count_roles += 1
            print(f"  - Loaded {count_roles} roles.")

            # Activities
            activities = data.get("activity_library", [])
            count_activities = 0
            for a in activities:
                # Convert tags list to JSON compatible format if needed (SQLModel handles List[str] with sa_type=JSON often if supported by dialect, SQLite logic needed)
                # Actually, in models.py we set sa_type=JSON.
                act = ActivityTable(**a)
                session.add(act)
                count_activities += 1
            print(f"  - Loaded {count_activities} activities.")
            
    except Exception as e:
        print(f"  ! Error loading labor: {e}")

def load_logistics(session: Session):
    print("Loading Logistics (DIV)...")
    try:
        with open(DATA_DIR / "db_div.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            
            # Policies -> SettingsTable
            policies = data.get("policies", {})
            for k, v in policies.items():
                setting = SettingsTable(key=f"policy_{k}", value=str(v), description="Logistics Policy")
                session.add(setting)
            print(f"  - Loaded {len(policies)} policies.")

            # Logistics Bundles -> LogisticsItemTable
            bundles = data.get("logistics_bundles", {})
            for k, v in bundles.items():
                # v is dict {desc, est_cost}
                item = LogisticsItemTable(
                    category="logistics_bundle",
                    item_key=k,
                    description=v.get("desc"),
                    cost_value=v.get("est_cost"),
                    unit="bundle"
                )
                session.add(item)
            print(f"  - Loaded {len(bundles)} logistics bundles.")

    except Exception as e:
        print(f"  ! Error loading logistics: {e}")

def main():
    print("Initializing Database...")
    create_db_and_tables()
    
    with Session(engine) as session:
        # Check if DB is already populated to avoid duplication if running multiple times
        # For now, simplistic approach: check if hardware table has rows
        existing_hw = session.exec(select(HardwareTable)).first()
        if existing_hw:
            print("Database seems already populated. Skipping seed. (Run with --force to overwrite NOT IMPLEMENTED YET)")
            return

        load_hardware(session)
        load_labor(session)
        load_logistics(session)
        
        session.commit()
    print("Database seeding completed.")

if __name__ == "__main__":
    main()
