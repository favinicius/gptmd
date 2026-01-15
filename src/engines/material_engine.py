from typing import List, Dict, Optional
from src.models import (
    Intent, ProposalData, CalculatedHardware, CalculatedService, CalculatedExpense
)
from src.database import Database

MISC_PCT = 0.10

class MaterialEngine:
    def __init__(self, database: Database):
        self.db = database

    def calculate_materials(self, intent: Intent, proposal: ProposalData):
        """
        Calcula Tabela de Materiais (Hardware)
        """
        for scope_item in intent.scope_items:
            hw_match = self.db.get_hardware(scope_item.name)
            if hw_match:
                qty = scope_item.detected_quantity
                unit_price = hw_match.cost_net if hw_match.cost_net else hw_match.cost_list
                proposal.hardware_table.append(CalculatedHardware(
                    description=hw_match.description_base,
                    partnumber=hw_match.partnumber,
                    qty=qty,
                    unit_price=unit_price,
                    total_price=unit_price * qty
                ))
        
        # Miscelâneas
        total_mat = sum(h.total_price for h in proposal.hardware_table)
        if total_mat > 0:
            misc_cost = total_mat * MISC_PCT
            proposal.hardware_table.append(CalculatedHardware(
                description="Miscelâneas (Materiais de Instalação)",
                partnumber="MISC-MAT",
                qty=1,
                unit_price=misc_cost,
                total_price=misc_cost,
                is_misc=True
            ))
        
        # Supply Only Logic (Zero Costs if Client Supplies)
        if intent.hardware_supply_by_client:
            for hw in proposal.hardware_table:
                hw.unit_price = 0.0
                hw.total_price = 0.0

        proposal.total_hardware = sum(h.total_price for h in proposal.hardware_table)

    def calculate_services(self, proposal: ProposalData, requires_certification: bool):
        """
        Calcula Serviços de Terceiros (SET)
        """
        if requires_certification:
            cert_items = [s for s in self.db.services if "Certificador" in s.description]
            for c in cert_items:
                proposal.service_table.append(CalculatedService(
                    description=c.description, qty=1, unit_price=c.cost_unit, total_price=c.cost_unit
                ))
            proposal.expense_table.append(CalculatedExpense(
                topic="T-00", # Usually generic expense
                description="Logística Reversa (Instrumentação)", qty=1, unit_price=450.0, total_price=450.0
            ))
        proposal.total_services = sum(i.total_price for i in proposal.service_table)
