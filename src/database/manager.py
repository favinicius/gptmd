import json
from typing import List, Optional
from pathlib import Path
from sqlmodel import select, Session

from src.models import HardwareItem, LaborDB, ServiceItem, LogisticsItem, ActivityLibraryItem, LogisticsDB, LaborRole
from .config import engine
from .models import HardwareTable, LaborRoleTable, ActivityTable, LogisticsItemTable, SettingsTable

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self.data_dir = Path(__file__).parent.parent / "data"
        self.hardware: List[HardwareItem] = []
        self.labor: Optional[LaborDB] = None
        self.services: List[ServiceItem] = []
        self.expenses: List[LogisticsItem] = []
        self.logistics_db: Optional[LogisticsDB] = None
        
        self._load_data_from_db()
        self._initialized = True

    def _load_data_from_db(self):
        """Loads data from SQLite into memory for fast access (Caching Strategy)"""
        with Session(engine) as session:
            # 1. Hardware
            hw_rows = session.exec(select(HardwareTable)).all()
            self.hardware = [HardwareItem(**row.model_dump()) for row in hw_rows]

            # 2. Labor (Roles & Activities)
            role_rows = session.exec(select(LaborRoleTable)).all()
            roles = [LaborRole(**row.model_dump()) for row in role_rows]
            
            act_rows = session.exec(select(ActivityTable)).all()
            activities = [ActivityLibraryItem(**row.model_dump()) for row in act_rows]

            # Reconstruct LaborDB structure
            # Note: We miss 'bundle_logic' if not in DB. Assuming bundle_logic stays in JSON or added to DB later.
            # For now, let's load bundle_logic from legacy JSON to not break it, or check if we added a table.
            # We didn't add BundleLogicTable. Let's keep it hybrid: Logic from JSON, Data from DB.
            legacy_mod = self._load_legacy_json("db_mod.json")
            bundle_logic = legacy_mod.get("bundle_logic", []) if legacy_mod else []
            
            self.labor = LaborDB(
                meta_info=legacy_mod.get("meta_info", {}),
                roles=roles,
                activity_library=activities,
                bundle_logic=bundle_logic 
            )

            # 3. Logistics (DIV)
            log_rows = session.exec(select(LogisticsItemTable)).all()
            settings_rows = session.exec(select(SettingsTable)).all()
            
            # Map SettingsTable back to dict policies
            policies = {}
            for s in settings_rows:
                key = s.key.replace("policy_", "")
                # Try convert to float/int if possible
                try:
                    val = float(s.value)
                    if val.is_integer(): val = int(val)
                except:
                    val = s.value
                policies[key] = val
                
            # Map LogisticsItemTable to bundles dict (flight_ne: {desc, est_cost})
            bundles = {}
            expenses_list = []
            
            for item in log_rows:
                if item.category == "logistics_bundle":
                    bundles[item.item_key] = {
                        "desc": item.description,
                        "est_cost": item.cost_value
                    }
                else:
                    # Treat others as generic LogisticsItem if needed, or Expense
                    # Existing code expects 'expenses' list for 'db_div.json' items? 
                    # Actually models.py LogisticsDB has policies and logistics_bundles.
                    pass
            
            self.logistics_db = LogisticsDB(
                policies=policies,
                logistics_bundles=bundles
            )
            self.expenses = [] # keeping empty as in original code logic

    def _load_legacy_json(self, filename: str) -> dict:
        try:
            with open(self.data_dir / filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}

    def get_hardware(self, query: str) -> Optional[HardwareItem]:
        query = query.lower()
        for item in self.hardware:
            if query in item.description_base.lower() or query in item.partnumber.lower() or query in item.option_code.lower():
                return item
        return None

    def get_role_cost(self, role_name: str) -> float:
        if not self.labor: return 0.0
        for r in self.labor.roles:
            if r.role.lower() == role_name.lower():
                return r.cost_unit
        return 0.0

    def get_activity_template(self, name_or_id: str) -> Optional[ActivityLibraryItem]:
        if not self.labor: return None
        # Try ID match first
        for t in self.labor.activity_library:
            if t.id.lower() == name_or_id.lower():
                return t
        # Try name match
        for t in self.labor.activity_library:
            if t.name.lower() == name_or_id.lower():
                return t
        # Try tag match
        for t in self.labor.activity_library:
            if any(name_or_id.lower() in tag.lower() for tag in t.tags):
                return t
        return None

    def get_scope_bundle(self, item_name: str) -> Optional[any]:
        if not self.labor: return None
        import re
        clean_name = re.sub(r'\d+', '', item_name.lower()).strip()
        
        def stem(s):
            words = s.split()
            stemmed = []
            for w in words:
                if len(w) > 4:
                    if w.endswith('es'): w = w[:-2]
                    elif w.endswith('s'): w = w[:-1]
                stemmed.append(w)
            return " ".join(stemmed)

        stemmed_clean = stem(clean_name)
        
        # bundle_logic is list of Pydantic models (from LaborDB/models.py)
        # We need to ensure we are iterating correctly. 
        # In original code: self.labor.bundle_logic is list of BundleLogic
        
        for bundle in self.labor.bundle_logic:
            # bundle is BundleLogic object (pydantic)
            # If loaded from JSON dict via LaborDB, pydantic handles it.
            keyword = bundle.trigger_keyword.lower()
            stemmed_keyword = stem(keyword)
            if (keyword in clean_name or 
                stemmed_keyword in stemmed_clean or 
                keyword in item_name.lower()):
                return bundle
        return None
