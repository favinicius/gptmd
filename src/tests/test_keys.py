import sys
from pathlib import Path

# Adiciona raiz do projeto ao path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.ai_agent import AIAgent

def test_key_priority():
    print("--- 🔐 Teste de Prioridade e Segurança de Chaves ---")
    
    try:
        # Inicializa o agente (vai carregar carregar do .env e rodar _select_best_key)
        agent = AIAgent()
        current = agent.current_key
        
        if not current:
            print("❌ ERRO: Nenhuma chave foi carregada.")
            return

        # Mascaramento seguro para exibição
        masked = f"{current[:8]}...{current[-4:]}"
        
        # Identificação do Tier
        is_paid = current == agent.paid_key
        tier = "PAID 💰" if is_paid else "FREE 🆓"
        
        print(f"Chave Selecionada: {masked}")
        print(f"Tier Atual:      {tier}")
        print(f"Total Free Keys: {len(agent.free_keys)}")
        print(f"Paid Key Config: {'Sim' if agent.paid_key else 'Não'}")
        
        # Validação da Lógica
        if agent.free_keys and is_paid:
            print("\n⚠️  AVISO: O sistema escolheu a chave PAGA, mas existem chaves FREE configuradas.")
            print("   Motivo provável: As chaves Free podem estar em Cooldown ou marcadas como Inválidas.")
        elif agent.free_keys and not is_paid:
            print("\n✅ SUCESSO: O sistema priorizou corretamente uma chave FREE.")
        elif not agent.free_keys:
            print("\nℹ️  INFO: Apenas chave Paga disponível (ou nenhuma Free configurada).")

        # Teste Real de Conexão
        print("\n--- 📡 Teste de Conectividade (Ping) ---")
        print("Enviando prompt de teste para o Gemini...")
        try:
            response = agent.generate_content("Responda apenas com a palavra: CONECTADO", max_output_tokens=10)
            print(f"Resposta da API: {response.strip()}")
        except Exception as e:
            print(f"❌ Falha na conexão: {e}")

    except Exception as e:
        print(f"❌ Erro Crítico durante o teste: {e}")

if __name__ == "__main__":
    test_key_priority()
