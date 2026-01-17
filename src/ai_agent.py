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
#MODEL_ID = "gemini-3-flash-preview"
MODEL_ID = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

class AIAgent:
    def __init__(self):
        self.model_name = MODEL_ID
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
             
        print("[!] AVISO: Todas as chaves (Free & Paid) em cooldown. Priorizando a que libera mais cedo.")
        self.current_key = min(all_valid, key=lambda k: self.state[k].get("cooldown_until") or "9999-12-31")
        
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
        Metodo genérico com retentativas, rotação inteligente e rastreamento de tokens.
        """
        max_retries_per_key = 2
        keys_tried = 0
        total_keys = len(self.api_keys)
        
        while keys_tried < total_keys:
            for attempt in range(max_retries_per_key):
                try:
                    response = self.client.models.generate_content(
                        model=MODEL_ID,
                        contents=prompt,
                        config={
                            "temperature": temperature,
                            "max_output_tokens": max_output_tokens
                        }
                    )
                    if not response or not response.text:
                        print(f"[!] Resposta vazia da IA (Tentativa {attempt + 1})...")
                        continue
                    
                    # Rastreamento de Tokens
                    tokens_total = 0
                    tokens_prompt = 0
                    tokens_output = 0
                    if hasattr(response, 'usage_metadata'):
                        tokens_total = response.usage_metadata.total_token_count
                        tokens_prompt = response.usage_metadata.prompt_token_count
                        tokens_output = response.usage_metadata.candidates_token_count
                    
                    self._mark_key_usage(tokens_total)
                    print(f"[METRICS] MODEL={MODEL_ID} TOKENS_PROMPT={tokens_prompt} TOKENS_OUTPUT={tokens_output} TOTAL={tokens_total}")
                    
                    self._clear_cooldown() # Se funcionou, não precisa de cooldown
                        
                    self.last_raw_content = response.text.strip()
                    return self.last_raw_content

                except errors.ServerError as e:
                    wait_time = (attempt + 1) * 3
                    print(f"[!] Servidor Sobrecarregado (503). Esperando {wait_time}s... ({e})")
                    time.sleep(wait_time)
                    
                except errors.ClientError as e:
                    if "429" in str(e) or "QUOTA_EXCEEDED" in str(e).upper():
                        masked_key = f"{self.current_key[:8]}...{self.current_key[-4:]}"
                        print(f"[!] Quota Excedida na chave {masked_key}. (Erro 429)")
                        self._mark_cooldown()
                        break # Rotaciona para próxima chave
                        
                    elif "400" in str(e) or "403" in str(e) or "API_KEY_INVALID" in str(e):
                         masked_key = f"{self.current_key[:8]}...{self.current_key[-4:]}"
                         print(f"❌ [CRÍTICO] Chave INVÁLIDA ou REVOGADA: {masked_key}. Desativando permanentemente.")
                         self.state[self.current_key]["status"] = "invalid"
                         self._save_state()
                         break # Rotaciona para próxima chave
                         
                    else:
                        print(f"[!] Erro de API Genérico: {e}")
                        raise e
                except Exception as e:
                    print(f"[!] Erro inesperado na IA: {e}")
                    raise e
            
            # Rotaciona para a próxima "melhor" chave
            try:
                self._select_best_key()
                self._setup_client()
            except ValueError as ve:
                print(f"[!] Fim da linha: {ve}")
                raise ve
                
            keys_tried += 1
            time.sleep(1)

        raise Exception("Todas as chaves de API falharam ou estão em cooldown.")

    def _clean_json_text(self, text: str) -> str:
        """Remove blocos de Markdown e tenta reparar JSON truncado."""
        # 1. Limpeza de Markdown
        text = text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\n", "", text)
            text = re.sub(r"\n```$", "", text)
        
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
        
        ## DIRETRIZES MESTRAS (SOBERANIA DA INSTRUÇÃO)
        1. **SOBERANIA ABSOLUTA:** A instrução do usuário é um "Ajuste de Rota". Se o PDF diz "2 servidores" e a instrução diz "apenas 1", **IGNORE O PDF E USE 1**.
        2. **DETALHAMENTO TÉCNICO:** O PDF serve apenas para detalhes técnicos (nomes de VMs, modelos) que NÃO foram mencionados na instrução.
        3. **BRANDING OBRIGATÓRIO:** O Cliente deve ser sempre **'Gilmar Corrêa'** e a Empresa **'OFI'**. 
        4. **LOCALIDADE:** O local do projeto é **Ilhéus - BA**.
        5. **CALIBRAÇÃO DE ESFORÇO (CALIBRATED WBS):**
           - Evite atomismo exagerado. Para itens simples (ex: 1 servidor, 1 switch), a lista de atividades deve ser concisa (ex: 5-10 atividades totais).
           - Para projetos complexos (ex: Datacenter completo, Migração crítica), a lista deve ser granular (>30 atividades).
           - Se a instrução é simples, responda com simplicidade técnica.
        6. **LOGÍSTICA:** 
           - **travel_segments**: Extraia o array de dias de cada viagem.
           - **team_size**: Extraia a quantidade de pessoas.
        7. **INVENTÁRIO DE VMS:** 
           - Localize a seção de Serviços Críticos/VMs no PDF.
           - Se a instrução reduzir a quantidade de VMs, reduza proporcionalmente mantendo a diversidade de tipos detectados.
        
        ## REGRAS DE EXTRAÇÃO E CLASSIFICAÇÃO
        1. **client_name:** "Gilmar Corrêa" (Default).
        2. **company_name:** "OFI" (Default).
        3. **scope_items**: Extraia os itens de escopo como uma LISTA DE OBJETOS JSON.
            - **Para VMs:** Consolide VMs de mesma função e perfil em uma única linha de escopo se elas forem repetitivas (ex: "8 VMs de Infraestrutura", qtde: 8). Se as VMs tiverem nomes e funções únicas e críticas no PDF, mantenha o detalhamento individual (qtde: 1 por linha).
              - "action_type": infra_vm, heavy_app_vm, db_vm, vdi_vm.
              - "context_note": Mencione a seção do PDF. SEJA CONCISO.
           - **Para Hardware/Outros:** Use os tipos padrão (`install`, `migrate_p2v`, `supply_only`, `turnkey`, `design`).
        4. **logistics**:
           - **travel_segments**: Array de dias por viagem.
           - **team_size**: Default: 1.
        5. **estimated_duration_weeks**: Baseie no cronograma do PDF. Default: 1.
        6. **requires_training**: True se o usuário solicitar "curso", "treinamento", "capacitação" ou se houver item de escopo relacionado.
        
        ## REGRAS DE ROTEAMENTO (V5.5 - PREVC)
        1. **selected_tech_template**: 
           - **Redes Industriais (Switches/OT):** Use `struct_network_industrial.md` se o escopo for focado em anéis óticos, switches industriais ou segmentação.
           - **Cabeamento/Serviços:** Use `struct_services_cabling.md` se o foco for lançamento de cabos, fusão de fibra, certificação e passivos.
           - **Migração/Upgrade:** Use `struct_server_migration.md` se for P2V, V2V, troca de servidores ou storage.
           - **Datacenter Sem Rede:** Use `iodc_no_net.md` se for explicitamente solicitado excluir a rede.
           - **Datacenter Completo (Default):** Use `iodc_full_structured.md` para projetos Turnkey (Infra + TI) completos.
        2. **selected_comm_template**:
           - Se a instrução mencionar "suporte mensal", "SLA", "recorrência" ou "manutenção": `hybrid_capex_opex.md`.
           - Caso contrário (Default): `capex_only.md`.
        3. **split_proposal**: 
           - Defina como `true` se o usuário solicitar "propostas separadas", "compliance", "anexo técnico", ou "arquivos técnicos e comerciais distintos".
           - Se não houver menção, defina como `false`.

        ## REGRAS DE TERMÔMETRO (V6.0)
        Analise o tom e keywords da instrução para calibrar a proposta:
        1. **sizing_mode**:
           - "aggressive" se: "enxuto", "competitivo", "mínimo", "agressivo", "econômico".
           - "secure" se: "robusto", "conservador", "seguro", "com folga", "premium".
           - "standard" (Default) caso contrário.
         2. **contingency_level**:
            - "none" APENAS se: "sem contingência", "risco zero", "sem gordura".
            - "high" se: "muito risco", "incerteza", "ambiente complexo", "instável".
            - "standard" (Padrão para Gilmar Corrêa) caso contrário.

        ## FORMATO DE SAÍDA (JSON ESTRITO)
        {{
            "client_name": "Gilmar Corrêa",
            "company_name": "OFI",
            "project_name": "String",
            "hardware_supply_by_client": boolean,
            "estimated_duration_weeks": int,
            "governance_level": "standard" | "intensive",
            "work_on_weekends": boolean,
            "requires_training": boolean,
            "selected_tech_template": "iodc_full_structured.md" | "iodc_no_net.md" | "struct_network_industrial.md" | "struct_services_cabling.md" | "struct_server_migration.md",
            "selected_comm_template": "capex_only.md" | "hybrid_capex_opex.md",
            "split_proposal": boolean,
            "sizing_mode": "aggressive" | "standard" | "secure",
            "contingency_level": "none" | "low" | "standard" | "high",
            "scope_items": [
                {{
                    "name": "Nome do Item",
                    "detected_quantity": int,
                    "action_type": "infra_vm" | "heavy_app_vm" | "db_vm" | "vdi_vm" | "install" | ... ,
                    "context_note": "String",
                    "visibility": "public" | "internal",
                    "explicit_total_hours": int,
                    "is_weekend": boolean
                }}
            ],
            "logistics_override": {{
                "transport_provider": "client" | "provider",
                "consulting": boolean,
                "team_size": int,
                "travel_segments": [int]
            }}
        }}

        Responda APENAS com o JSON puro.
        """
        
        raw_text = self.generate_content(prompt, temperature=0.1)
        
        # Armazenar o texto bruto para debug externo (será salvo pelo main.py se --debug estiver ativo)
        self.last_raw_interpretation = raw_text
        
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
        
        ## DEFINIÇÕES DE RECURSOS
        1. **requires_flight**: True se a distância > 400km ou se for interestadual. No caso de Ilhéus, saindo de Jundiaí/SP, é OBRIGATÓRIO.
        2. **flight_region**: "flight_ne" (Nordeste).
        3. **requires_car_rental**: True.
        4. **estimated_daily_km**: Média de deslocamento local. Default: 60km (Hotel <-> Fábrica).
        5. **requires_freight**: True apenas se houver escopo de equipamentos pesados (racks, servidores) novos a serem enviados.
        6. **hotel_tier**: "hotel_tier_interior" (Ilhéus).
        7. **origin_mobilization_km**: 65.0 (Jundiaí -> Aeroporto).
        8. **flight_cost_override**: Nulo (null), a menos que o usuário dê um valor explícito na instrução. **NÃO INVENTE VALORES**.

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
                "name": "Nome da Tarefa",
                "role": "Nome do Perfil",
                "setup_hours": 0.0,
                "unit_hours": float,
                "description": "Checklist: [sub-atividades]",
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
