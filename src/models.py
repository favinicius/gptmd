from typing import List, Optional, Literal, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field

def format_br_number(value: float, decimal_places: int = 2) -> str:
    """Formata um float para o padrão brasileiro: 1.234,56"""
    if value is None: return "0"
    # Se for um inteiro puro, não precisa de casas decimais a menos que forçado
    if value == int(value) and decimal_places == 0:
        return f"{int(value):,}".replace(",", ".")
    
    formatted = f"{value:,.{decimal_places}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return formatted

def format_br_currency(value: float) -> str:
    """Formata um float para o padrão brasileiro com 2 casas: 1.234,56"""
    return format_br_number(value, 2)

def format_excel_number(value: float):
    """Regra: Se o número for um inteiro (ex: 8.0), remova o decimal (8). 
    Se for fracionado, mantenha 1 casa."""
    if value == int(value):
        return int(value)
    return round(value, 1)

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
    flight_cost_override: Optional[float] = None # Manual override for flight cost

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
    action_type: Literal["install", "migrate_p2v", "migration", "v2v_migration", "migrate_v2v", "supply_only", "turnkey", "design", "infra_vm", "heavy_app_vm", "db_vm", "vdi_vm", "training", "consulting", "logistics", "other"]
    summary_rational: Optional[str] = "" # Explicação simples (1-2 linhas) para o cliente
    context_note: Optional[str] = ""
    visibility: Literal["public", "internal"] = "public" # New field
    explicit_total_hours: Optional[int] = 0 # New field for overrides, defaulting to 0 if None
    is_weekend: Optional[bool] = False # New field for weekend work factor

class SizingMode(str, Enum):
    AGGRESSIVE = "aggressive"  # 0.85x
    STANDARD = "standard"      # 1.00x
    SECURE = "secure"          # 1.40x
    CRITICAL = "critical"      # 1.60x

class ContingencyLevel(str, Enum):
    NONE = "none"              # 0.0h
    LOW = "low"                # 1.0h/dia
    STANDARD = "standard"      # 1.5h/dia
    HIGH = "high"             # 2.0h/dia + 10% buff

class Intent(BaseModel):
    client_name: str
    company_name: str
    contact_name: Optional[str] = "Responsável Técnico" # Novo campo
    project_name: str
    project_motivation: Optional[str] = ""
    company_short_name: Optional[str] = "" 
    scope_items: List[ScopeItem]
    hardware_supply_by_client: bool = False
    # Governance Fields (v2.0)
    needs_clarification: bool = False
    clarification_questions: List[str] = Field(default_factory=list)
    confidence_score: float = 1.0
    logistics_override: Optional[LogisticsOverride] = None
    detailed_logistics: Optional[LogisticsPlan] = None
    estimated_duration_weeks: int = 1
    governance_level: Literal["standard", "intensive"] = "standard"
    work_on_weekends: bool = False
    requires_training: bool = False # Flag for training/course requirement
    
    # --- New Template Routing Fields (v5.0) ---
    selected_tech_template: str = "iodc_full.md"
    selected_comm_template: str = "capex_only.md"
    split_proposal: bool = False # If True, generate separate files

    # --- Sizing Thermometers (v6.0) ---
    sizing_mode: SizingMode = SizingMode.STANDARD
    contingency_level: ContingencyLevel = ContingencyLevel.STANDARD





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
    executions: float = 1.0 # Volume de itens (v7.2+)
    qty_professionals: int
    daily_hours: float = 8.0
    days: int
    hours: float
    hourly_rate: float
    total_price: float
    activity_type: str
    is_contingency: bool = False
    complexity: str # To track origin
    source_ref: str = "DB_STD" # DB_STD, DB_CALC, ESTIMATE, EXPLICIT
    technical_detail: Optional[str] = "" # Checklist/Observações técnicas (v9.2)

class CalculatedService(BaseModel):
    description: str
    qty: int
    unit_price: float
    total_price: float

class CalculatedExpense(BaseModel):
    topic: str = "T-00"
    description: str
    qty: Any
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
    
    # --- Commercial Selling Prices (v9.0) ---
    total_labor_venda: float = 0.0
    total_services_venda: float = 0.0
    total_expenses_venda: float = 0.0
    grand_total_venda: float = 0.0
    payment_term: int = 30
    
    grand_total: float = 0.0
    ai_research_count: int = 0
