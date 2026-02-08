from typing import List, Dict, Optional
import re
from src.models import (
    Intent, ProposalData, CalculatedHardware, CalculatedService, CalculatedExpense
)
from src.database import Database

# Configuração de Miscelâneas (v11.0 - Industrial)
MISC_PCT = 0.08 # Reduzido para 8% mas focado em itens de montagem

class MaterialEngine:
    def __init__(self, database: Database):
        self.db = database

    def calculate_materials(self, intent: Intent, proposal: ProposalData):
        """
        Calcula Tabela de Materiais (Hardware) - v11.0 Robust Mapping
        Foco: Determinismo e Anti-Alucinação.
        """
        aggregation = {} # {partnumber: CalculatedHardware}
        
        # Mapeamento Determinístico de Categorias (Fallback Robusto)
        # Se a IA identificar a categoria, usamos um item padrão do banco se o específico falhar.
        CATEGORY_FALLBACKS = {
            "SWITCH": "XC208G",      # Siemens XC208G como padrão industrial
            "SERVER": "DL380-G11",   # HPE DL380 como padrão de host
            "STORAGE": "MSA-2060",   # HPE MSA como padrão de storage
            "RACK": "GEN-RACK-44U",  # Rack 44U padrão
            "UPS": "GEN-UPS-3KVA",   # UPS 3KVA padrão
            "CABLING": "1403927",    # Phoenix Patch Cord CAT5e como fallback de cabling
            "FIREWALL": "MANUAL-FIREWALL", # Firewall requer cotação específica
            "BACKUP": "MANUAL-BACKUP",     # Backup (Fitas/Software) requer cotação
        }

        # 1. Processamento de Itens de Escopo
        for scope_item in intent.scope_items:
            # Pular itens puramente lógicos ou de serviço
            if scope_item.action_type in ["MIGRATION", "DESIGN", "CONSULTING", "VM", "TRAINING", "OTHER"]:
                continue

            qty = scope_item.detected_quantity
            item_name = scope_item.name
            context = (item_name + " " + (scope_item.context_note or "")).lower()

            hw_match = None
            
            # Estratégia de busca hierárquica (Determinismo)
            # A. Busca Exata por Part Number ou Option Code (Soberania)
            for item in self.db.hardware:
                # Part Number match (case insensitive)
                if item.partnumber and item.partnumber.lower() in context:
                    hw_match = item
                    break
                # Option Code match (Apenas se tiver conteúdo real, evita match por string vazia)
                if item.option_code and len(item.option_code) > 2 and item.option_code.lower() in context:
                    hw_match = item
                    break
            
            # B. Busca por Categoria (Action Type) se o item for genérico
            if not hw_match and scope_item.action_type in CATEGORY_FALLBACKS:
                hw_match = self.db.get_hardware(CATEGORY_FALLBACKS[scope_item.action_type])

            # C. Busca por Palavras-Chave de Categoria se B falhar
            if not hw_match:
                if "switch" in context:
                    hw_match = self.db.get_hardware("XC208G")
                elif "servidor" in context or "host" in context:
                    hw_match = self.db.get_hardware("DL380-G11")
                elif "storage" in context:
                    hw_match = self.db.get_hardware("MSA-2060")

            # D. Placeholder Anti-Alucinação (Cotação Manual)
            if not hw_match:
                # Se for hardware mas não mapeamos, criamos um item sem preço para cotação manual
                manual_pn = f"MANUAL-{re.sub(r'[^A-Z0-9]', '-', item_name.upper()[:10])}"
                aggregation[manual_pn] = CalculatedHardware(
                    description=f"[(!) COTAÇÃO MANUAL] {item_name}",
                    partnumber=manual_pn,
                    qty=qty,
                    unit_price=0.0,
                    total_price=0.0
                )
                continue

            # Registro do Item Mapeado
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

        # 2. Injeção de Itens Detectados pelo PDF (Inventário Explícito)
        # Se a IA detectou uma lista de hardware no PDF que não está no escopo de serviços, adicionamos aqui.
        for hw_spec in intent.detected_hardware_list:
            if hw_spec.part_number and hw_spec.part_number != "N/A":
                db_item = self.db.get_hardware(hw_spec.part_number)
                if db_item:
                    pn = db_item.partnumber
                    unit_price = db_item.cost_net if db_item.cost_net else db_item.cost_list
                    qty = hw_spec.quantity
                    
                    if pn in aggregation:
                        aggregation[pn].qty += qty
                        aggregation[pn].total_price = aggregation[pn].qty * aggregation[pn].unit_price
                    else:
                        aggregation[pn] = CalculatedHardware(
                            description=db_item.description_base,
                            partnumber=pn,
                            qty=qty,
                            unit_price=unit_price,
                            total_price=unit_price * qty
                        )

        # Converte agregação para a tabela final
        proposal.hardware_table = list(aggregation.values())
        
        # 3. Miscelâneas de Instalação (Proporcional ao Hardware Mapeado)
        total_mat = sum(h.total_price for h in proposal.hardware_table)
        if total_mat > 0:
            misc_cost = total_mat * MISC_PCT
            proposal.hardware_table.append(CalculatedHardware(
                description="Miscelâneas (Conectores, Identificadores e Fixadores)",
                partnumber="MISC-MAT",
                qty=1,
                unit_price=misc_cost,
                total_price=misc_cost,
                is_misc=True
            ))
        
        # Supply Only Logic (Se o cliente fornecer o hardware, o custo é zero para nós)
        if intent.hardware_supply_by_client:
            for hw in proposal.hardware_table:
                hw.unit_price = 0.0
                hw.total_price = 0.0

        proposal.total_hardware = sum(h.total_price for h in proposal.hardware_table)

    def calculate_services(self, proposal: ProposalData, intent: Intent, requires_certification: bool):
        """
        Calcula Serviços de Terceiros (SET) vinculados a infraestrutura física.
        """
        # Certificação de Rede (SET)
        if requires_certification:
            cert_items = [s for s in self.db.services if "Certificador" in s.description]
            for c in cert_items:
                proposal.service_table.append(CalculatedService(
                    description=c.description, qty=1, unit_price=c.cost_unit, total_price=c.cost_unit
                ))
            # Logística de instrumentação (DIV)
            proposal.expense_table.append(CalculatedExpense(
                topic="T-00", 
                description="Logística Reversa (Instrumentação)", qty=1, unit_price=450.0, total_price=450.0
            ))
            
        # Treinamento Operacional
        if intent.requires_training:
             proposal.service_table.append(CalculatedService(
                description="Investimento em Capacitação Técnica Operacional", 
                qty=1, 
                unit_price=1200.00, 
                total_price=1200.00
            ))
        
        proposal.total_services = sum(i.total_price for i in proposal.service_table)
