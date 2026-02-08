import os
import json
import time
import re
from typing import List, Dict, Any
from datetime import datetime, timedelta
from pathlib import Path
from google import genai
from google.genai import errors
from dotenv import load_dotenv
from src.models import Intent, LogisticsPlan

load_dotenv()

# Usando o modelo mais recente conforme diretriz Section 5.
# Configuração de Modelos (v3.0 - Resiliência)
# Configuração de Modelos (v3.1 - Benchmark Optim-Lite)
MODEL_PREFERENCIAL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-lite")
MODEL_SECUNDARIO = os.getenv("GEMINI_MODEL_LIGHT", "gemini-2.0-flash") # Fallback para o modelo completo

class AIAgent:
    def __init__(self, model_name: str = None):
        self.model_name = model_name or MODEL_PREFERENCIAL
        self._load_keys_tiered() # Carrega separado Free vs Paid
        
        if not self.free_keys and not self.paid_key:
            raise ValueError("Nenhuma API Key válida encontrada no .env.")
            
        # Compatibilidade: Lista combinada para loops antigos
        self.api_keys = self.free_keys + ([self.paid_key] if self.paid_key else [])
        
        self.state_file = Path("data/api_state.json")
        self._init_state()
        self._select_best_key()
        self._setup_client()

    def _load_keys_tiered(self):
        """Carrega chaves separando Tier Gratuito de Tier Pago."""
        self.free_keys = []
        self.paid_key = os.getenv("GEMINI_PAID_KEY")
        
        # Carrega todas as chaves padrão como Free Tier
        raw_keys = []
        
        # 1. Chaves do Ambiente (GEMINI_FREE_* ou GEMINI_API_KEY*)
        # Prioriza chaves explicitamente nomeadas como FREE
        for var_name, value in os.environ.items():
            if (var_name.startswith("GEMINI_FREE_") or var_name.startswith("GEMINI_API_KEY")) and value not in raw_keys:
                # Evita carregar a GEMINI_PAID_KEY se ela estiver duplicada com outro nome
                if value != self.paid_key:
                    raw_keys.append(value)
        
        # 2. Arquivo .env (Parsing para pegar comentadas ou ocultas que não subiram pro env)
        try:
            if os.path.exists(".env"):
                with open(".env", "r") as f:
                    content = f.read()
                    matches = re.findall(r"(?:#\s*)?(GEMINI_(?:FREE|API_KEY)[A-Za-z0-9_\-\d]*)\s*=\s*([A-Za-z0-9_\-]+)", content)
                    for _, value in matches:
                        if value not in raw_keys and value != self.paid_key:
                            raw_keys.append(value)
        except Exception:
            pass
            
        self.free_keys = raw_keys

    def _init_state(self):
        """Inicializa ou carrega o estado das chaves de API."""
        self.state = {}
        if self.state_file.exists():
            try:
                with open(self.state_file, "r") as f:
                    self.state = json.load(f)
            except Exception:
                self.state = {}

        # Sincroniza chaves do .env com o estado
        all_known_keys = self.free_keys + ([self.paid_key] if self.paid_key else [])
        updated = False
        
        for key in all_known_keys:
            if key not in self.state:
                self.state[key] = {
                    "last_used": None,
                    "cooldown_until": None,
                    "status": "active", # active, invalid
                    "total_calls": 0,
                    "total_tokens": 0,
                    "tier": "paid" if key == self.paid_key else "free"
                }
                updated = True
        
        if updated:
            self._save_state()

    def _save_state(self):
        """Salva o estado atual no arquivo JSON."""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, "w") as f:
            json.dump(self.state, f, indent=4)

    def _select_best_key(self):
        """
        Algoritmo de Seleção de Chave (V3.0 - Cost Optimized):
        1. Tenta chaves FREE ativas e sem cooldown (seleciona a menos usada recentemente).
        2. Se todas as FREE estiverem em cooldown, tenta a PAID KEY.
        3. Se a PAID também estiver em cooldown (ou não existir), espera a FREE mais próxima.
        """
        now = datetime.now()
        
        # Filtra chaves inválidas permanentemente
        valid_free = [k for k in self.free_keys if self.state[k].get("status") != "invalid"]
        
        # 1. Candidatas Free Disponíveis
        available_free = []
        for key in valid_free:
            cooldown = self.state[key].get("cooldown_until")
            if cooldown:
                if now < datetime.fromisoformat(cooldown):
                    continue
            available_free.append(key)
            
        if available_free:
            # Seleciona a que descansou por mais tempo
            self.current_key = min(available_free, key=lambda k: self.state[k]["last_used"] or "0")
            # print(f"[DEBUG] Usando chave FREE: {self.current_key[:8]}...")
            return

        # 2. Fallback para Paid Key
        if self.paid_key and self.state[self.paid_key].get("status") != "invalid":
            cooldown = self.state[self.paid_key].get("cooldown_until")
            is_ready = True
            if cooldown:
                if now < datetime.fromisoformat(cooldown):
                    is_ready = False
            
            if is_ready:
                print("[$] Todas as chaves Free esgotadas. Usando chave PAGA.")
                self.current_key = self.paid_key
                return

        # 3. Last Resort: Esperar pela chave que libera mais cedo (seja free ou paid)
        all_valid = valid_free + ([self.paid_key] if self.paid_key else [])
        if not all_valid:
             raise ValueError("CRÍTICO: Todas as chaves foram marcadas como INVÁLIDAS.")
             
        soonest_key = min(all_valid, key=lambda k: self.state[k].get("cooldown_until") or "9999-12-31")
        cooldown_until = self.state[soonest_key].get("cooldown_until")
        
        if cooldown_until:
            until_dt = datetime.fromisoformat(cooldown_until)
            if now < until_dt:
                wait_time = min(int((until_dt - now).total_seconds()) + 1, 60)
                if wait_time > 0:
                    print(f"[!] AVISO: Todas as chaves (Free & Paid) em cooldown. Aguardando {wait_time}s até liberação...")
                    time.sleep(wait_time)
        
        self.current_key = soonest_key
        
    def _setup_client(self):
        """Inicializa o cliente com a chave selecionada."""
        key = self.current_key
        masked_key = f"{key[:8]}...{key[-4:]}"
        # Apenas log se for relevante
        # print(f"[*] AI Client pronto: {masked_key}")
        self.client = genai.Client(api_key=key)

    def _mark_key_usage(self, tokens: int = 0):
        """Atualiza o estado de uso da chave atual."""
        key = self.current_key
        self.state[key]["last_used"] = datetime.now().isoformat()
        self.state[key]["total_calls"] += 1
        self.state[key]["total_tokens"] += tokens
        self._save_state()

    def _mark_cooldown(self):
        """Coloca a chave atual em cooldown de 15 minutos."""
        key = self.current_key
        until = (datetime.now() + timedelta(minutes=15)).isoformat()
        self.state[key]["cooldown_until"] = until
        self._save_state()
        print(f"[!] Chave {key[:8]}... em cooldown até {until.split('T')[1][:8]}")

    def _clear_cooldown(self):
        """Remove o cooldown da chave atual (auto-recuperação)."""
        key = self.current_key
        if self.state[key].get("cooldown_until"):
            self.state[key]["cooldown_until"] = None
            self._save_state()

    def generate_content(self, prompt: str, temperature: float = 0.1, max_output_tokens: int = 8192) -> str:
        """
        Geração resiliente com:
        1. Rotação de Chaves (Free -> Paid)
        2. Rotação de Modelos (Preferencial -> Light)
        3. Backoff Exponencial (Retentativas para 503)
        """
        if not hasattr(self, '_response_cache'): self._response_cache = {}
        cache_key = f"{prompt[:100]}_{len(prompt)}_{temperature}"
        if cache_key in self._response_cache:
            return self._response_cache[cache_key]

        # Prioridade de Modelos (Dinâmico v3.1)
        models_to_try = [self.model_name]
        if self.model_name != MODEL_SECUNDARIO:
            models_to_try.append(MODEL_SECUNDARIO)
        
        while True: # Loop de Rotação de Chave (Select Best Key cuida da ordem)
            goto_next_key = False
            for model_id in models_to_try:
                max_retries = 4
                for attempt in range(max_retries):
                    try:
                        print(f"[*] Tentando {model_id} (Attempt {attempt+1}/{max_retries}) | Model Tier: {'FREE' if self.state[self.current_key]['tier'] == 'free' else 'PAID'}")
                        response = self.client.models.generate_content(
                            model=model_id,
                            contents=prompt,
                            config={"temperature": temperature, "max_output_tokens": max_output_tokens}
                        )
                        
                        if not response or not response.text:
                            continue
                        
                        # Sucesso
                        self._mark_key_usage(getattr(response.usage_metadata, 'total_token_count', 0))
                        self._clear_cooldown()
                        self.last_raw_content = response.text.strip()
                        self._response_cache[cache_key] = self.last_raw_content
                        return self.last_raw_content

                    except errors.ServerError as e:
                        if "503" in str(e):
                            wait_time = 2 ** (attempt + 1) + 2 # Exponencial: 4, 6, 10, 18
                            print(f"[!] Erro 503 ({model_id} sobrecarregado). Backoff: {wait_time}s...")
                            time.sleep(wait_time)
                            continue
                        raise e
                    
                    except errors.ClientError as e:
                        if "429" in str(e) or "QUOTA_EXCEEDED" in str(e).upper():
                            print(f"[!] Quota Excedida na chave {self.current_key[:8]}... Rodando chave.")
                            self._mark_cooldown()
                            goto_next_key = True
                            break # Sai do loop de retentativas do modelo para trocar a chave
                        elif any(err in str(e) for err in ["400", "403", "API_KEY_INVALID"]):
                             print(f"❌ Chave INVÁLIDA: {self.current_key[:8]}.")
                             self.state[self.current_key]["status"] = "invalid"
                             self._save_state()
                             goto_next_key = True
                             break
                        else:
                            raise e
                    except Exception as e:
                        print(f"[!] Erro inesperado: {e}")
                        raise e
                
                if goto_next_key:
                    break # Sai do loop de modelos para trocar a chave

                # Se após as 4 tentativas do modelo 1 deu erro de servidor, ele pula pro modelo 2 na MESMA chave
                # antes de tentar rodar a chave se for um erro de cota.
                print(f"[!] Modelo {model_id} indisponível após {max_retries} tentativas.")
                
            # Se chegamos aqui, esgotamos os modelos nesta chave ou tivemos erro de cota
            try:
                self._select_best_key()
                self._setup_client()
            except Exception as ve:
                print(f"[!] Crítico: Todas as chaves e modelos falharam.")
                raise ve

    def _clean_json_text(self, text: str) -> str:
        """Remove blocos de Markdown e tenta reparar JSON truncado."""
        # 1. Limpeza de Markdown e ruído extra
        text = text.strip()
        
        # Busca o primeiro '{' ou '[' e o último '}' ou ']'
        start_brace = text.find('{')
        start_bracket = text.find('[')
        
        # Define o início do JSON
        start_idx = -1
        if start_brace != -1 and start_bracket != -1:
            start_idx = min(start_brace, start_bracket)
        elif start_brace != -1:
            start_idx = start_brace
        elif start_bracket != -1:
            start_idx = start_bracket
            
        # Define o fim do JSON
        end_brace = text.rfind('}')
        end_bracket = text.rfind(']')
        end_idx = max(end_brace, end_bracket)
        
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            text = text[start_idx:end_idx+1]
        
        # 2. Reparo Emergencial (Truncamento)
        # Se o texto parece incompleto (faltam fechamentos)
        if text.count('{') > text.count('}') or text.count('[') > text.count(']'):
            # Busca o último ponto estável: um fechamento de objeto, array ou uma vírgula
            last_good = max(text.rfind('}'), text.rfind(']'), text.rfind(','))
            
            if last_good != -1:
                text = text[:last_good]
                # Se cortamos em uma vírgula, removemos ela também para evitar trailing comma
                text = text.rstrip(',')
        
        # Fecha aspas abertas (caso o corte tenha sido no meio de uma string)
        if text.count('"') % 2 != 0:
            text += '"'

        # Algoritmo de Pilha para fechar estruturas aninhadas corretamente (LIFO)
        stack = []
        in_string = False
        escaped = False
        
        for char in text:
            if char == '"' and not escaped:
                in_string = not in_string
            if in_string:
                if char == '\\': escaped = not escaped
                else: escaped = False
                continue
            
            if char == '{': stack.append('}')
            elif char == '[': stack.append(']')
            elif char == '}':
                if stack and stack[-1] == '}': stack.pop()
            elif char == ']':
                if stack and stack[-1] == ']': stack.pop()
        
        # Fecha as estruturas na ordem inversa
        while stack:
            text += stack.pop()
            
        return text

    def interpret_instruction(self, instruction_text: str, doc_content: str = "") -> Intent:
        """
        Stage 1: Ingestion & Comprehension via Gemini.
        Returns mapped Intent object.
        """
        prompt = f"""
        # ATUE COMO SR. AI ENGINEER - EXTRAÇÃO DE ATRIBUTOS E BUNDLES DINÂMICOS (V2.5 - ENGENHARIA)
        
        Sua tarefa é extrair os dados necessários para uma proposta técnica, focando em quantidades, nuances de ação e **INVENTÁRIO DETALHADO DE VIRTUALIZAÇÃO**.
        
        ## INPUTS
        1. **User Instruction (CLI):** "{instruction_text}"
        2. **Technical Context (PDF):** "{doc_content[:15000]}"
        
        ## DIRETRIZES MESTRAS (GOVERNANÇA E SOBERANIA)
        1. **SOBERANIA ABSOLUTA:** A instrução do usuário é um "Ajuste de Rota". Se o PDF diz "2 servidores" e a instrução diz "apenas 1", **IGNORE O PDF E USE 1**.
        
        ## GOVERNANÇA DE ESCOPO (ANTI-ALUCINAÇÃO)
        1. **NÃO INVENTE QUANTIDADES:** Se a instrução diz apenas "Servidores" e o PDF não especifica, NÃO assuma 1, 2 ou 3. Marque `needs_clarification: true`.
        2. **AGRUPAMENTO OBRIGATÓRIO:** Sempre que múltiplos hardwares fizerem parte de uma solução lógica única (Ex: 3 servidores em um Cluster, 12 servidores para migrar), gere um ÚNICO `ScopeItem` com a quantidade total no campo `detected_quantity`. **NUNCA** atomize em 3 itens separados de quantidade 1 se o contexto for o mesmo.
        3. **IGNORAR SUGESTÃO DE EQUIPE:** Se o input disser "Use 2 técnicos" ou "Sugiro equipe de 3 pessoas", **IGNORE**. A equipe é dimensionada estritamente pelo Motor de Cálculo (LaborEngine).
        4. **ANTI-DEFAULT (CLUSTER/VMWARE):** Se a instrução mencionar apenas "Servidor" ou "Migração", NÃO assuma que é um Cluster ou que utilizará VMware/Hyper-V a menos que esteja explicitamente escrito. Se houver dúvida sobre a arquitetura (Cluster vs Standalone), preencha `needs_clarification: true`.
        5. **TRIGGER DE CLARIFICAÇÃO:** Se houver itens críticos (Servidores, Storage, Switches) sem definição de Quantidade OU sem distinção básica (Físico/Virtual), preencha `needs_clarification: true`. Se a quantidade estiver clara (ex: "3 Servidores"), prossiga usando modelos genéricos de mercado.
        
        ## DIRETRIZES DE EXTRAÇÃO
        1. **DETALHAMENTO TÉCNICO:** O PDF serve apenas para detalhes técnicos (nomes de VMs, modelos) que NÃO foram mencionados na instrução.
        2. **BRANDING:** Extraia o nome do Cliente, Empresa e Contato.
        3. **LOCALIDADE:** Default: **Ilhéus - BA**.
        4. **CALIBRAÇÃO DE ESFORÇO:** Evite atomismo exagerado para itens simples.
        5. **LOGÍSTICA:** Extraia travel_segments array.
        6. **INVENTÁRIO DE VMS:** Se a instrução reduzir a quantidade de VMs, reduza proporcionalmente.
        
        ## SELEÇÃO DE TEMPLATE TÉCNICO
        Escolha o template que melhor se adapta ao escopo principal:
        - `struct_assessment.md`: Foco estritamente CONSULTIVO de diagnóstico, inventário e auditoria (Assessment).
        - `iodc_full_structured.md`: Projetos completos (Infraestrutura + Rede + Backup).
        - `iodc_no_net.md`: Foco em Datacenter/Servidores (sem escopo de rede industrial).
        - `struct_network_industrial.md`: Projetos de Implantação de Redes OT (Switches, Fibra, Firewalls).
        - `struct_server_migration.md`: Foco em Virtualização e Migração de sistemas.
        - `struct_services_cabling.md`: Foco em Cabeamento e Infraestrutura Física.
        - `noc_monitoring_support.md`: Contratos de Sustentação, Monitoramento e Suporte NOC (quando a infra já existe).
        ## REGRAS DE EXTRAÇÃO E CLASSIFICAÇÃO DETERMINÍSTICA (V7.0)
        1. **MAPEAMENTO COMPLETO DE ITENS (SOMA PDF + CLI)**: 
           - Extraia CADA item listado na seção "Relação de Itens" (Existentes e Novos) da Instrução.
           - Extraia os part numbers e detalhes específicos do PDF.
           - **MESCLE:** Use a quantidade da instrução (SOBERANIA) mas os detalhes do PDF.
        2. **CLASSIFICAÇÃO MANDATÓRIA (ACTION_TYPE)**:
           O campo `action_type` é o gatilho para o cálculo de mão de obra. Você DEVE usar um destes valores exatos:
           - `SWITCH`: Para switches de acesso, core ou industriais.
           - `SERVER`: Para servidores físicos (Bare Metal).
           - `STORAGE`: Para storages NAS/SAN físicos.
           - `VM`: Para criação de máquinas virtuais (Infra VM).
           - `WIFI`: Para Access Points e Controladoras.
           - `FIREWALL`: Para ativos de segurança física/virtual.
           - `BACKUP`: Para sistemas de proteção de dados.
           - `MIGRATION`: Para migração de cargas (P2V/V2V).
           - `CABLING`: Para serviços de infraestrutura passiva/fibra.
           - `DESIGN`: Para planejamento, arquitetura e LLD.
        3. **NÃO IGNORE O FINAL DO TEXTO**: Certifique-se de capturar itens como Backup, DR e Migração.
        4. **CLIENTE VS PROVEDOR (CRÍTICO)**:
           - O **PROVEDOR** (Sua empresa) é SEMPRE "EGE Soluções Industriais" (ou "EGE").
           - O **CLIENTE** é a empresa para quem a proposta está sendo enviada (ex: OFI, Bionovis, Maratá).
            - **NUNCA** preencha `client_name` com "EGE".
            - **NUNCA** preencha `company_name` com "EGE". `company_name` deve ser o nome completo do CLIENTE.
         5. **NATUREZA DO PROJETO (PROJECT_NATURE)**:
            - `brownfield`: Se o objetivo principal envolver termos como "migração", "remanejamento", "retrofit", "mudança", "limpeza", "adequação", "ajuste" ou "reorganização" de itens existentes.
            - `greenfield`: Se o projeto focar em "nova planta", "expansão", "novas capacidades", "implantação do zero" ou "novas redes".
         6. **OPEX E RECORRÊNCIA (EXCLUDE_OPEX)**:
            - Set `exclude_opex: true` se a instrução explicitamente disser termos como "Apenas CAPEX", "Sem OPEX", "Não incluir sustentação", "Sem serviços recorrentes" ou "Apenas projeto/implantação".

        ## FORMATO DE SAÍDA (JSON ESTRITO)
        {{
            "client_name": "String",
            "company_name": "String",
            "contact_name": "String",
            "company_short_name": "String",
            "project_name": "String",
            "project_motivation": "String",
            "hardware_supply_by_client": boolean,
            "estimated_duration_weeks": int,
            "governance_level": "standard" | "intensive" | "critical",
            "work_on_weekends": boolean,
            "requires_training": boolean,
            "selected_tech_template": "struct_assessment.md" | "iodc_full_structured.md" | "iodc_no_net.md" | "struct_network_industrial.md" | "struct_server_migration.md" | "struct_services_cabling.md" | "noc_monitoring_support.md",
            "selected_comm_template": "hybrid_capex_opex.md",
            "exclude_opex": boolean,
            "is_assessment": boolean, // Define se é um trabalho puramente consultivo
            "split_proposal": boolean,
            "sizing_mode": "aggressive" | "standard" | "secure" | "critical",
            "contingency_level": "none" | "low" | "standard" | "high",
            "project_nature": "greenfield" | "brownfield",
            "scope_items": [
                {{
                    "name": "String (Ex: Implantação de Servidores Dell R670)",
                    "detected_quantity": int,
                    "action_type": "SWITCH" | "SERVER" | "STORAGE" | "VM" | "WIFI" | "FIREWALL" | "BACKUP" | "MIGRATION" | "CABLING" | "DESIGN" | "TRAINING" | "SOFTWARE" | "HARDWARE",
                    "summary_rational": "String",
                    "context_note": "String",
                    "visibility": "public",
                    "explicit_total_hours": int,
                    "is_weekend": boolean
                }}
            ],
            "logistics_override": {{
                "transport_provider": "provider",
                "consulting": boolean,
                "team_size": int,
                "travel_segments": [int]
            }},
            "needs_clarification": boolean,
            "clarification_questions": [],
            "confidence_score": float,
            "detected_hardware_list": [
                {{
                    "description": "String",
                    "quantity": int,
                    "part_number": "String"
                }}
            ]
        }}

        Responda APENAS com o JSON puro. Seja direto e siga a estrutura à risca.
        """
        
        raw_text = self.generate_content(prompt, temperature=0.1, max_output_tokens=8192)
        
        # Armazenar o texto bruto para debug externo
        self.last_raw_interpretation = raw_text
        
        if len(raw_text) < 500:
             print(f"⚠️ AVISO: Resposta da IA muito curta ({len(raw_text)} chars). Possível truncamento.")
             
        clean_text = self._clean_json_text(raw_text)
        
        try:
            data = json.loads(clean_text)
            return Intent(**data)
        except Exception as e:
            print(f"CRÍTICO: Erro de Parsing no Intent. Verifique raw_ai_interpretation.txt. Erro: {e}")
            raise e

    def plan_logistics(self, origin: str, destination: str, instruction_text: str, team_size: int, duration_days: int) -> LogisticsPlan:
        """
        Stage 2: Logistics Planning.
        """
        prompt = f"""
        # ATUE COMO LOGISTICS MANAGER - PLANEJAMENTO DE VIAGEM (V1.2)
        
        Você é um especialista em logística. Planeje a viagem de {origin} para {destination}. 
        Considere a instrução: '{instruction_text}'. 
        
        ## PARÂMETROS
        - Equipe: {team_size} pessoas
        - Duração: {duration_days} dias
        
        ## DEFINIÇÕES DE RECURSOS (V1.3 - REGRAS GEOGRÁFICAS)
        1. **requires_flight**: 
           - **SANTOS / CAPITAL / INTERIOR SP**: Se a origem é Jundiaí e o destino é Santos, Capital ou Interior de SP, **Sempre FALSE** (Use carro).
           - **NORDESTE / SUL / NORTE**: Se for interestadual de longa distância (> 400km), **True**.
        2. **flight_region**: "flight_ne" para Nordeste, "flight_s_se" para Sul/Sudeste longo.
        3. **requires_car_rental**: True.
        4. **estimated_daily_km**: Média de deslocamento local. Default: 60km (Hotel <-> Fábrica).
        5. **requires_freight**: True apenas se houver escopo de equipamentos pesados (racks, servidores) novos a serem enviados.
        6. **hotel_tier**: "hotel_tier_interior" para cidades fora de capitais, "hotel_tier_capital" para capitais.
        7. **origin_mobilization_km**: 65.0 (Jundiaí -> Aeroporto) se houver voo. Se não houver voo (Carro), pode ser 0 ou a distância real.
        8. **flight_cost_override**: Nulo (null), a menos que o usuário dê um valor explícito.

        ## OUTPUT JSON FORMAT
        {{
            "requires_flight": true,
            "flight_region": "flight_ne",
            "flight_cost_override": null,
            "requires_car_rental": true,
            "estimated_daily_km": 60,
            "requires_freight": false,
            "hotel_tier": "hotel_tier_interior",
            "origin_mobilization_km": 65.0
        }}
        
        Responda APENAS com o JSON.
        """
        
        raw_text = self.generate_content(prompt, temperature=0.1)
        
        # Armazenar para debug
        self.last_raw_logistics = raw_text

        clean_text = self._clean_json_text(raw_text)
            
        try:
            data = json.loads(clean_text)
            return LogisticsPlan(**data)
        except Exception as e:
            print(f"CRÍTICO: Erro de Parsing na Logística. Verifique raw_ai_interpretation.txt. Erro: {e}")
            raise e

    def compose_technical_redaction(self, intent_summary: str, tech_scope: str, proposal_summary: str, is_assessment: bool = False, project_nature: str = "greenfield") -> Dict[str, Any]:
        """Gera o corpo técnico da proposta usando IA para personalização."""
        if is_assessment:
            # --- PROMPT EXCLUSIVO PARA ASSESSMENT (v2.0 - Pureza Consultiva) ---
            prompt = f"""
            # ATUE COMO CONSULTOR SÊNIOR DE INFRAESTRUTURA INDUSTRIAL
            
            Sua tarefa é redigir uma Proposta Técnica de ASSESSMENT (Diagnóstico e Auditoria).
            NATUREZA DO PROJETO: {project_nature.upper()}
            
            ## REGRAS CRÍTICAS DE NEGÓCIO (PUREZA CONSULTIVA):
            1. **FOCO TOTAL EM INVESTIGAÇÃO**: O trabalho é descobrir o estado atual (As-Is).
            2. **PROIBIDO**: Não mencione fornecimento de equipamentos, instalação física (passagem de cabos), configuração de novos sistemas, treinamento de operadores ou serviços de monitoramento/sustentação.
            3. **DETALHAMENTO DE CAMPO**: Descreva atividades como "desconexão de cabos para teste", "mapeamento porta-a-porta", "auditoria de painéis" e "validação de running configs".
            
            ## INPUTS DO PROJETO:
            - MOTIVAÇÃO: {intent_summary}
            - ITENS SOB ANÁLISE: {tech_scope}
            
            ## SEÇÕES REQUERIDAS (JSON):
            - custom_objective_md: 2 parágrafos sobre a dor e a estratégia de investigação.
            - custom_benefits_md: Benefícios da documentação e visibilidade (As-Is).
            - custom_vision_md: Metodologia em 4-5 passos (ex: Auditoria Física, Auditoria Lógica, Running Configs, Relatório).
            - testing_protocol_md: Como as conexões serão validadas (testes passivos e de continuidade).
            - team_structure_md: Papéis (Consultor, Especialista em Automação, Técnico de Redes).
            - timeline_md: Marcos (Entrevista de Alinhamento, Diagnóstico de Campo, Consolidação, Entrega Final).
            - deliverables_list_md: Lista de documentos entregues (Relatório, Inventário PN, Diagramas As-Is).
            
            ## SEÇÕES PROIBIDAS (DEIXE VAZIAS):
            - custom_training_md: ""
            - asset_table_md: "" (Será listado em outro bloco)
            - cabling_context_md: ""
            - software_licensing_md: ""
            
            Responda APENAS o JSON.
            """
        else:
            # --- PROMPT PADRÃO PARA IMPLANTAÇÃO (v1.4) ---
            prompt = f"""
            # ATUE COMO ENGENHEIRO DE SISTEMAS SÊNIOR E REDATOR TÉCNICO (V1.4 - ALTA FIDELIDADE)
            
            Sua tarefa é gerar 6 blocos de texto personalizados e RÍGIDOS em Markdown para uma proposta técnica industrial. 
            O objetivo é eliminar qualquer tom genérico. Se o texto parecer "boilerplate", ele falhou.
            
            ## INPUTS DO PROJETO
            - NATUREZA: {project_nature.upper()}
            - RESUMO DO INTENT: {intent_summary}
            - ESCOPO TÉCNICO DETALHADO: {tech_scope}
            
            ## DIRETRIZES DE TOM (V1.5 - REALISMO TÉCNICO)
            Se {project_nature.upper()} == "BROWNFIELD":
                - Foco: Mitigação de riscos, continuidade operacional, organização (limpeza técnica), segurança e conformidade normativa.
                - Proibido: Usar "Nova rede", "Transformação completa", "Modernização estratégica".
                - Termos Preferenciais: "Adequação", "Continuidade", "Remanejamento seguro", "Normalização física".
            Se {project_nature.upper()} == "GREENFIELD":
                - Foco: Inovação, robustez, escalabilidade, nova infraestrutura.
                - Termos Preferenciais: "Nova rede de automação", "Implantação estratégica", "Evolução".
            - RESUMO DA PROPOSTA (VALORES/HORAS): {proposal_summary}
            
            ## INSTRUÇÕES DE REDAÇÃO (DIRETRIZES)
            1. **Seção: Objetivo Geral**: Escreva obrigatoriamente 2 parágrafos. 
               - Parágrafo 1: Contextualize a dor/necessidade do cliente (Cenário atual explicado).
               - Parágrafo 2: Resuma nossa sugestão/estratégia de solução de forma objetiva.
            2. **Seção: Benefícios (Extensivo)**:
               - Gere no mínimo de 2 a 3 categorias usando títulos ###.
               - Em cada categoria, adicione 2 a 3 bullet points detalhados.
               - O texto deve explicar o ganho real para este escopo. Ex: "Eliminação de loops de rede através de protocolos RSTP/STP", "Redução de inatividade por falhas de infraestrutura física".
            3. **Seção: Visão Geral da Solução (O Coração da Proposta)**:
               - Descreva a solução em 4 a 5 passos numerados de 1 a 5.
               - Cada passo deve ter um título em negrito e uma explicação técnica de 2 linhas.
               - Adapte ao escopo: Se for rede, os passos são Design, Greenfield/Brownfield, Backbone, Acesso, Segurança e SAT. Se for migração, foque em Inventário, Staging, Cutover e Validação.
               - **EVITE REPETIÇÃO**: Garanta que o passo de "Infraestrutura Física" (se houver) não repita o conteúdo de "Design/Planejamento".
            4. **Seção: Protocolo de Testes**: Foco em validação de aceitação (SAT). Explique a metodologia de testes em ambientes de manufatura/operação.
            5. **Seção: Estrutura da Equipe**: Cargos e responsabilidades (Gestor, Engenheiro, Especialista em Automação, Técnicos de Campo).
            6. **Seção: Cronograma**: 
               - **PROIBIDO**: Mencionar quantidade exata de horas ou dias (Ex: NÃO diga "185 horas" ou "20 dias").
               - **OESTRUTURA**: Comece obrigatoriamente com o marco "**Entrevista de Expectativa**" seguido de Kick-off, Mobilização, Execução, SAT e Handover.
               - **ESTRUTURA**: Um parágrafo dissertativo sobre o fluxo do projeto seguido por uma lista sucinta de "Marcos do Plano".
            7. **Seção: Treinamento**: Foco em transferência de conhecimento. NÃO mencione "quadros elétricos" a menos que seja instalação elétrica. Use termos genéricos: "Apresentação dos equipamentos, organização e identificação dos ativos".
            8. **Seção: Tabela de Ativos (OPEX)**: Crie uma tabela Markdown consolidando os ativos que serão suportados/monitorados (para o bloco de Sustentação).

            ## REGRAS DE OURO
            - **PROIBIDO**: Termos genéricos corporativos ("value-add", "best-in-class").
            - **BRANDING**: Use nomes genéricos técnicos ou descritivos da operação ("Área de Envasado", "Rede de Automação da Moega", "Cluster de Virtualização Industrial").
            - **SOBERANIA INDUSTRIAL**: Lembre-se que o usuário muitas vezes trabalha com MÁQUINAS e OPERAÇÕES, não apenas servidores em racks de escritório.
            
            ## FORMATO DA RESPOSTA (JSON ESTRITO)
            {{
                "custom_objective_md": "Markdown aqui",
                "custom_benefits_md": "Markdown aqui (com títulos ### e bullets)",
                "custom_vision_md": "Markdown aqui (pontos numerados 1 a 5)",
                "testing_protocol_md": "Markdown aqui (Protocolo de Testes Industrial)",
                "team_structure_md": "Markdown aqui (Equipe e Responsabilidades)",
                "timeline_md": "Markdown aqui (Fluxo do projeto e Marcos)",
                "custom_training_md": "Markdown aqui (Transferência de conhecimento)",
                "asset_table_md": "Tabela Markdown com os ativos monitorados",
                "cabling_context_md": "Texto CONCISO sobre conectividade, cabos e acessórios industriais",
                "software_licensing_md": "Texto CONCISO sobre licenciamento de automação e sistemas operacionais",
                "deliverables_list_md": "Lista em bullets dos entregáveis REAIS (ex: Databook, SAT, Treinamento, Relatório de Certificação de Rede)."
            }}
            
            Responda APENAS o JSON. Seja conciso mas técnico.
            """

        raw_text = self.generate_content(prompt, temperature=0.3, max_output_tokens=16384)
        clean_text = self._clean_json_text(raw_text)
        
        try:
            return json.loads(clean_text)
        except Exception:
            # Fallback aprimorado para manter as novas regras mesmo em erro
            if is_assessment:
                return {
                    "custom_objective_md": "O assessment foca na investigação técnica e diagnóstico da infraestrutura atual.",
                    "custom_benefits_md": "### Visibilidade e Diagnóstico\n* Documentação As-Is completa.\n* Identificação de gargalos.",
                    "custom_vision_md": "1. Investigação de Campo\n2. Auditoria Lógica\n3. Consolidação de Dados\n4. Relatório Final",
                    "testing_protocol_md": "Validação de conectividade baseada em testes físicos porta-a-porta.",
                    "team_structure_md": "Equipe especializada em diagnóstico de redes e automação industrial.",
                    "timeline_md": "* **Entrevista de Expectativa**\n* Coleta de Dados\n* Auditoria de Campo\n* Entrega de Relatórios",
                    "custom_training_md": "",
                    "asset_table_md": ""
                }
            return {
                "custom_objective_md": f"{intent_summary}\n\nNossa proposta foca na modernização e segurança da infraestrutura para garantir a continuidade operacional conforme os requisitos apresentados.",
                "custom_benefits_md": "### Confiabilidade e Segurança\n* Mitigação de riscos de parada.\n* Proteção de ativos críticos.",
                "custom_vision_md": "1. Planejamento\n2. Execução de Infra\n3. Configuração Lógica\n4. Testes e Validação\n5. Handover",
                "testing_protocol_md": "Protocolo de testes (SAT) a ser definido no kick-off focado em ambiente industrial.",
                "team_structure_md": "Equipe multidisciplinar composta por Coordenador, Engenheiros e Técnicos Especializados.",
                "timeline_md": "*   **Entrevista de Expectativa**\n*   Kick-off\n*   Mobilização\n*   Execução e Configuração\n*   Testes de Aceitação (SAT)\n*   Handover e Treinamento",
                "custom_training_md": "Treinamento focado na operação dos ativos, identificação de pontos e procedimentos de emergência.",
                "asset_table_md": "| Ativo | Descrição |\n| :--- | :--- |\n| Infraestrutura | Conforme levantamento |"
            }

    def research_technical_wbs(self, activity_name: str, context: str = "") -> List[Dict[str, Any]]:
        """
        Stage 4: Research Engine (AI-Powered WBS Decomposition).
        Usa o Prompt Mestre de Engenharia de Processos do usuário para detalhar atividades.
        """
        # Mapping for the AI to use existing system roles
        role_guidance = "Auxiliar, Técnico, Analista, Engenheiro, Arquiteto ou Gestor"
        
        prompt = f"""
        # ATUE COMO ESPECIALISTA EM ENGENHARIA DE PROCESSOS DE TI E GESTÃO DE CUSTOS (V8.0)
        
        CONTEXTO: Preciso decompor uma atividade macro de TI em tarefas menores para otimizar a escala de técnicos e custos.
        ATIVIDADE: "{activity_name}"
        CONTEXTO ADICIONAL: "{context}"

        ## INSTRUÇÕES DE EXECUÇÃO:

        1. **Decomposição:** Quebre a atividade em blocos lógicos baseados na senioridade necessária.
        2. **Regra de Unidade de Tempo:** Cada bloco deve ter uma estimativa de hora cheia (1h, 2h, 3h...). Arredonde para cima, considerando tempos de deslocamento, testes e processamento de fundo.
        3. **Perfil de Custo:** Atribua cada bloco a um dos seguintes perfis EXATAMENTE: {role_guidance}.
        4. **Microtarefas (Checklist):** Liste as subetapas manuais necessárias dentro de cada hora estimada.
        5. **Justificativa de Prazo:** Explique por que leva esse tempo e por que esse profissional foi escolhido.

        ## FORMATO DA RESPOSTA (JSON ESTRITO)
        Retorne uma LISTA de objetos seguindo EXATAMENTE este esquema:
        [
            {{
                "id": "RES_001",
                "category": "PHASE_X",  // Escolha entre PHASE_1 (Plan), PHASE_2 (Phys), PHASE_3 (Net), PHASE_5 (Soft)
                "name": "Nome da Tarefa (Única linha, ação direta)",
                "role": "Nome do Perfil",
                "setup_hours": 0.0,
                "unit_hours": float,
                "description": "Resumo conciso da tarefa (máximo 3 linhas ou checklist curto)",
                "rationale": "Justificativa técnica"
            }}
        ]

        Responda APENAS com o JSON puro.
        """
        
        raw_text = self.generate_content(prompt, temperature=0.1)
        clean_text = self._clean_json_text(raw_text)
            
        try:
            return json.loads(clean_text)
        except Exception as e:
            print(f"ERRO no Research AI: {e}")
            return []

    def get_usage_stats(self) -> str:
        """Retorna um resumo formatado do uso de todas as chaves."""
        report = ["## 📊 RELATÓRIO DE USO DE APIS (v2.6.1)"]
        total_tokens_all = 0
        total_calls_all = 0
        
        for i, (key, info) in enumerate(self.state.items()):
            masked = f"{key[:8]}...{key[-4:]}"
            cooldown = info.get("cooldown_until")
            status = "✅ OK"
            if cooldown:
                if datetime.now() < datetime.fromisoformat(cooldown):
                    status = f"❄️ COOLDOWN (até {cooldown.split('T')[1][:5]})"
            
            last = info.get("last_used")
            if last and isinstance(last, str):
                last = last.split("T")[1][:8]
            else:
                last = "Nunca"

            report.append(f"- **Key {i+1}** ({masked}): {status}")
            report.append(f"  - Uso: {info['total_calls']} chamadas | {info['total_tokens']:,} tokens")
            report.append(f"  - Última: {last}")
            
            total_tokens_all += info["total_tokens"]
            total_calls_all += info["total_calls"]

        report.append(f"\n**TOTAL ACUMULADO: {total_calls_all} chamadas | {total_tokens_all:,} tokens**")
        return "\n".join(report)
