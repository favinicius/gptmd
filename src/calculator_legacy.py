import math
import pandas as pd
from typing import List, Dict, Optional
from src.models import (
    Intent, ProposalData, CalculatedHardware, CalculatedLabor, 
    CalculatedService, CalculatedExpense, HardwareItem
)
from src.database import Database

# Constants
CONTINGENCY_PCT = 0.20
MISC_PCT = 0.10
BLOCK_ROUNDING = 2
MAX_DAILY_HOURS = 8

class PricingEngine:
    def __init__(self):
        self.db = Database()

    def _calculate_hours(self, base_hours: float) -> int:
        """
        Regra C: Arredondar para próximo par.
        """
        hours = math.ceil(base_hours)
        if hours % 2 != 0:
            hours += 1
        return hours

    def _add_contingency(self, hours: int) -> int:
        """
        Regra D: Contingência (20%, min 2h, even rounding).
        """
        if hours == 0:
            return 0
            
        contingency = math.ceil(hours * CONTINGENCY_PCT)
        if contingency < 2:
            contingency = 2
        
        if contingency % 2 != 0:
            contingency += 1
            
        return contingency

    def _get_role_cost(self, role: str) -> float:
        """Busca o custo unitário do papel no DB."""
        return self.db.get_role_cost(role)

    def _calculate_labor(self, intent: Intent, proposal: ProposalData, requires_certification: bool) -> str:
        """
        Refatorado (v2.1): Motor de Cálculo Semântico via Bundles Dinâmicos.
        Lê fórmulas e condições do db_mod.json.
        """
        # Heurística de Complexidade Global
        global_complexity = "Média"
        if any("core" in i.name.lower() for i in intent.scope_items) or requires_certification:
            global_complexity = "Alta"
            
        item_counter = 1
        team_size = max(1, intent.logistics_override.team_size)
        
        # 1. Governança e Gestão (T-00) - Transversal e Dinâmica
        item_counter = self._calculate_governance(intent, proposal, item_counter)

        # 2. Atividades por Item de Escopo (Lógica Dinâmica)
        for i, scope_item in enumerate(intent.scope_items):
            topic_id = f"T-{i+1:02d}"
            bundle = self.db.get_scope_bundle(scope_item.name)
            
            topic_physical_days = 0
            
            # REGRA V1.2 - LOGICA DE OVERRIDE
            if scope_item.explicit_total_hours > 0:
                # Cria uma única atividade representativa
                bundle_for_template = self.db.get_scope_bundle(scope_item.name)
                # Tenta pegar um template genérico do bundle ou fallback
                template_id_use = bundle_for_template.activities[0].template_id if bundle_for_template and bundle_for_template.activities else "act_rack_mount"
                template = self.db.get_activity_template(template_id_use)
                if not template: template = self.db.get_activity_template("act_rack_mount")
                
                role = template.default_role if template else "Consultor"
                role_cost = self._get_role_cost(role)
                
                effort_hours = scope_item.explicit_total_hours
                
                # Factor Weekend (V1.2) - +20%
                weekend_factor = 1.2 if scope_item.is_weekend else 1.0
                
                # Se for horas grandes, team_size divide o tempo de calendario, mas horas totais mantem
                days = math.ceil(effort_hours / (team_size * 8))
                allocated_hours = effort_hours # Total a pagar
                
                # Custo Total com Fator
                total_price = allocated_hours * role_cost * weekend_factor
                
                proposal.labor_table.append(CalculatedLabor(
                    item_id=item_counter,
                    topic=topic_id,
                    role=role,
                    activity=f"{scope_item.name} (Dec. Explícita: {scope_item.explicit_total_hours}h)",
                    qty_professionals=team_size,
                    daily_hours=8,
                    days=days,
                    hours=int(allocated_hours),
                    hourly_rate=role_cost,
                    total_price=total_price,
                    activity_type="Técnica (Manual)",
                    complexity=f"Manual {'(Fim de Semana)' if scope_item.is_weekend else ''}"
                ))
                item_counter += 1
                
                # Pula o processamento padrão do bundle
                continue

                if bundle:
                    for b_act in bundle.activities:
                        # Avaliação de Condição (Simplificada para action_type e Contexto de Item)
                        if b_act.condition:
                            eval_context = {
                                "action_type": scope_item.action_type,
                                "detected_quantity": scope_item.detected_quantity,
                                "scope_item_name": scope_item.name
                            }
                            try:
                                if not eval(b_act.condition, eval_context):
                                    continue
                            except Exception:
                                continue
                        
                        template = self.db.get_activity_template(b_act.template_id)
                        if not template: continue
                        
                        role = template.default_role
                        role_cost = self._get_role_cost(role)
                        
                        # REGRA DE OURO V2: Se per_unit > 0, multiplica. Se 0, usa fixo.
                        if b_act.per_unit_hours > 0:
                            effort_hours = b_act.per_unit_hours * scope_item.detected_quantity
                        else:
                            effort_hours = b_act.fixed_hours
                        
                        # Multiplicador Especial: Switch de Acesso (qtd > 2 -> dobrar esforço)
                        if b_act.template_id == "act_net_access_config" and scope_item.detected_quantity > 2:
                            effort_hours *= 2

                        # Multiplicador de Complexidade (Se item for 'core')
                        if "core" in scope_item.name.lower():
                            effort_hours *= 2
                            
                        # REGRA DE SEGURANÇA/IMPREVISTO (Safety Factor)
                        # Aplica 1.15x e arredonda para cima em Migração e Configuração
                        if any(t in ["migration", "config", "logic"] for t in template.tags):
                            effort_hours = math.ceil(effort_hours * 1.15)
                        
                        # Quantidade de profissionais baseada no tipo de atividade
                        qty_profs = team_size if any(tag in template.tags for tag in ["execution", "physical", "testing"]) else 1
                        
                        days = math.ceil(effort_hours / (qty_profs * 8))
                        allocated_hours = qty_profs * 8 * days
                        
                        # Acumula dias físicos para cálculo de SHE
                        if any(tag in ["execution", "physical", "infrastructure"] for tag in template.tags):
                            topic_physical_days += days
                        
                        # Weekend Factor V1.2
                        weekend_factor = 1.2 if scope_item.is_weekend else 1.0
                        total_price = allocated_hours * role_cost * weekend_factor
                        
                        proposal.labor_table.append(CalculatedLabor(
                            item_id=item_counter,
                            topic=topic_id,
                            role=role,
                            activity=f"{template.activity_name} ({scope_item.name})",
                            qty_professionals=qty_profs,
                            daily_hours=8,
                            days=days,
                            hours=int(allocated_hours),
                            hourly_rate=role_cost,
                            total_price=total_price,
                            activity_type=template.tags[0] if template.tags else "Técnica",
                            complexity=f"{global_complexity} (Safety Applied){' (Fim de Semana)' if scope_item.is_weekend else ''}"
                        ))
                        item_counter += 1
            
            else:
                # Fallback: Se não achar bundle, aplica esforço genérico de 8h
                template = self.db.get_activity_template("act_rack_mount") # Default to rack mount as physical fallback
                if template:
                    effort = 8 * scope_item.detected_quantity
                    days = math.ceil(effort / (team_size * 8))
                    allocated_hours = team_size * 8 * days
                    topic_physical_days += days 
                    
                    # Weekend Factor
                    weekend_factor = 1.2 if scope_item.is_weekend else 1.0
                    total_price = allocated_hours * self._get_role_cost(template.default_role) * weekend_factor
                    
                    proposal.labor_table.append(CalculatedLabor(
                        item_id=item_counter, topic=topic_id, role=template.default_role,
                        activity=f"{template.activity_name} (Genérico: {scope_item.name})",
                        qty_professionals=team_size, daily_hours=8, days=days,
                        hours=int(allocated_hours), hourly_rate=self._get_role_cost(template.default_role),
                        total_price=total_price,
                        activity_type="Execução", complexity=f"Fallback{' (Weekend)' if scope_item.is_weekend else ''}"
                    ))
                    item_counter += 1
            
            # REGRA DE SHE/ACESSO (Ineferência de Campo)
            if topic_physical_days > 0:
                she_template = self.db.get_activity_template("act_she_admission")
                if she_template:
                    # 1.5h por dia de visita estimado (topic_physical_days)
                    she_hours_total = math.ceil(topic_physical_days * 1.5)
                    she_days = math.ceil(she_hours_total / 8) # Normaliza em dias de 8h para a tabela, ou mantém horas quebradas?
                    # O template diz min_hours_day = 2. Vamos usar o calculado.
                    # Se for pouco (ex: 1.5h), arredonda para 2h ou 4h (meio período)? 
                    # Request diz: "Arredondado para 1 dia ou horas inteiras".
                    
                    # Vamos manter em horas inteiras.
                    she_allocated_hours = she_hours_total
                    
                    # Ajuste para caber em 'days' (para tabela)
                    # Se she_hours < 8, days=1, mas daily_hours = she_hours
                    effective_days = math.ceil(she_allocated_hours / 8)
                    
                    proposal.labor_table.append(CalculatedLabor(
                        item_id=item_counter,
                        topic=topic_id,
                        role=she_template.default_role,
                        activity=f"{she_template.activity_name} (Ineficiência: {topic_physical_days} dias)",
                        qty_professionals=team_size, # Equipe toda para para SHE
                        daily_hours=int(she_allocated_hours / effective_days) if effective_days > 0 else 2,
                        days=effective_days,
                        hours=int(she_allocated_hours * team_size), # Horas totais = horas * equipe
                        hourly_rate=self._get_role_cost(she_template.default_role),
                        total_price=(she_allocated_hours * team_size) * self._get_role_cost(she_template.default_role),
                        activity_type="Ineficiência/SHE",
                        complexity="Mandatório"
                    ))
                    item_counter += 1

        # 3. Documentação (T-00)
        doc_template = self.db.get_activity_template("act_doc")
        if doc_template:
            doc_cost = self._get_role_cost(doc_template.default_role)
            doc_hours = max(4, len(intent.scope_items) * 2)
            days = math.ceil(doc_hours / 8)
            allocated_hours = 8 * days
            proposal.labor_table.append(CalculatedLabor(
                item_id=item_counter, topic="T-00", role=doc_template.default_role,
                activity=doc_template.activity_name, qty_professionals=1,
                daily_hours=8, days=days, hours=int(allocated_hours),
                hourly_rate=doc_cost, total_price=allocated_hours * doc_cost,
                activity_type="Documentação", complexity=global_complexity
            ))
            item_counter += 1

        # 4. Supply Only Consulting (T-00)
        if intent.hardware_supply_by_client:
            total_tech_hours = sum(l.hours for l in proposal.labor_table if l.role in ["Técnico", "Auxiliar"])
            consulting_base = max(16, int(total_tech_hours * 0.10))
            days = math.ceil(consulting_base / 8)
            allocated_hours = 8 * days
            cost = self._get_role_cost("Engenheiro")
            proposal.labor_table.append(CalculatedLabor(
                item_id=item_counter, topic="T-00", role="Engenheiro",
                activity="Consultoria Técnica (Acompanhamento Supply)",
                qty_professionals=1, daily_hours=8, days=days,
                hours=int(allocated_hours), hourly_rate=cost,
                total_price=allocated_hours * cost, activity_type="Consultoria",
                complexity=global_complexity
            ))
            item_counter += 1

        proposal.total_labor = sum(i.total_price for i in proposal.labor_table)
        return "Calculated"


    def _calculate_governance(self, intent: Intent, proposal: ProposalData, item_counter: int) -> int:
        """
        Popula o tópico T-00 com atividades de governança baseadas na duração e nível.
        """
        duration_weeks = intent.estimated_duration_weeks
        level = intent.governance_level
        role_gestor = "Gestor"
        cost_gestor = self._get_role_cost(role_gestor)

        # 1. Kick-off (Fixo)
        template_kickoff = self.db.get_activity_template("act_gov_kickoff")
        if template_kickoff:
            proposal.labor_table.append(CalculatedLabor(
                item_id=item_counter, topic="T-00", role=role_gestor,
                activity=template_kickoff.activity_name, qty_professionals=1,
                daily_hours=template_kickoff.min_hours_day, days=1, 
                hours=template_kickoff.min_hours_day, hourly_rate=cost_gestor,
                total_price=template_kickoff.min_hours_day * cost_gestor,
                activity_type="Governança", complexity="Fixa"
            ))
            item_counter += 1

        # 2. Reunião Semanal (Recorrente)
        template_weekly = self.db.get_activity_template("act_gov_weekly")
        if template_weekly:
            total_hours = template_weekly.min_hours_day * duration_weeks
            proposal.labor_table.append(CalculatedLabor(
                item_id=item_counter, topic="T-00", role=role_gestor,
                activity=template_weekly.activity_name, qty_professionals=1,
                daily_hours=template_weekly.min_hours_day, days=duration_weeks,
                hours=int(total_hours), hourly_rate=cost_gestor,
                total_price=total_hours * cost_gestor,
                activity_type="Governança", complexity=f"Recorrente ({duration_weeks} sem)"
            ))
            item_counter += 1

        # 3. Dailies (Se Intensivo)
        if level == "intensive":
            template_daily = self.db.get_activity_template("act_gov_daily")
            if template_daily:
                total_days = duration_weeks * 5
                total_hours = template_daily.min_hours_day * total_days
                proposal.labor_table.append(CalculatedLabor(
                    item_id=item_counter, topic="T-00", role=role_gestor,
                    activity=template_daily.activity_name, qty_professionals=1,
                    daily_hours=template_daily.min_hours_day, days=total_days,
                    hours=int(total_hours), hourly_rate=cost_gestor,
                    total_price=total_hours * cost_gestor,
                    activity_type="Governança", complexity="Intensiva (Diária)"
                ))
                item_counter += 1

        # 4. Encerramento (Fixo)
        template_close = self.db.get_activity_template("act_gov_close")
        if template_close:
            proposal.labor_table.append(CalculatedLabor(
                item_id=item_counter, topic="T-00", role=role_gestor,
                activity=template_close.activity_name, qty_professionals=1,
                daily_hours=template_close.min_hours_day, days=1,
                hours=template_close.min_hours_day, hourly_rate=cost_gestor,
                total_price=template_close.min_hours_day * cost_gestor,
                activity_type="Governança", complexity="Fixa"
            ))
            item_counter += 1
        
        return item_counter

    def _calculate_services(self, proposal: ProposalData, requires_certification: bool):
        if requires_certification:
            cert_items = [s for s in self.db.services if "Certificador" in s.description]
            for c in cert_items:
                proposal.service_table.append(CalculatedService(
                    description=c.description, qty=1, unit_price=c.cost_unit, total_price=c.cost_unit
                ))
            proposal.expense_table.append(CalculatedExpense(
                description="Logística Reversa (Instrumentação)", qty=1, unit_price=450.0, total_price=450.0
            ))
        proposal.total_services = sum(i.total_price for i in proposal.service_table)

    def _calculate_logistics(self, intent: Intent, proposal: ProposalData):
        """
        Calcula despesas de logística baseadas no plano detalhado (LogisticsPlan)
        e nas políticas definidas em db_div.json.
        """
        override = intent.logistics_override
        plan = intent.detailed_logistics
        
        # Fallback se não houver plano (safety net)
        if not plan:
            # Tenta inferir básico
            from src.models import LogisticsPlan
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
            
            # --- 1. Aéreo (Trava de Custos do Banco de Dados) ---
            if plan.requires_flight:
                flight_bundle = bundles.get(plan.flight_region)
                if flight_bundle:
                    flight_cost_base = flight_bundle.est_cost
                    flight_desc_base = flight_bundle.desc
                else:
                    # Trava: se não encontrar, usa 0.00 e marca como A COTAR
                    flight_cost_base = 0.00
                    flight_desc_base = f"Passagem Aérea ({plan.flight_region}) - A COTAR"
                
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
                # Regra: Proporção 5:2 para viagens de 10 dias (8 úteis, 2 FDS)
                # Generalizando: A cada 7 dias, 5 úteis e 2 FDS.
                weeks = days_in_trip // 7
                extra_days = days_in_trip % 7
                
                # Assume-se que extra_days (1 a 6) primeiro preenche os dias úteis
                # Se days_in_trip = 10, weeks = 1 (5 úteis, 2 fds), extra = 3 (3 úteis). Total 8 úteis, 2 fds. Exatamente como pedido.
                fds_days = weeks * 2
                weekday_days = (weeks * 5) + extra_days
                
                qty_weekday = weekday_days * team_size
                qty_fds = fds_days * team_size
                
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

        # 6. Frete
        if plan.requires_freight:
            freight_bundle = bundles.get("freight_heavy")
            freight_cost = freight_bundle.est_cost if freight_bundle else 5000.00
            
            proposal.expense_table.append(CalculatedExpense(
                topic="LOG-00",
                description="Frete/Mobilização de Equipamentos",
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

    def _apply_multipliers(self, proposal: ProposalData):
        """
        Aplica as margens de venda (Regra J).
        """
        # Hardware (* 2)
        for hw in proposal.hardware_table:
            hw.unit_price = hw.unit_price * 2
            hw.total_price = hw.unit_price * hw.qty
        proposal.total_hardware = sum(h.total_price for h in proposal.hardware_table)
        
        # Labor (* 3)
        for lab in proposal.labor_table:
            # Mantém hourly_rate original (base) e aplica multiplier no total_price (que já inclui factors)
            lab.total_price = lab.total_price * 3.0
        proposal.total_labor = sum(l.total_price for l in proposal.labor_table)
        
        # Services (* 1.6)
        for serv in proposal.service_table:
            serv.unit_price = serv.unit_price * 1.6
            serv.total_price = serv.qty * serv.unit_price
        proposal.total_services = sum(s.total_price for s in proposal.service_table)
        
        # Expenses (* 1.2)
        for exp in proposal.expense_table:
            exp.unit_price = exp.unit_price * 1.2
            exp.total_price = exp.qty * exp.unit_price
        proposal.total_expenses = sum(e.total_price for e in proposal.expense_table)

    def calculate_proposal(self, intent: Intent) -> ProposalData:
        proposal = ProposalData()
        
        # 1. Identificar necessidades especiais
        requires_certification = any("fibra" in i.name.lower() or "cabeamento" in i.name.lower() for i in intent.scope_items)
        
        # 1b. Initialize Topics Mapping
        from src.models import TopicMapping
        for i, scope_item in enumerate(intent.scope_items):
            proposal.topics.append(TopicMapping(
                topic_id=f"T-{i+1:02d}",
                description=f"{scope_item.name} ({scope_item.detected_quantity} un - {scope_item.action_type})"
            ))
        
        # 2. Hardware (MAT)
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
        
        if intent.hardware_supply_by_client:
            for hw in proposal.hardware_table:
                # Mantemos registro mas zeramos para o total de venda
                hw.unit_price = 0.0
                hw.total_price = 0.0
        
        # 3. Labor (MOD)
        self._calculate_labor(intent, proposal, requires_certification)
        
        # 4. Services (SET)
        self._calculate_services(proposal, requires_certification)
        
        # 5. Logistics (DIV)
        self._calculate_logistics(intent, proposal)
        
        # 6. Margens e Totais
        self._apply_multipliers(proposal)
        
        proposal.grand_total = (
            proposal.total_hardware +
            proposal.total_labor +
            proposal.total_services +
            proposal.total_expenses
        )
        
        return proposal
