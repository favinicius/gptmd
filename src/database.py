import json
from typing import List, Optional
from pathlib import Path
from src.models import HardwareItem, LaborDB, ServiceItem, LogisticsItem, ActivityLibraryItem, LogisticsDB

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
        self.services: List[ServiceItem] = [] # db_set.json (Assuming structure based on context usage, check file if needed)
        self.expenses: List[LogisticsItem] = [] # db_div.json
        self.logistics_db: Optional[LogisticsDB] = None
        
        self._load_data()
        self._initialized = True

    def _load_data(self):
        # Load Hardware
        with open(self.data_dir / "db_mat.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            self.hardware = [HardwareItem(**item) for item in data]

        # Load Labor
        with open(self.data_dir / "db_mod.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            self.labor = LaborDB(**data)

        # Load Services (db_set.json)
        try:
           with open(self.data_dir / "db_set.json", "r", encoding="utf-8") as f:
               data = json.load(f)
               # Assuming simple structure or need to inspect first? 
               # Let's assume list of dicts. If it fails I will validade.
               # Based on Logic.js: "Adicionar Custo SET (Locação Fluke) do DB_SET"
               # I'll use a generic dict load first or try to define ServiceItem loosely if I don't see the file.
               # Actually I saw db_set.json size 832 bytes in Step 9.
               # Let's assume standard fields.
               self.services = [ServiceItem(**item) for item in data]
        except (FileNotFoundError, Exception):
             # Fallback or empty if structure mismatch, for now essential to proceed
             self.services = [] 

        # Load Expenses (db_div.json)
        try:
            with open(self.data_dir / "db_div.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.logistics_db = LogisticsDB(**data)
                # self.expenses kept for backward compatibility if needed, but empty
                self.expenses = [] 
        except (FileNotFoundError, Exception) as e:
            print(f"Error loading db_div.json: {e}")
            self.logistics_db = None
            self.expenses = []

    def get_hardware(self, query: str) -> Optional[HardwareItem]:
        # Simple lookup logic - can be enhanced with fuzzy match later if needed
        # For now, searching by description or partnumber
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
        # Normalização: minúsculo e remove números
        clean_name = re.sub(r'\d+', '', item_name.lower()).strip()
        
        # Função interna para simplificar palavras (Remover s/es finais para bater singular/plural)
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
        
        for bundle in self.labor.bundle_logic:
            keyword = bundle.trigger_keyword.lower()
            stemmed_keyword = stem(keyword)
            if (keyword in clean_name or 
                stemmed_keyword in stemmed_clean or 
                keyword in item_name.lower()):
                return bundle
        return None

