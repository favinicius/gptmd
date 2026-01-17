from typing import List, Dict, Optional
import math
from src.models import (
    Intent, ProposalData, CalculatedExpense, format_br_currency, format_excel_number
)
from src.database import Database

class LogisticsEngine:
    def __init__(self, database: Database):
        self.db = database
        self.audit_log = []

    def get_audit_report(self) -> str:
        return "# AUDITORIA DE LOGÍSTICA v2.6\n\n" + "\n".join(self.audit_log)

    def calculate_logistics(self, intent: Intent, proposal: ProposalData):
        """
        Calcula as despesas de viagem (DIV) baseadas no plano da IA ou manual override.
        """
        self.audit_log = []
        plan = intent.detailed_logistics
        if not plan:
            self.audit_log.append("- [WARN] Nenhum plano logístico disponível.")
            return

        if not self.db.logistics_db:
            self.audit_log.append("- [ERROR] Database logístico não carregado.")
            return

        policies = self.db.logistics_db.policies
        bundles = self.db.logistics_db.logistics_bundles
        
        team_size = max(1, intent.logistics_override.team_size) if intent.logistics_override else 1
        
        segments = intent.logistics_override.travel_segments if (intent.logistics_override and intent.logistics_override.travel_segments) else []
        duration_days = sum(segments)
        
        # 0. Mobilização Terrestre Origem (v3.0)
        if plan.origin_mobilization_km > 0:
            mob_cost = (plan.origin_mobilization_km * policies.fuel_avg_price / policies.fuel_efficiency_km_l) + 200
            proposal.expense_table.append(CalculatedExpense(
                topic="LOG-00",
                description="Mobilização Terrestre Origem (Jundiaí - Aeroporto) - Ida/Volta",
                qty=1,
                unit_price=mob_cost,
                total_price=mob_cost
            ))

        # Loop pelos segmentos de viagem
        for i, segment_days in enumerate(segments):
            trip_label = f"Viagem {i+1:02d}"
            topic_id = f"LOG-{i+1:02d}"
            # 1. Aéreo
            if plan.requires_flight:
                # Se for Nordeste (OFI / Ilhéus), a regra é preço de venda fixo de 2500 (RT)
                # O custo base é lido do db_div.json. Se lá estiver 2500, e a margem de venda é 1.2:
                # Custo Unitário = (est_cost / 1.2) / 2 [para splitar IDA/VOLTA]
                
                region_key = plan.flight_region or "flight_ne"
                flight_bundle = bundles.get(region_key)
                flight_cost_ref = flight_bundle.est_cost if flight_bundle else 2500.00
                
                # Override manual se houver
                if plan.flight_cost_override and plan.flight_cost_override > 0:
                    flight_cost_ref = plan.flight_cost_override

                # Cálculo de custo unitário para que o total de venda seja flight_cost_ref
                # Venda_Total = Custo_Total * 1.2
                # Custo_Total = flight_cost_ref / 1.2
                # Custo_Unit (por perna) = (flight_cost_ref / 1.2) / 2
                
                one_way_cost = (flight_cost_ref / 1.2) / 2
                flight_desc_base = flight_bundle.desc if flight_bundle else "Passagem Aérea"
                
                if region_key == "flight_ne":
                    flight_desc_base += " [STRICT v4.0]"

                proposal.expense_table.append(CalculatedExpense(
                    topic=topic_id, description=f"[{trip_label}] {flight_desc_base} - IDA",
                    qty=format_excel_number(team_size), unit_price=one_way_cost, total_price=team_size * one_way_cost
                ))
                proposal.expense_table.append(CalculatedExpense(
                    topic=topic_id, description=f"[{trip_label}] {flight_desc_base} - VOLTA",
                    qty=format_excel_number(team_size), unit_price=one_way_cost, total_price=team_size * one_way_cost
                ))

            # 2. Hospedagem
            hotel_bundle = bundles.get(plan.hotel_tier)
            if hotel_bundle:
                proposal.expense_table.append(CalculatedExpense(
                    topic=topic_id, description=f"[{trip_label}] {hotel_bundle.desc}",
                    qty=format_excel_number(team_size * segment_days),
                    unit_price=hotel_bundle.est_cost, total_price=(team_size * segment_days) * hotel_bundle.est_cost
                ))

            # 3. Alimentação
            work_days = 5 
            weekend_days = 2
            if segment_days > 7:
                 work_days = (segment_days // 7) * 5 + min(5, segment_days % 7)
                 weekend_days = segment_days - work_days
            elif segment_days > 0:
                 work_days = segment_days
                 weekend_days = 0

            proposal.expense_table.append(CalculatedExpense(
                topic=topic_id, description=f"[{trip_label}] Alimentação (Dias Úteis)",
                qty=format_excel_number(team_size * work_days), unit_price=policies.meal_weekday,
                total_price=(team_size * work_days) * policies.meal_weekday
            ))
            if weekend_days > 0:
                proposal.expense_table.append(CalculatedExpense(
                    topic=topic_id, description=f"[{trip_label}] Alimentação (Finais de Semana)",
                    qty=format_excel_number(team_size * weekend_days), unit_price=policies.meal_weekend_holiday,
                    total_price=(team_size * weekend_days) * policies.meal_weekend_holiday
                ))

            # 4. Aluguel de Carro
            if plan.requires_car_rental:
                car_bundle = bundles.get("car_rental_suv")
                if car_bundle:
                    proposal.expense_table.append(CalculatedExpense(
                        topic=topic_id, description=f"[{trip_label}] {car_bundle.desc}",
                        qty=format_excel_number(segment_days), unit_price=car_bundle.est_cost,
                        total_price=segment_days * car_bundle.est_cost
                    ))
                
                # Combustível
                trip_km = plan.estimated_daily_km * segment_days
                total_km_clean = format_excel_number(trip_km)
                trip_liters = math.ceil(trip_km / policies.fuel_efficiency_km_l)
                
                proposal.expense_table.append(CalculatedExpense(
                    topic=topic_id,
                    description=f"[{trip_label}] Combustível ({total_km_clean} km)",
                    qty=format_excel_number(trip_liters),
                    unit_price=policies.fuel_avg_price,
                    total_price=trip_liters * policies.fuel_avg_price
                ))

        # 6. Frete
        if plan.requires_freight:
             freight_bundle = bundles.get("freight_heavy")
             if freight_bundle:
                proposal.expense_table.append(CalculatedExpense(
                    topic="LOG-00", description=freight_bundle.desc,
                    qty=1, unit_price=freight_bundle.est_cost, total_price=freight_bundle.est_cost
                ))

        proposal.total_expenses = sum(i.total_price for i in proposal.expense_table)
