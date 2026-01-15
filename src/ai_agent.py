import os
import json
import time
import re
from google import genai
from google.genai import errors
from dotenv import load_dotenv
from src.models import Intent, LogisticsPlan

load_dotenv()

# Usando o modelo mais recente conforme diretriz Section 5.
MODEL_ID = "gemini-2.5-flash" 

class AIAgent:
    def __init__(self):
        self.model_name = MODEL_ID
        self.api_keys = self._load_all_keys()
        if not self.api_keys:
            raise ValueError("Nenhuma GEMINI_API_KEY encontrada no arquivo .env.")
        
        self.current_key_index = 0
        self._setup_client()

    def _load_all_keys(self):
        """Carrega todas as chaves do .env e do ambiente, priorizando a GEMINI_API_KEY ativa."""
        keys = []
        
        # 1. Tentar pegar a chave principal do ambiente primeiro (Garante prioridade)
        main_key = os.getenv("GEMINI_API_KEY")
        if main_key:
            keys.append(main_key)
        
        # 2. Capturar outras chaves do ambiente (GEMINI_API_KEY_1, GEMINI_API_KEY-2, etc)
        for var_name, value in os.environ.items():
            if var_name.startswith("GEMINI_API_KEY") and value not in keys:
                keys.append(value)
        
        # 3. Ler o arquivo .env para chaves comentadas ou variantes não carregadas no ambiente
        try:
            if os.path.exists(".env"):
                with open(".env", "r") as f:
                    content = f.read()
                    # Busca por padrões de chaves, inclusive comentadas
                    matches = re.findall(r"(?:#\s*)?(GEMINI_API_KEY[A-Za-z0-9_\-\d]*)\s*=\s*([A-Za-z0-9_\-]+)", content)
                    for var_name, value in matches:
                        if value not in keys:
                            keys.append(value)
        except Exception as e:
            print(f"Erro ao ler .env para carregar chaves: {e}")
            
        return keys

    def _setup_client(self):
        """Inicializa o cliente com a chave atual."""
        key = self.api_keys[self.current_key_index]
        # Mascarando a chave para o log
        masked_key = f"{key[:8]}...{key[-4:]}"
        print(f"[*] Iniciando AI com chave: {masked_key} (Índice: {self.current_key_index + 1}/{len(self.api_keys)})")
        self.client = genai.Client(api_key=key)

    def _rotate_key(self):
        """Troca para a próxima chave disponível."""
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        self._setup_client()

    def generate_content(self, prompt: str, temperature: float = 0.1) -> str:
        """
        Metodo genérico com retentativas, rotação de chaves e backoff exponencial.
        """
        max_retries_per_key = 2
        total_keys = len(self.api_keys)
        keys_tried = 0
        
        while keys_tried < total_keys:
            for attempt in range(max_retries_per_key):
                try:
                    response = self.client.models.generate_content(
                        model=MODEL_ID,
                        contents=prompt,
                        config={"temperature": temperature}
                    )
                    
                    if not response or not response.text:
                        # Se o modelo retornou vazio mas não deu erro, pode ser um filtro de segurança
                        # ou um problema temporário. Vamos tentar mais uma vez.
                        print(f"[!] Resposta vazia da IA (Tentativa {attempt + 1})...")
                        continue
                        
                    return response.text.strip()

                except errors.ServerError as e:
                    # Erro 503 (Overload)
                    wait_time = (attempt + 1) * 3
                    print(f"[!] Servidor Sobrecarregado (503). Esperando {wait_time}s... ({e})")
                    time.sleep(wait_time)
                    
                except errors.ClientError as e:
                    # Erro 429 (Quota) ou outros erros de cliente
                    if "429" in str(e) or "QUOTA_EXCEEDED" in str(e).upper():
                        print(f"[!] Quota Excedida (429) na chave {self.current_key_index + 1}.")
                        break # Sai do loop de tentativas desta chave e rotaciona
                    else:
                        print(f"[!] Erro de API: {e}")
                        raise e
                except Exception as e:
                    print(f"[!] Erro inesperado na IA: {e}")
                    raise e
            
            # Se chegou aqui, a chave atual falhou em todas as tentativas ou deu 429
            print(f"[*] Rotacionando chave de API...")
            self._rotate_key()
            keys_tried += 1
            time.sleep(1) # Pequena pausa entre trocas de chave

        raise Exception("Todas as chaves de API falharam ou excederam a quota.")

    def interpret_instruction(self, instruction_text: str, doc_content: str = "") -> Intent:
        """
        Stage 1: Ingestion & Comprehension via Gemini.
        Returns mapped Intent object.
        """
        prompt = f"""
        # ATUE COMO SR. AI ENGINEER - EXTRAÇÃO DE ATRIBUTOS E BUNDLES DINÂMICOS (V2.2 - HOTFIX)
        
        Sua tarefa é extrair os dados necessários para uma proposta técnica, focando em quantidades, nuances de ação (como P2V vs Clean Install) e **VISIBILIDADE DO ESCOPO**.
        
        ## INPUTS
        1. **User Instruction (CLI):** "{instruction_text}"
        2. **Technical Context (PDF):** "{doc_content[:6000]}"
        
        ## DIRETRIZ MESTRA (PRIORIDADE)
        1. Se houver discrepância de QUANTIDADE entre o Texto Técnico (PDF) e a Instrução do Usuário (Instruction), a **Instrução do Usuário PREVALECE**. Ex: PDF diz 20, Usuário diz 'Considerar 26'. O output deve ser 26.
        2. A "User Instruction" tem PRIORIDADE ABSOLUTA sobre o "Technical Context".
        
        ## REGRAS DE EXTRAÇÃO
        1. **client_name / company_name:** Extraia da Instruction. Se não houver, tente no PDF.
        2. **hardware_supply_by_client:** Se a Instruction disser "Supply Only" ou "Cliente fornece hardware", defina como true. Default: false.
        3. **logistics**:
           - **travel_segments**: Array de dias por viagem. Extraia da Instruction. Default: [5].
           - **team_size**: Procure por número de técnicos/profissionais. Default: 1.
        4. **scope_items**: Extraia os itens de escopo como uma LISTA DE OBJETOS JSON.
           - Cada objeto DEVE ter:
             - "name": Nome conciso e técnico do item.
             - "detected_quantity": INTEIRO. Extraia do texto. **Siga a Diretriz Mestra de Prioridade**.
             - "action_type": Um dos valores: "install", "migrate_p2v", "supply_only", "turnkey", "design".
             - "context_note": Trecho curto justificando a classificação.
             - "visibility": "public" ou "internal".
               - **"internal"**: Se for item preparatório, curso, treinamento interno, ou planejamento prévio (ex: "Planejamento em Jundiaí", "Curso Hyper-V").
               - **"public"**: Itens de entrega final ao cliente.
             - "explicit_total_hours": INTEIRO (em Horas). Default: 0.
               - Extraia APENAS se a instrução der uma duração explícita para aquele item Específico.
               - Conversões: "30 dias" -> 240, "80 horas" -> 80.
             - "is_weekend": boolean.
               - True se a instrução mencionar que este item específico será feito no "final de semana", "sábado" ou "domingo". Default: false.
        5. **estimated_duration_weeks**: INTEIRO.
           - Estime baseado no cronograma descrito no PDF ou na Instruction (ex: "5 etapas", "30 dias" -> 4 semanas).
           - Se não houver informação clara, use o cálculo fallback: `soma dos travel_segments / 5` (dias úteis). Default: 1.
        6. **governance_level**: String: "standard" ou "intensive".
           - "intensive" se a Instruction pedir follow-up diário, acompanhamento próximo, ou se for um projeto crítico.
           - Default: "standard".
        
        ## FORMATO DE SAÍDA (JSON ESTRITO)
        {{
            "client_name": "String",
            "company_name": "String",
            "project_name": "String",
            "hardware_supply_by_client": boolean,
            "estimated_duration_weeks": int,
            "governance_level": "standard" | "intensive",
            "work_on_weekends": boolean,
            "scope_items": [
                {{
                    "name": "Nome do Item",
                    "detected_quantity": 26,
                    "action_type": "migrate_p2v",
                    "context_note": "Migração de servidores físicos para virtuais conforme solicitado",
                    "visibility": "public",
                    "explicit_total_hours": 0,
                    "is_weekend": false
                }},
                {{
                    "name": "Planejamento Inicial",
                    "detected_quantity": 1,
                    "action_type": "design",
                    "context_note": "30 dias de planejamento interno",
                    "visibility": "internal",
                    "explicit_total_hours": 240,
                    "is_weekend": false
                }}
            ],
            "logistics_override": {{
                "transport_provider": "client" | "provider",
                "consulting": boolean,
                "team_size": int,
                "travel_segments": [int, int, ...]
            }}
        }}

        ## INSTRUÇÕES ADICIONAIS
        - **work_on_weekends**: Defina como true se a instrução mencionar "considerar custos de finais-de-semana", "aproveitar finais-de-semana" ou termos similares que indiquem trabalho contínuo incluindo Sábados/Domingos.
        
        Responda APENAS com o JSON puro, sem markdown.
        """
        
        text = self.generate_content(prompt, temperature=0.1)
        
        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "")
        
        try:
            data = json.loads(text)
            return Intent(**data)
        except Exception as e:
            print(f"AI Parse Error: {e}. Raw: {text}")
            return Intent(
                client_name="Cliente Geral",
                company_name="Empresa Não Identificada",
                project_name="Projeto de Automação",
                scope_items=[],
                logistics_override={"transport_provider": "provider"}
            )

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
        1. **requires_flight**: True se a distância > 400km ou se for interestadual (exceto vizinhos próximos).
        2. **flight_region**: "flight_ne" (Nordeste/Norte/Centro-Oeste long) ou "flight_s_se" (Sul/Sudeste/Centro-Oeste close).
        3. **requires_car_rental**: True se precisar visitar locais (fábricas, clientes) no destino.
        4. **estimated_daily_km**: Média de deslocamento local. Default: 60km (Hotel <-> Fábrica).
        5. **requires_freight**: True se houver escopo de equipamentos pesados (racks, servidores, painéis) na Instrução.
        6. **hotel_tier**: "hotel_tier_capital" (Capitais) ou "hotel_tier_interior" (Cidades pequenas/Interior).
        7. **origin_mobilization_km**: Distância de mobilização terrestre inicial (ex: Jundiaí -> Aeroporto/Sede). 
           - Se a instrução mencionar "mobilização de Jundiaí" ou algo similar, calcule a distância estimada (padrão 50km). Senão 0.

        ## OUTPUT JSON FORMAT
        {{
            "requires_flight": true,
            "flight_region": "flight_ne",
            "requires_car_rental": true,
            "estimated_daily_km": 60,
            "requires_freight": false,
            "hotel_tier": "hotel_tier_capital",
            "origin_mobilization_km": 50.0
        }}
        
        Responda APENAS com o JSON.
        """
        
        text = self.generate_content(prompt, temperature=0.1)

        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "")
            
        try:
            data = json.loads(text)
            return LogisticsPlan(**data)
        except Exception as e:
            print(f"AI Logistics Parse Error: {e}. Raw: {text}")
            # Fallback seguro
            return LogisticsPlan(
                requires_flight=True,
                flight_region="flight_s_se",
                requires_car_rental=True,
                estimated_daily_km=50,
                hotel_tier="hotel_tier_capital"
            )
