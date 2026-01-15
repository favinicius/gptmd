import math
from typing import List, Dict, Optional
from src.models import (
    Intent, ProposalData, CalculatedExpense, LogisticsPlan
)
from src.database import Database

class LogisticsEngine:
    def __init__(self, database: Database):
        self.db = database

    def calculate_logistics(self, intent: Intent, proposal: ProposalData):
        """
        Calcula despesas de logística baseadas no plano detalhado (LogisticsPlan)
        e nas políticas definidas em db_div.json.
        """
        override = intent.logistics_override
        plan = intent.detailed_logistics
        
        # Fallback se não houver plano (safety net)
        if not plan:
            plan = LogisticsPlan(
                requires_flight=(override.transport_provider == "provider"), 
                flight_region="flight_s_se",
                requires_car_rental=True,
                estimated_daily_km=50,
                hotel_tier="hotel_tier_capital"
            )

        travel_segments = override.travel_segments
        if not travel_segments:
            travel_segments = [5] # Padrão
            
        team_size = override.team_size if override.team_size > 0 else 1
        
        # Acesso ao DB de Logística
        log_db = self.db.logistics_db
        if not log_db:
            return

        policies = log_db.policies
        bundles = log_db.logistics_bundles
        
        # Iterar sobre CADA VIAGEM (Segmento)
        for i, days_in_trip in enumerate(travel_segments):
            trip_id = i + 1
            topic_id = f"LOG-{trip_id:02d}"
            trip_label = f"Viagem {trip_id:02d}"
            
            # --- 1. Aéreo (Trava de Custos Rígida v2.1) ---
            if plan.requires_flight:
                region_key = plan.flight_region
                flight_bundle = bundles.get(region_key)
                
                if flight_bundle:
                    flight_cost_base = flight_bundle.est_cost
                    flight_desc_base = flight_bundle.desc
                else:
                    # Trava v2.1: Proibido sugerir preço. 
                    # Se a chave não existir ou for nula, o custo é 0.00 (A COTAR)
                    flight_cost_base = 0.00
                    flight_desc_base = f"Passagem Aérea ({region_key}) - NÃO LOCALIZADA NO DB"
                
                one_way_cost = flight_cost_base / 2
                
                # IDA
                proposal.expense_table.append(CalculatedExpense(
                    topic=topic_id,
                    description=f"[{trip_label}] {flight_desc_base} - IDA",
                    qty=team_size,
                    unit_price=one_way_cost,
                    total_price=team_size * one_way_cost
                ))
                
                # VOLTA
                proposal.expense_table.append(CalculatedExpense(
                    topic=topic_id,
                    description=f"[{trip_label}] {flight_desc_base} - VOLTA",
                    qty=team_size,
                    unit_price=one_way_cost,
                    total_price=team_size * one_way_cost
                ))
            
            # --- 2. Hospedagem ---
            hotel_price = policies.hotel_tier_capital if plan.hotel_tier == "hotel_tier_capital" else policies.hotel_tier_interior
            total_hotel_qty = days_in_trip * team_size
            
            proposal.expense_table.append(CalculatedExpense(
                topic=topic_id,
                description=f"[{trip_label}] Hospedagem ({plan.hotel_tier.replace('hotel_tier_', '')})",
                qty=total_hotel_qty,
                unit_price=hotel_price,
                total_price=total_hotel_qty * hotel_price
            ))
            
            # --- 3. Alimentação (Lógica de Dias Úteis vs. Finais de Semana) ---
            if not intent.work_on_weekends:
                # Regra: Todos os dias como meal_weekday
                qty_weekday = days_in_trip * team_size
                proposal.expense_table.append(CalculatedExpense(
                    topic=topic_id,
                    description=f"[{trip_label}] Alimentação (Dias Úteis)",
                    qty=qty_weekday,
                    unit_price=policies.meal_weekday,
                    total_price=qty_weekday * policies.meal_weekday
                ))
            else:
                # Regra: Proporção 5:2 para viagens longas
                # A cada 7 dias, 5 úteis e 2 FDS.
                weeks = days_in_trip // 7
                extra_days = days_in_trip % 7
                
                # Assume-se que extra_days primeiro preenche os dias úteis (até 5)
                # Se sobrar, vai para FDS?
                # Exemplo: 10 dias. 1 semana (5,2) + 3 dias. Total: 8 úteis, 2 FDS.
                # Exemplo: 13 dias. 1 semana (5,2) + 6 dias (5 úteis, 1 FDS). Total: 10 úteis, 3 FDS.
                
                extra_weekdays = min(extra_days, 5)
                extra_fds = max(0, extra_days - 5)
                
                total_weekdays = (weeks * 5) + extra_weekdays
                total_fds = (weeks * 2) + extra_fds
                
                qty_weekday = total_weekdays * team_size
                qty_fds = total_fds * team_size
                
                if qty_weekday > 0:
                    proposal.expense_table.append(CalculatedExpense(
                        topic=topic_id,
                        description=f"[{trip_label}] Alimentação (Dias Úteis)",
                        qty=qty_weekday,
                        unit_price=policies.meal_weekday,
                        total_price=qty_weekday * policies.meal_weekday
                    ))
                
                if qty_fds > 0:
                    proposal.expense_table.append(CalculatedExpense(
                        topic=topic_id,
                        description=f"[{trip_label}] Alimentação (Finais de Semana)",
                        qty=qty_fds,
                        unit_price=policies.meal_weekend_holiday,
                        total_price=qty_fds * policies.meal_weekend_holiday
                    ))
            
            # --- 4. Locação Veículo ---
            if plan.requires_car_rental:
                cars_qty = math.ceil(team_size / 3)
                rental_days = days_in_trip
                total_rental_units = rental_days * cars_qty
                
                proposal.expense_table.append(CalculatedExpense(
                    topic=topic_id,
                    description=f"[{trip_label}] Locação Veículo (SUV)",
                    qty=total_rental_units,
                    unit_price=policies.car_rental_suv,
                    total_price=total_rental_units * policies.car_rental_suv
                ))
                
                # --- 5. Combustível ---
                trip_km = days_in_trip * plan.estimated_daily_km * cars_qty
                trip_liters = math.ceil(trip_km / policies.fuel_efficiency_km_l)
                
                proposal.expense_table.append(CalculatedExpense(
                    topic=topic_id,
                    description=f"[{trip_label}] Combustível ({trip_km} km)",
                    qty=trip_liters,
                    unit_price=policies.fuel_avg_price,
                    total_price=trip_liters * policies.fuel_avg_price
                ))

        # 6. Frete (Transversal - Custo Sugerido v2.1)
        if plan.requires_freight:
            freight_bundle = bundles.get("freight_heavy")
            # Trava v2.1: Proibido fallback manual.
            freight_cost = freight_bundle.est_cost if freight_bundle else 0.00
            freight_desc = freight_bundle.desc if freight_bundle else "Frete/Mobilização (EQUIPAMENTO NÃO IDENTIFICADO) - A COTAR"
            
            proposal.expense_table.append(CalculatedExpense(
                topic="LOG-00",
                description=freight_desc,
                qty=1,
                unit_price=freight_cost,
                total_price=freight_cost
            ))
            
        # 7. Mobilização Inicial Terrestre (Jundiaí - Aeroporto) - V1.2
        if plan.origin_mobilization_km > 0:
            total_mob_km = plan.origin_mobilization_km * 2 # Ida e Volta
            mob_cost = total_mob_km * policies.km_reimbursement
            
            proposal.expense_table.append(CalculatedExpense(
                topic="LOG-00",
                description=f"Mobilização Terrestre Origem (Jundiaí - Aeroporto) - Ida/Volta",
                qty=1,
                unit_price=mob_cost,
                total_price=mob_cost
            ))
            
        proposal.total_expenses = sum(i.total_price for i in proposal.expense_table)
