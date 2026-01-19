import math
import collections
from typing import List, Dict, Optional
from src.models import (
    Intent, ProposalData, CalculatedLabor, format_excel_number, ScopeItem
)
from src.database import Database
from src.engines.research_engine import ResearchEngine

class LaborEngine:
    def __init__(self, database: Database, research_engine: Optional[ResearchEngine] = None):
        self.db = database
        self.research = research_engine
        self.item_counter = 1

    CONFIG_SIZING = {
        "aggressive": 0.85,
        "standard": 1.00,
        "secure": 1.25
    }

    CONFIG_CONTINGENCY = {
        "none": 0.0,
        "low": 0.10, 
        "standard": 0.15,
        "high": 0.20
    }

    def calculate_labor(self, intent: Intent, proposal: ProposalData, requires_certification: bool = False):
        """
        Calcula Tabela de Mão de Obra (MOD) - Versão v8.0 (Aprendizado e Consolidação)
        Fórmula: Execs * Qtde * Horas_Dia * Dias = Total_H
        Regra: VMs agora consolidadas por tipo.
        """
        self.item_counter = 1
        
        # Fatores
        s_mode = str(intent.sizing_mode.value) if hasattr(intent.sizing_mode, 'value') else intent.sizing_mode
        c_level = str(intent.contingency_level.value) if hasattr(intent.contingency_level, 'value') else intent.contingency_level
        sizing_factor = self.CONFIG_SIZING.get(s_mode, 1.0)
        she_factor = self.CONFIG_CONTINGENCY.get(c_level, 0.15)

        # 1. Mobilização
        self._calculate_logistics_mirroring(intent, proposal)
        
        # 2. Governança e Transverais
        self._calculate_governance(intent, proposal, sizing_factor)
        
        # 3. Escopo Técnico
        total_tech_hours = 0.0
        # Initialize ai_research_count for this calculation run if it's not already part of proposal
        # Assuming ProposalData already has ai_research_count, as it's incremented later.
        # If not, it should be initialized in ProposalData's __init__ or here.
        # proposal.ai_research_count = 0 # Uncomment if ProposalData doesn't initialize it.
        global_complexity = intent.logistics_override.consulting if intent.logistics_override else False
        complexity_multiplier = 1.3
        
        topic_tech_effort = collections.defaultdict(float)
        topic_team_size = {}

        vm_profiles = {
            "infra_vm": "VIRT_VM_INFRA",
            "heavy_app_vm": "VIRT_VM_HEAVY",
            "db_vm": "VIRT_VM_DB",
            "vdi_vm": "VIRT_VM_VDI"
        }

        for i, scope_item in enumerate(intent.scope_items):
            topic_id = f"T-{i+1:02d}"
            team_size = max(1, intent.logistics_override.team_size) if intent.logistics_override else 1
            is_complex = any(kw in scope_item.name.lower() or kw in scope_item.context_note.lower() 
                           for kw in ["migração", "crítico", "complexo", "cluster"])
            
            qty_items = scope_item.detected_quantity
            phase_groups = collections.defaultdict(list)

            # Lógica Especial para VMs (Consolidação v8.0)
            if scope_item.action_type in vm_profiles:
                # 1. Provisionamento Base
                base_tpl = self.db.get_activity_template("VIRT_003")
                if base_tpl:
                    eff = (base_tpl.setup_hours / qty_items if qty_items > 0 else 0) + base_tpl.unit_hours
                    eff *= sizing_factor
                    phase_groups[base_tpl.category].append({"template": base_tpl, "eff": eff})
                
                # 2. Configuração Específica do Perfil
                prof_tpl = self.db.get_activity_template(vm_profiles[scope_item.action_type])
                if prof_tpl:
                    eff = prof_tpl.unit_hours * sizing_factor
                    if is_complex: eff *= complexity_multiplier
                    phase_groups[prof_tpl.category].append({"template": prof_tpl, "eff": eff})
                
                # 3. Validação
                val_tpl = self.db.get_activity_template("VAL_001")
                if val_tpl:
                    eff = 1.0 * sizing_factor # Reduzido para 1h por unidade em VM
                    phase_groups[val_tpl.category].append({"template": val_tpl, "eff": eff})
            
            else:
                # Lógica de Bundle para Hardware/Outros
                bundle = self.db.get_scope_bundle(scope_item.name)
                if not bundle or not bundle.required_activities:
                    # Tenta Pesquisa se não houver Bundle (v8.0)
                    if self.research:
                        researched_wbs = self.research.estimate_unknown_activity(scope_item.name, scope_item.context_note)
                        if researched_wbs:
                            proposal.ai_research_count += 1
                            for res_act in researched_wbs:
                                eff = res_act["unit_hours"] * sizing_factor
                                if is_complex and res_act["role"] in ["Engenheiro", "Arquiteto"]:
                                    eff *= complexity_multiplier
                                
                                self._add_labor_line_from_raw_generic(
                                    proposal, topic_id, res_act["role"], res_act["name"],
                                    qty_items, team_size, eff, self.db.get_role_cost(res_act["role"]), res_act["category"],
                                    source_ref="AI_RESEARCH_V8"
                                )
                                act_total_h = eff * qty_items
                                topic_tech_effort[topic_id] += act_total_h
                                total_tech_hours += act_total_h
                            topic_team_size[topic_id] = team_size
                            continue

                    self._create_fallback_with_coalescence(topic_id, scope_item, proposal, team_size, sizing_factor)
                    continue

                for act_id in bundle.required_activities:
                    template = self.db.get_activity_template(act_id)
                    if not template: continue
                    
                    unit_eff = template.unit_hours
                    setup_part = template.setup_hours / qty_items if qty_items > 0 else 0
                    eff = unit_eff + setup_part
                    
                    if is_complex and any(tag in ["config", "logic", "migration", "virtualization", "network"] for tag in template.tags):
                        eff *= complexity_multiplier
                    if any(t in ["migration", "config", "logic"] for t in template.tags):
                        eff *= 1.15
                    
                    eff *= sizing_factor
                    phase_groups[template.category].append({"template": template, "eff": eff})

            # Processa e Consolida fases
            for category, acts in phase_groups.items():
                total_phase_unit_eff = sum(a["eff"] for a in acts)
                
                if len(acts) > 1:
                    main_names = [a["template"].name.split('(')[0].strip() for a in acts]
                    unique_names = []
                    for name in main_names:
                        if name not in unique_names: unique_names.append(name)
                    combined_name = " / ".join(unique_names)
                else:
                    combined_name = acts[0]["template"].name

                # Regra OFI: Mínimo 1h por bloco consolidado
                final_unit_eff = max(1.0, total_phase_unit_eff)
                main_role = acts[0]["template"].role
                
                self._add_labor_line_from_raw_generic(
                    proposal, topic_id, main_role, combined_name,
                    qty_items, team_size, final_unit_eff, self.db.get_role_cost(main_role), category
                )
                
                act_total_h = final_unit_eff * qty_items
                topic_tech_effort[topic_id] += act_total_h
                total_tech_hours += act_total_h
            
            topic_team_size[topic_id] = team_size

        # 4. SHE (Ineficiência)
        for topic_id, tech_effort in topic_tech_effort.items():
            team_size = topic_team_size.get(topic_id, 1)
            self._calculate_she(tech_effort, topic_id, team_size, proposal, she_factor)

        self._calculate_transversals(intent, proposal, global_complexity, sizing_factor)
        proposal.total_labor = sum(i.total_price for i in proposal.labor_table)

    def _add_labor_line_from_raw_generic(self, proposal, topic_id, role, activity, total_items, team_size, unit_effort, cost, category, is_contingency=False, source_ref=None):
        qty_profs = max(1, team_size)
        execs_per_prof = total_items / qty_profs
        
        if unit_effort > 8:
            dias = math.ceil(unit_effort / 8)
            h_dia = round(unit_effort / dias, 2)
        else:
            dias = 1
            h_dia = round(unit_effort, 2)
            
        total_h = round(execs_per_prof * qty_profs * h_dia * dias, 2)
        
        if source_ref is None:
            source_ref = "DB_MOD_V8" if "fallback" not in activity.lower() else "ESTIMATE_FALLBACK"

        proposal.labor_table.append(CalculatedLabor(
            item_id=self.item_counter, topic=topic_id, role=role,
            activity=activity,
            executions=round(execs_per_prof, 2),
            qty_professionals=qty_profs,
            daily_hours=h_dia,
            days=dias, 
            hours=total_h,
            hourly_rate=cost,
            total_price=total_h * cost,
            activity_type=category,
            is_contingency=is_contingency,
            complexity="V8.0 - Consolidated",
            source_ref=source_ref
        ))
        self.item_counter += 1

    def _calculate_logistics_mirroring(self, intent: Intent, proposal: ProposalData):
        if not intent.logistics_override or not intent.logistics_override.travel_segments: return
        team_size = max(1, intent.logistics_override.team_size)
        cost_eng = self.db.get_role_cost("Engenheiro")
        cost_ana = self.db.get_role_cost("Analista")
        
        for idx, _ in enumerate(intent.logistics_override.travel_segments):
            label = f"Mobilização Técnico Viagem {idx+1:02d}"
            self._add_labor_line_from_raw_generic(proposal, "LOG-MOB", "Engenheiro", label, 1, 1, 10.0, cost_eng, "Logística")
            if team_size > 1:
                self._add_labor_line_from_raw_generic(proposal, "LOG-MOB", "Analista", label, 1, team_size-1, 10.0, cost_ana, "Logística")

    def _calculate_governance(self, intent: Intent, proposal: ProposalData, sizing_factor: float = 1.0):
        c_gestor = self.db.get_role_cost("Gestor")
        c_arq = self.db.get_role_cost("Arquiteto")
        self._add_labor_line_from_raw_generic(proposal, "T-00", "Gestor", "Kick-off e Gestão de Stakeholders", 1, 1, 12.0 * sizing_factor, c_gestor, "Governança")
        self._add_labor_line_from_raw_generic(proposal, "T-00", "Arquiteto", "Planejamento Técnico e Design LLD", 1, 1, 20.0 * sizing_factor, c_arq, "Planejamento")

    def _calculate_transversals(self, intent: Intent, proposal: ProposalData, global_complexity: bool, sizing_factor: float = 1.0):
        if global_complexity:
             c_eng = self.db.get_role_cost("Engenheiro")
             self._add_labor_line_from_raw_generic(proposal, "T-00", "Engenheiro", "Consultoria Técnica (Acompanhamento)", 1, 1, 16.0 * sizing_factor, c_eng, "Consultoria")

    def _calculate_she(self, tech_effort, topic_id, team_size, proposal, she_factor: float = 0.15):
        if she_factor <= 0: return
        she_cost = self.db.get_role_cost("Técnico")
        she_total_unit = max(1.0, (tech_effort * she_factor))
        self._add_labor_line_from_raw_generic(proposal, topic_id, "Técnico", "Ineficiência SHE / Permissões", 1, team_size, she_total_unit, she_cost, "Ineficiência/SHE", is_contingency=True)

    def _create_fallback_with_coalescence(self, topic_id: str, scope_item: ScopeItem, proposal: ProposalData, team_size: int, sizing_factor: float):
        role = "Analista"
        cost = self.db.get_role_cost(role)
        unit_h = 16.0 * sizing_factor
        if (scope_item.explicit_total_hours or 0) > 0:
            unit_h = scope_item.explicit_total_hours / scope_item.detected_quantity
        self._add_labor_line_from_raw_generic(proposal, topic_id, role, f"Execução Técnica: {scope_item.name}", scope_item.detected_quantity, team_size, max(1.0, unit_h), cost, "Execução")
