import math
from typing import List, Dict, Optional
from src.models import (
    Intent, ProposalData, CalculatedLabor, ProposalData
)
from src.database import Database

class LaborEngine:
    def __init__(self, database: Database):
        self.db = database
        self.item_counter = 1

    def _find_bundle_with_synonyms(self, item_name: str):
        """
        Busca por bundles usando sinônimos e keywords aprimoradas (v2.1).
        Ex: 'Planejamento' -> 'Project_Start'
        """
        item_name_lower = item_name.lower()
        synonyms = {
            "planejamento": "Project_Start",
            "projeto": "Project_Start",
            "encerramento": "Project_End",
            "finalização": "Project_End",
            "migração": "Migration",
            "migracao": "Migration",
            "servidor": "Server",
            "rede": "Rede",
            "switch": "Switch",
            "armazenamento": "Storage",
            "backup": "Backup",
            "virtualização": "Hyper-V",
            "virtualizacao": "Hyper-V",
            "hyper-v": "Hyper-V",
            "vmware": "Hyper-V" # Usando Hyper-V como bundle genérico de virtualização
        }
        
        # 1. Busca por sinônimos manuais
        for key, target in synonyms.items():
            if key in item_name_lower:
                bundle = self.db.get_scope_bundle(target)
                if bundle: return bundle
        
        # 2. Busca padrão no banco (substring match)
        return self.db.get_scope_bundle(item_name)

    def _get_role_cost(self, role: str) -> float:
        return self.db.get_role_cost(role)

    def _calculate_hours(self, hours: float) -> int:
        return math.ceil(hours)

    def _calculate_days(self, hours: float, team_size: int) -> int:
        return math.ceil(hours / (team_size * 8))

    def calculate_labor(self, intent: Intent, proposal: ProposalData, requires_certification: bool):
        """
        Calcula a tabela de Mão de Obra (MOD) com lógica de Bundle Explosion v2.0.
        """
        self.item_counter = 1
        
        # --- 1. Heurística de Complexidade e Multiplicadores (v2.0) ---
        complex_keywords = ["disaster recovery", "dr", "hyper-v", "brownfield", "migração", "migration", "nova tecnologia"]
        context_text = (intent.project_name + " " + " ".join([i.name for i in intent.scope_items])).lower()
        
        is_complex = any(kw in context_text for kw in complex_keywords)
        complexity_multiplier = 1.5 if is_complex else 1.0
        
        global_complexity = "Alta (Complexa)" if is_complex else "Média"
        if requires_certification:
            global_complexity = "Alta (Certificação)"
            
        team_size = max(1, intent.logistics_override.team_size)

        # 1. Governança e Planejamento Decomposto (T-00)
        self._calculate_governance(intent, proposal, team_size)
        
        # 2. Espelhamento de Logística (Viagem é Trabalho) - v2.0
        self._calculate_logistics_mirroring(intent, proposal)

        # 3. Atividades por Item de Escopo (Bundle Explosion)
        total_tech_hours = 0.0

        for i, scope_item in enumerate(intent.scope_items):
            topic_id = f"T-{i+1:02d}"
            
            # --- Melhoria do Matching (v2.1) ---
            bundle = self._find_bundle_with_synonyms(scope_item.name)
            
            if not bundle or not bundle.required_activities:
                self._create_fallback_activity(topic_id, scope_item, proposal, team_size, global_complexity, complexity_multiplier)
                continue

            # --- Lógica de Explosão v3.1 (WBS Rígido e Proporcional) ---
            topic_physical_days = 0 
            
            # 1. Primeiro cálculo para obter o esforço base total do bundle
            base_efforts = []
            total_bundle_base_hours = 0.0
            
            for act_id in bundle.required_activities:
                template = self.db.get_activity_template(act_id)
                if not template: continue
                
                # FÓRMULA v3.0: horas = setup + (unit_hours * Qtd)
                act_base_effort = template.setup_hours + (template.unit_hours * scope_item.detected_quantity)
                
                # Multiplicador de Complexidade v2.0
                if is_complex and any(tag in ["config", "logic", "migration", "virtualization", "network"] for tag in template.tags):
                    act_base_effort *= complexity_multiplier
                
                # Regras Legadas de Safety Factor (1.15x)
                if any(t in ["migration", "config", "logic"] for t in template.tags):
                    act_base_effort = math.ceil(act_base_effort * 1.15)
                
                # Forçar mínimo de 1h se a atividade existe no bundle (Fim das Linhas Genéricas)
                act_base_effort = max(1.0, act_base_effort)
                
                base_efforts.append((template, act_base_effort))
                total_bundle_base_hours += act_base_effort

            # 2. Cálculo do Fator de Distribuição se houver horas explícitas
            distribution_factor = 1.0
            if scope_item.explicit_total_hours > 0 and total_bundle_base_hours > 0:
                distribution_factor = scope_item.explicit_total_hours / total_bundle_base_hours

            # 3. Geração das linhas da MOD
            for template, act_base_effort in base_efforts:
                # Aplicar a distribuição proporcional
                act_effort = act_base_effort * distribution_factor
                
                # Regras de Fim de Semana (Global Factor)
                weekend_factor = 1.2 if scope_item.is_weekend else 1.0
                complexity_suffix = " (FDS)" if scope_item.is_weekend else ""
                
                role = template.role
                role_cost = self._get_role_cost(role)
                qty_profs = team_size if any(tag in template.tags for tag in ["execution", "physical", "testing"]) else 1
                
                days = self._calculate_days(act_effort, qty_profs)
                allocated_hours = round(act_effort)
                total_price = allocated_hours * role_cost * weekend_factor
                
                if any(tag in ["execution", "physical", "infrastructure"] for tag in template.tags):
                    topic_physical_days += days
                
                total_tech_hours += allocated_hours

                proposal.labor_table.append(CalculatedLabor(
                    item_id=self.item_counter,
                    topic=topic_id,
                    role=role,
                    activity=f"{template.name} ({scope_item.name})",
                    qty_professionals=qty_profs,
                    daily_hours=8,
                    days=days,
                    hours=allocated_hours,
                    hourly_rate=role_cost,
                    total_price=total_price,
                    activity_type=template.tags[0] if template.tags else "Técnica",
                    complexity=f"{global_complexity}{complexity_suffix}",
                    source_ref="DB_BUNDLE" if scope_item.explicit_total_hours == 0 else "EXPLICIT_DIST"
                ))
                self.item_counter += 1

            # Ineficiência de Campo
            if topic_physical_days > 0:
                self._calculate_she(topic_physical_days, topic_id, team_size, proposal)

        # 4. Itens Transversais Finais
        self._calculate_transversals(intent, proposal, global_complexity, total_tech_hours)

        proposal.total_labor = sum(i.total_price for i in proposal.labor_table)

    def _calculate_logistics_mirroring(self, intent: Intent, proposal: ProposalData):
        """
        Injeta horas de mobilização no MOD baseadas nas viagens.
        """
        segments = intent.logistics_override.travel_segments
        if not segments: return

        team_size = max(1, intent.logistics_override.team_size)
        role = "Engenheiro" # Aplicar a todos os envolvidos? Constituição diz 'Engineers + Analysts'
        role_analista = "Analista"
        
        cost_eng = self._get_role_cost(role)
        cost_ana = self._get_role_cost(role_analista)

        for i, days in enumerate(segments):
            trip_id = i + 1
            # Ida e Volta por viagem - v2.0: 5h por perna (sugestão do usuário)
            perna_hours = 5.0
            total_mob_hours = perna_hours * 2 # Ida + Volta
            
            # Adicionar para Engenheiro
            proposal.labor_table.append(CalculatedLabor(
                item_id=self.item_counter, topic="LOG-MOB", role=role,
                activity=f"Mobilização/Deslocamento Técnico Viagem {trip_id:02d} (Ida/Volta)",
                qty_professionals=1, daily_hours=perna_hours, days=2, hours=total_mob_hours,
                hourly_rate=cost_eng, total_price=total_mob_hours * cost_eng,
                activity_type="Logística", complexity="Transversal", source_ref="ESTIMATE"
            ))
            self.item_counter += 1

            # Adicionar para Analista (se equipe > 1)
            if team_size > 1:
                proposal.labor_table.append(CalculatedLabor(
                    item_id=self.item_counter, topic="LOG-MOB", role=role_analista,
                    activity=f"Mobilização/Deslocamento Técnico Viagem {trip_id:02d} (Ida/Volta)",
                    qty_professionals=team_size - 1, daily_hours=perna_hours, days=2, 
                    hours=total_mob_hours * (team_size - 1),
                    hourly_rate=cost_ana, total_price=total_mob_hours * (team_size - 1) * cost_ana,
                    activity_type="Logística", complexity="Transversal", source_ref="ESTIMATE"
                ))
                self.item_counter += 1

        proposal.total_labor = sum(i.total_price for i in proposal.labor_table)

    def _calculate_governance(self, intent: Intent, proposal: ProposalData, team_size: int):
        # T-00 Activities - Decomposição Mandatória v2.0
        duration_weeks = intent.estimated_duration_weeks
        role_gestor = "Gestor"
        role_arquiteto = "Arquiteto"
        cost_gestor = self._get_role_cost(role_gestor)
        cost_arq = self._get_role_cost(role_arquiteto)
        
        # 1. Kick-off e Levantamento de Requisitos
        proposal.labor_table.append(CalculatedLabor(
            item_id=self.item_counter, topic="T-00", role=role_gestor,
            activity="Kick-off e Levantamento de Requisitos", qty_professionals=1,
            daily_hours=8, days=1, hours=8,
            hourly_rate=cost_gestor, total_price=8*cost_gestor,
            activity_type="Governança", complexity="Fixa", source_ref="DB_CALC"
        ))
        self.item_counter += 1

        # 2. Definição de Hardware e Validação de BOM
        proposal.labor_table.append(CalculatedLabor(
            item_id=self.item_counter, topic="T-00", role=role_arquiteto,
            activity="Definição de Hardware e Validação de BOM", qty_professionals=1,
            daily_hours=4, days=1, hours=4,
            hourly_rate=cost_arq, total_price=4*cost_arq,
            activity_type="Planejamento", complexity="Fixa", source_ref="ESTIMATE"
        ))
        self.item_counter += 1

        # 3. Low-Level Design (LLD) e Plano de Trabalho (Planbook)
        lld_hours = 16 # Mínimo sugerido pela v2.0
        proposal.labor_table.append(CalculatedLabor(
            item_id=self.item_counter, topic="T-00", role=role_arquiteto,
            activity="Design de Baixível e Criação de Planbook (LLD)", qty_professionals=1,
            daily_hours=8, days=int(lld_hours/8), hours=lld_hours,
            hourly_rate=cost_arq, total_price=lld_hours*cost_arq,
            activity_type="Planejamento", complexity="Técnica", source_ref="DB_STD"
        ))
        self.item_counter += 1

        # 4. Reuniões de Aprovação Executiva
        proposal.labor_table.append(CalculatedLabor(
            item_id=self.item_counter, topic="T-00", role=role_gestor,
            activity="Reuniões de Aprovação Executiva e Stakeholders", qty_professionals=1,
            daily_hours=2, days=2, hours=4,
            hourly_rate=cost_gestor, total_price=4*cost_gestor,
            activity_type="Governança", complexity="Fixa", source_ref="ESTIMATE"
        ))
        self.item_counter += 1
            
        # 5. Acompanhamento Semanal (Recorrente)
        t_weekly = self.db.get_activity_template("act_gov_weekly")
        if t_weekly:
            total_hours = t_weekly.min_hours_day * duration_weeks
            proposal.labor_table.append(CalculatedLabor(
                item_id=self.item_counter, topic="T-00", role=role_gestor,
                activity=t_weekly.activity_name, qty_professionals=1,
                daily_hours=t_weekly.min_hours_day, days=duration_weeks, hours=int(total_hours),
                hourly_rate=cost_gestor, total_price=total_hours*cost_gestor,
                activity_type="Governança", complexity=f"Recorrente ({duration_weeks} sem)",
                source_ref="DB_CALC"
            ))
            self.item_counter += 1
            
        # 6. Dailies (Intensive only)
        if intent.governance_level == "intensive":
            t_daily = self.db.get_activity_template("act_gov_daily")
            if t_daily:
                total_days_gov = duration_weeks * 5
                total_hours = t_daily.min_hours_day * total_days_gov
                proposal.labor_table.append(CalculatedLabor(
                     item_id=self.item_counter, topic="T-00", role=role_gestor,
                    activity=t_daily.activity_name, qty_professionals=1,
                    daily_hours=t_daily.min_hours_day, days=total_days_gov, hours=int(total_hours),
                    hourly_rate=cost_gestor, total_price=total_hours*cost_gestor,
                    activity_type="Governança", complexity="Intensiva (Diária)",
                    source_ref="DB_CALC"
                ))
                self.item_counter += 1

        # 7. Encerramento
        t_close = self.db.get_activity_template("act_gov_close")
        if t_close:
             proposal.labor_table.append(CalculatedLabor(
                item_id=self.item_counter, topic="T-00", role=role_gestor,
                activity=t_close.activity_name, qty_professionals=1,
                daily_hours=t_close.min_hours_day, days=1, hours=t_close.min_hours_day,
                hourly_rate=cost_gestor, total_price=t_close.min_hours_day*cost_gestor,
                activity_type="Governança", complexity="Fixa",
                source_ref="DB_STD"
            ))
             self.item_counter += 1

    def _create_fallback_activity(self, topic_id, scope_item, proposal, team_size, global_complexity, multiplier):
        # Fallback genérico
        effort = 8 * scope_item.detected_quantity * multiplier
        if scope_item.explicit_total_hours > 0:
            effort = scope_item.explicit_total_hours
            
        role = "Técnico"
        cost = self._get_role_cost(role)
        days = math.ceil(effort / (team_size * 8))
        
        weekend_factor = 1.2 if scope_item.is_weekend else 1.0
        
        proposal.labor_table.append(CalculatedLabor(
            item_id=self.item_counter, topic=topic_id, role=role,
            activity=f"Execução Genérica ({scope_item.name})",
            qty_professionals=team_size, daily_hours=8, days=days, hours=int(effort),
            hourly_rate=cost, total_price=effort*cost*weekend_factor,
            activity_type="Execução", complexity=global_complexity, source_ref="ESTIMATE"
        ))
        self.item_counter += 1

    def _calculate_she(self, physical_days, topic_id, team_size, proposal):
        she_template = self.db.get_activity_template("act_she_admission")
        if not she_template: return
        
        # 1.5h per physical day (Legado) mantido como 'Admissão/Integração' por Tópico
        she_hours_total = math.ceil(physical_days * 1.5)
        days = math.ceil(she_hours_total / 8)
        
        cost = self._get_role_cost(she_template.default_role)
        
        proposal.labor_table.append(CalculatedLabor(
            item_id=self.item_counter, topic=topic_id, role=she_template.default_role,
            activity=f"{she_template.activity_name} (Integração Local)",
            qty_professionals=team_size, daily_hours=int(she_hours_total/days) if days else 2,
            days=days, hours=int(she_hours_total * team_size),
            hourly_rate=cost, total_price=(she_hours_total * team_size) * cost,
            activity_type="Ineficiência/SHE", complexity="Mandatório", source_ref="DB_CALC"
        ))
        self.item_counter += 1

    def _calculate_transversals(self, intent: Intent, proposal: ProposalData, global_complexity: str, total_tech_hours: float):
         # 1. Documentação
        doc_template = self.db.get_activity_template("act_doc")
        if doc_template:
            doc_hours = max(4, len(intent.scope_items) * 2)
            days = math.ceil(doc_hours/8)
            cost = self._get_role_cost(doc_template.default_role)
            proposal.labor_table.append(CalculatedLabor(
                 item_id=self.item_counter, topic="T-00", role=doc_template.default_role,
                 activity=doc_template.activity_name, qty_professionals=1,
                 daily_hours=8, days=days, hours=doc_hours, hourly_rate=cost,
                 total_price=doc_hours*cost, activity_type="Documentação", complexity=global_complexity,
                 source_ref="DB_CALC"
            ))
            self.item_counter += 1
            
        # 2. Ineficiência de Campo / SHE (Buffer 5-10% v2.0)
        # Aplicamos 7% como média do range solicitado
        buffer_hours = math.ceil(total_tech_hours * 0.07)
        if buffer_hours > 0:
            role_she = "Técnico"
            cost_she = self._get_role_cost(role_she)
            proposal.labor_table.append(CalculatedLabor(
                item_id=self.item_counter, topic="T-00", role=role_she,
                activity="Buffer de Ineficiência Operacional / SHE (Fator 7%)",
                qty_professionals=1, daily_hours=8, days=math.ceil(buffer_hours/8), hours=buffer_hours,
                hourly_rate=cost_she, total_price=buffer_hours * cost_she,
                activity_type="Ineficiência/SHE", complexity="Buffer", source_ref="EXPLICIT"
            ))
            self.item_counter += 1

        # 3. Consultoria de Compras (Acompanhamento Supply)
        if intent.hardware_supply_by_client:
            consulting_hours = max(16, int(total_tech_hours * 0.10))
            days = math.ceil(consulting_hours/8)
            cost = self._get_role_cost("Engenheiro")
            proposal.labor_table.append(CalculatedLabor(
                item_id=self.item_counter, topic="T-00", role="Engenheiro",
                activity="Consultoria Técnica (Acompanhamento Supply)",
                qty_professionals=1, daily_hours=8, days=days, hours=consulting_hours,
                hourly_rate=cost, total_price=consulting_hours*cost,
                activity_type="Consultoria", complexity=global_complexity,
                source_ref="DB_CALC"
            ))
            self.item_counter += 1
