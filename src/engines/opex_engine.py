import math
from typing import List, Dict
from src.models import ProposalData, OpexData, OpexItem, CalculatedHardware, ScopeItem

class OpexEngine:
    """
    Motor de Cálculo de Custos Recorrentes (OPEX) e Dimensionamento de Suporte (NOC).
    Baseado na tabela de referência EGE/OFI v2.0.
    """

    # Tabela de Preços Unitários Mensais
    PRICING_TABLE = {
        "server_storage": 250.00,
        "switches": 200.00,
        "vms": 150.00,
        "workstations": 100.00,  # Regra de Lote de 5
        "systems": 70.00,        # Regra de Lote de 5
        "others": 50.00          # Regra de Lote de 5
    }

    # Custos Fixos de Conectividade
    FIXED_COSTS = {
        "ege_appliance": 800.00,
        "starlink_antenna": 170.00,
        "backup_internet": 700.00 # Opcional
    }

    # Taxa Implícita para Venda de Hora de Suporte (Baseado em R$ 7.500 -> 50h)
    HOURLY_RATE_F2 = 150.00

    @staticmethod
    def _categorize_hardware(hw_list: List[CalculatedHardware]) -> Dict[str, int]:
        """Classifica o hardware detectado nas categorias de cobrança."""
        counts = {
            "server_storage": 0,
            "switches": 0,
            "others": 0
        }
        
        for item in hw_list:
            desc = item.description.lower()
            qty = item.qty
            
            if any(x in desc for x in ["server", "servidor", "storage", "nas", "san"]):
                counts["server_storage"] += qty
            elif any(x in desc for x in ["switch", "router", "firewall", "gateway"]):
                counts["switches"] += qty
            else:
                counts["others"] += qty
                
        return counts

    @staticmethod
    def _count_scope_items(scope_items: List[ScopeItem]) -> Dict[str, int]:
        """Conta itens abstratos do escopo (VMs, Serviços)."""
        counts = {
            "vms": 0,
            "workstations": 0,
            "systems": 0
        }

        for item in scope_items:
            qty = item.detected_quantity
            # VMs
            if item.action_type in ["infra_vm", "heavy_app_vm", "db_vm", "vdi_vm", "migrate_p2v", "v2v_migration"]:
                 counts["vms"] += qty
            # Outros (Ex: VDI pode ser workstation também, dependendo da interpretação, mas vamos segregar)
            
        return counts

    @staticmethod
    def calculate_opex(proposal: ProposalData, scope_items: List[ScopeItem], months: int = 12) -> OpexData:
        """Processa o inventário e gera os dados de OPEX."""
        
        opex_data = OpexData()
        opex_data.contract_duration_months = months

        # 1. Levantamento de Quantitativos
        hw_counts = OpexEngine._categorize_hardware(proposal.hardware_table)
        scope_counts = OpexEngine._count_scope_items(scope_items)

        # 2. Cálculo de Monitoramento (Itens Monitorados)
        
        # Servidores / Storage
        if hw_counts["server_storage"] > 0:
            qty = hw_counts["server_storage"]
            unit_price = OpexEngine.PRICING_TABLE["server_storage"]
            opex_data.items.append(OpexItem(
                item_name="Servidores / Storage Físico",
                quantity=qty,
                unit_price=unit_price,
                total_price=qty * unit_price,
                category="monitoring"
            ))

        # Switches / Rede
        if hw_counts["switches"] > 0:
            qty = hw_counts["switches"]
            unit_price = OpexEngine.PRICING_TABLE["switches"]
            opex_data.items.append(OpexItem(
                item_name="Ativos de Rede (Switches/Routers/FW)",
                quantity=qty,
                unit_price=unit_price,
                total_price=qty * unit_price,
                category="monitoring"
            ))

        # Máquinas Virtuais
        if scope_counts["vms"] > 0:
            qty = scope_counts["vms"]
            unit_price = OpexEngine.PRICING_TABLE["vms"]
            opex_data.items.append(OpexItem(
                item_name="Máquinas Virtuais / Workloads",
                quantity=qty,
                unit_price=unit_price,
                total_price=qty * unit_price,
                category="monitoring"
            ))

        # Workstations / Outros (Regra de Lote de 5)
        # Exemplo: Se houver detecção de PCs, aplicar math.ceil(qty/5) * 5
        # Por enquanto, assumindo 0 se não detectado explicitamente, mas a lógica estaria aqui.
        
        # 3. Cálculo de Infraestrutura de Conectividade (Fixos)
        
        # Appliance EGE RASA (Sempre incluso conforme regra)
        opex_data.items.append(OpexItem(
            item_name="Appliance EGE RASA (Monitoramento Local)",
            quantity=1,
            unit_price=OpexEngine.FIXED_COSTS["ege_appliance"],
            total_price=OpexEngine.FIXED_COSTS["ege_appliance"],
            category="connectivity"
        ))

        # Antena Starlink (Sempre incluso conforme regra da imagem, verificar se é opcional depois)
        # Assumindo incluso por padrão como "Link Backup" ou gestão dele
        opex_data.items.append(OpexItem(
            item_name="Gestão Link Starlink / Antena",
            quantity=1,
            unit_price=OpexEngine.FIXED_COSTS["starlink_antenna"],
            total_price=OpexEngine.FIXED_COSTS["starlink_antenna"],
            category="connectivity"
        ))
        
        # 4. Totalização
        for item in opex_data.items:
            if item.category == "monitoring":
                opex_data.total_monitoring_monthly += item.total_price
            elif item.category == "connectivity":
                opex_data.total_connectivity_monthly += item.total_price
        
        opex_data.grand_total_monthly = (opex_data.total_monitoring_monthly + 
                                         opex_data.total_connectivity_monthly)
        
        opex_data.contract_total_value = opex_data.grand_total_monthly * months

        # 5. Cálculo de Franquia de Horas
        # Regra: Total Mensal / Rate (150.00)
        if opex_data.grand_total_monthly > 0:
            raw_hours = opex_data.grand_total_monthly / OpexEngine.HOURLY_RATE_F2
            # Arredondar para o inteiro mais próximo (ou múltiplo de 5, usuário pediu entre 45-50h para 7.5k)
            # 7500 / 150 = 50. Casou perfeitamente.
            opex_data.support_hours_f2 = math.floor(raw_hours)
        
        return opex_data
