import os
import sys
from pathlib import Path
from src.ai_agent import AIAgent

def refactor_content(content: str, user_request: str, agent: AIAgent) -> str:
    """Uses AI to refactor the content based on user request."""
    prompt = f"""
    # ATUE COMO ESCRITOR TÉCNICO E ESPECIALISTA EM PROPOSTAS (V1.0)
    
    Sua tarefa é refatorar o conteúdo Markdown abaixo seguindo a instrução do usuário.
    
    ## CONTEÚDO ORIGINAL:
    {content}
    
    ## INSTRUÇÃO DE MELHORIA:
    "{user_request}"
    
    ## DIRETRIZES:
    1. Mantenha as variáveis Jinja2 (ex: `{{{{ client_name }}}}`) e Tags de imagem (ex: `[TAG: ...]`).
    2. Melhore a persuasão, clareza ou detalhamento conforme solicitado.
    3. Retorne APENAS o Markdown refatorado.
    """
    
    return agent.generate_content(prompt, temperature=0.2)

def main():
    if len(sys.argv) < 3:
        print("Uso: python3 src/tools/section_refactorer.py <caminho_do_bloco_md> '<instrução_de_melhoria>'")
        return

    block_path = Path(sys.argv[1])
    instruction = sys.argv[2]
    
    if not block_path.exists():
        print(f"Erro: Bloco {block_path} não encontrado.")
        return
        
    with open(block_path, "r", encoding="utf-8") as f:
        original_content = f.read()
        
    print(f"[*] Refatorando bloco: {block_path.parent.name}")
    agent = AIAgent()
    new_content = refactor_content(original_content, instruction, agent)
    
    # Criar backup antes de sobrescrever
    backup_path = block_path.with_suffix(".md.bak")
    with open(backup_path, "w", encoding="utf-8") as f:
        f.write(original_content)
        
    # Salvar nova versão
    with open(block_path, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    print(f"[+] Sucesso! Versão refatorada salva.")
    print(f"[*] Backup da versão anterior em: {backup_path}")

if __name__ == "__main__":
    main()
