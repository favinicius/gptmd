from typing import List, Optional
from sqlmodel import Field, SQLModel, JSON

# --- Base Models ---

class HardwareTable(SQLModel, table=True):
    __tablename__ = "hardware_items"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    category: str
    type: str = "Reference"
    description_base: str
    description_detail: str
    option_code: Optional[str] = ""
    vendor: str
    partnumber: str
    url: Optional[str] = ""
    cost_list: float
    cost_net: float = 0.0
    ipi_rate: float = 0.0

class LaborRoleTable(SQLModel, table=True):
    __tablename__ = "labor_roles"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    role: str = Field(index=True, unique=True)
    cost_unit: float
    level: str = "mid" # entry, mid, senior, expert, management

class ActivityTable(SQLModel, table=True):
    __tablename__ = "activity_library"
    
    id: str = Field(primary_key=True) # Text based ID like 'PHYS_SW_01'
    category: str
    name: str
    description: str
    role: str
    setup_hours: float
    unit_hours: float
    unit_measure: str
    tags: List[str] = Field(default=[], sa_type=JSON) 

class LogisticsItemTable(SQLModel, table=True):
    __tablename__ = "logistics_items" # For DB_DIV generic items or others
    
    id: Optional[int] = Field(default=None, primary_key=True)
    category: str # 'logistics_bundle', 'expense', etc.
    item_key: str # 'flight_ne', 'meal_weekday'
    description: str
    cost_value: float
    unit: str = "unidade"
    details: Optional[str] = "" 

class SettingsTable(SQLModel, table=True):
    __tablename__ = "settings" # For global policies
    
    key: str = Field(primary_key=True)
    value: str # JSON encoded value or simple string
    description: Optional[str] = None
