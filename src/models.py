from typing import List, Optional, Literal, Dict
from pydantic import BaseModel, Field

# --- Database Models ---

class HardwareItem(BaseModel):
    category: str
    type: str
    description_base: str
    description_detail: str
    option_code: str
    vendor: str
    partnumber: str
    url: str
    cost_list: float
    cost_net: Optional[float] = None
    ipi_rate: float

class LaborRole(BaseModel):
    role: str
    cost_unit: float

class ActivityLibraryItem(BaseModel):
    id: str
    category: str
    name: str
    description: str
    role: str
    setup_hours: float
    unit_hours: float
    unit_measure: str
    tags: List[str]

class BundleLogic(BaseModel):
    trigger_keyword: str
    required_activities: List[str] # Lista de IDs em ActivityLibraryItem

class LaborDB(BaseModel):
    roles: List[LaborRole]
    activity_library: List[ActivityLibraryItem]
    bundle_logic: List[BundleLogic] = Field(default_factory=list)

class ServiceItem(BaseModel):
    category: str
    description: str
    details: str
    vendor: str
    unit: str
    cost_unit: float
    requires_logistics: bool

class LogisticsItem(BaseModel):
    item: str
    city_ref: str
    type: Optional[str] = None
    vendor: str
    details: str
    unit: str
    cost_unit: float

class LogisticsPolicies(BaseModel):
    meal_weekday: float
    meal_weekend_holiday: float
    hotel_tier_capital: float
    hotel_tier_interior: float
    km_reimbursement: float
    car_rental_suv: float
    fuel_avg_price: float
    fuel_efficiency_km_l: float

class LogisticsBundleItem(BaseModel):
    desc: str
    est_cost: float

class LogisticsDB(BaseModel):
    policies: LogisticsPolicies
    logistics_bundles: Dict[str, LogisticsBundleItem]


# --- Proposal Logic Models ---

class LogisticsPlan(BaseModel):
    requires_flight: bool = False
    flight_region: Optional[str] = None # 'flight_ne' or 'flight_s_se'
    requires_car_rental: bool = False
    estimated_daily_km: float = 0.0
    requires_freight: bool = False
    hotel_tier: Literal["hotel_tier_capital", "hotel_tier_interior"] = "hotel_tier_interior"
    origin_mobilization_km: float = 0.0 # New field for initial mobilization

class LogisticsOverride(BaseModel):
    transport_provider: Literal["client", "provider"] = "provider"
    consulting: bool = False
    travel_segments: List[int] = Field(default_factory=list) # Array de dias, ex: [5, 5, 5, 5, 15]
    team_size: int = 1
    stay_duration_days: List[int] = Field(default_factory=list)


class TopicMapping(BaseModel):
    topic_id: str
    description: str

class ScopeItem(BaseModel):
    name: str
    detected_quantity: int = 1
    action_type: Literal["install", "migrate_p2v", "supply_only", "turnkey", "design"]
    context_note: str
    visibility: Literal["public", "internal"] = "public" # New field
    explicit_total_hours: int = 0 # New field for overrides
    is_weekend: bool = False # New field for weekend work factor

class Intent(BaseModel):
    client_name: str
    company_name: str
    project_name: str
    scope_items: List[ScopeItem]
    hardware_supply_by_client: bool = False
    logistics_override: LogisticsOverride
    detailed_logistics: Optional[LogisticsPlan] = None
    estimated_duration_weeks: int = 1
    governance_level: Literal["standard", "intensive"] = "standard"
    work_on_weekends: bool = False



# --- Calculated Result Models ---

class CalculatedHardware(BaseModel):
    description: str
    partnumber: str
    qty: int
    unit_price: float
    total_price: float
    is_misc: bool = False

class CalculatedLabor(BaseModel):
    item_id: int
    topic: str
    role: str
    activity: str
    qty_professionals: int
    daily_hours: float = 8.0
    days: float
    hours: float
    hourly_rate: float
    total_price: float
    activity_type: str
    is_contingency: bool = False
    complexity: str # To track origin
    source_ref: str = "DB_STD" # DB_STD, DB_CALC, ESTIMATE, EXPLICIT

class CalculatedService(BaseModel):
    description: str
    qty: int
    unit_price: float
    total_price: float

class CalculatedExpense(BaseModel):
    topic: str = "T-00"
    description: str
    qty: int
    unit_price: float
    total_price: float

class ProposalData(BaseModel):
    hardware_table: List[CalculatedHardware] = Field(default_factory=list)
    labor_table: List[CalculatedLabor] = Field(default_factory=list)
    service_table: List[CalculatedService] = Field(default_factory=list)
    expense_table: List[CalculatedExpense] = Field(default_factory=list)
    topics: List[TopicMapping] = Field(default_factory=list)
    
    total_hardware: float = 0.0
    total_labor: float = 0.0
    total_services: float = 0.0
    total_expenses: float = 0.0
    grand_total: float = 0.0
