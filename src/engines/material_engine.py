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
        aggregation = {} # {partnumber: CalculatedHardware}

        for scope_item in intent.scope_items:
            # Pular itens que não envolvem fornecimento de hardware físico (ex: migração de carga ou criação de VMs)
            if scope_item.action_type in ["migration", "design", "consulting", "infra_vm", "heavy_app_vm", "db_vm", "vdi_vm", "other"]:
                continue

            matches = []
            
            hw_direct = self.db.get_hardware(scope_item.name)
            if hw_direct:
                matches.append(hw_direct)
            else:
                # Search for multiple keywords in name + note
                search_text = (scope_item.name + " " + (scope_item.context_note or "")).lower()
                
                # Check for multiple categories
                found_categories = []
                if ("servidor" in search_text or "host" in search_text) and "server" not in found_categories:
                    m = self.db.get_hardware("DL380-G11") # Specific PN for fallback
                    if m: matches.append(m); found_categories.append("server")
                if "switch" in search_text and "switch" not in found_categories:
                    m = self.db.get_hardware("Switch") # Category keyword match
                    if m: matches.append(m); found_categories.append("switch")
                if "storage" in search_text and "storage" not in found_categories:
                    m = self.db.get_hardware("MSA-2060") # PN de storage no DB
                    if m: matches.append(m); found_categories.append("storage")
                if "rack" in search_text and "rack" not in found_categories:
                    m = self.db.get_hardware("GEN-RACK-44U") # Specific PN for fallback
                    if m: matches.append(m); found_categories.append("rack")
                if ("no-break" in search_text or "ups" in search_text) and "ups" not in found_categories:
                    m = self.db.get_hardware("GEN-UPS-3KVA") # Specific PN for fallback
                    if m: matches.append(m); found_categories.append("ups")
                if ("appliance" in search_text or "monitoramento" in search_text) and "monitoring" not in found_categories:
                    m = self.db.get_hardware("GEN-MON-APP") # Specific PN for fallback
                    if m: matches.append(m); found_categories.append("monitoring")

            for hw_match in matches:
                qty = scope_item.detected_quantity
                pn = hw_match.partnumber
                unit_price = hw_match.cost_net if hw_match.cost_net else hw_match.cost_list
                
                if pn in aggregation:
                    aggregation[pn].qty += qty
                    aggregation[pn].total_price = aggregation[pn].qty * aggregation[pn].unit_price
                else:
                    aggregation[pn] = CalculatedHardware(
                        description=hw_match.description_base,
                        partnumber=pn,
                        qty=qty,
                        unit_price=unit_price,
                        total_price=unit_price * qty
                    )
        
        # Converte agregação para a tabela final
        proposal.hardware_table = list(aggregation.values())
        
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

    def calculate_services(self, proposal: ProposalData, intent: Intent, requires_certification: bool):
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
            
        # Add Training Course Cost (v2.6)
        if intent.requires_training:
             proposal.service_table.append(CalculatedService(
                description="Investimento em Capacitação Técnica Hyper-V", 
                qty=1, 
                unit_price=1000.00, 
                total_price=1000.00
            ))
        proposal.total_services = sum(i.total_price for i in proposal.service_table)
