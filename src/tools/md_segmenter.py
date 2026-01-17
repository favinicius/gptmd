import os
import sys
import re
import json
from pathlib import Path
from src.ai_agent import AIAgent

def identify_sections(md_content: str) -> list:
    """Splits MD content into sections based on ## headers."""
    sections = []
    current_section = {"title": "Capa", "content": ""}
    
    lines = md_content.split('\n')
    for line in lines:
        if line.startswith('## '):
            sections.append(current_section)
            title = line.replace('## ', '').strip().lower().replace(' ', '_')
            # Remove characters like 1.1, 10., etc from start
            title = re.sub(r'^[\d.]+[\s.]+', '', title)
            current_section = {"title": title, "content": line + "\n"}
        else:
            current_section["content"] += line + "\n"
    
    sections.append(current_section)
    return sections

def templatify_block(content: str, agent: AIAgent) -> str:
    """Uses AI to replace specific data with Jinja2 placeholders in a single block."""
    prompt = f"""
    # ATUE COMO ARQUITETO DE TEMPLATES (V1.0)
    
    Converta o conteúdo Markdown abaixo em um template JINJA2 genérico.
    
    ## DIRETRIZES:
    1. **VARIAVÉIS JINJA2:** Substitua dados específicos por:
       - `{{{{ client_name }}}}` para o nome do cliente.
       - `{{{{ project_name }}}}` para o nome do projeto.
       - `{{{{ date }}}}` para datas.
       - `{{{{ proposal_ref }}}}` para números de referência.
       - `{{{{ company_name }}}}` para a empresa (EGE ou OFI).
       - `{{{{ city }}}}` e `{{{{ state }}}}` para localidade.
    2. **ESTRUTURA:** Mantenha todo o Markdown original, apenas troque os nomes próprios por variáveis.
    
    ## CONTEÚDO:
    {content}
    
    Responda APENAS com o conteúdo Markdown templatizado.
    """
    return agent.generate_content(prompt, temperature=0.1)

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 src/tools/md_segmenter.py <caminho_do_md>")
        return

    md_path = sys.argv[1]
    source_name = Path(md_path).stem
    
    if not os.path.exists(md_path):
        print(f"Erro: Arquivo {md_path} não encontrado.")
        return
        
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()
        
    print(f"[*] Identificando seções em: {md_path}")
    sections = identify_sections(md_content)
    
    agent = AIAgent()
    library_path = Path("templates/library")
    
    print(f"[*] Processando {len(sections)} seções...")
    for section in sections:
        title = section["title"]
        content = section["content"].strip()
        
        if not content:
            continue
            
        print(f"  [>] Templatizando secao: {title}")
        templated_content = templatify_block(content, agent)
        
        section_dir = library_path / title
        section_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = section_dir / f"{source_name}.md"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(templated_content)
        
    print("[+] Processo concluído.")

if __name__ == "__main__":
    main()
