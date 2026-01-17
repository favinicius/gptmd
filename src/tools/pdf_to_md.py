import os
import sys
import re
from pathlib import Path
import pypdf
from src.ai_agent import AIAgent

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts raw text from PDF using pypdf."""
    try:
        reader = pypdf.PdfReader(pdf_path)
        full_text = []
        for page in reader.pages:
            full_text.append(page.extract_text())
        return "\n---PAGE_BREAK---\n".join(full_text)
    except Exception as e:
        print(f"Erro ao ler PDF {pdf_path}: {e}")
        return ""

def convert_to_md(raw_text: str, agent: AIAgent) -> str:
    """Uses AIAgent to convert raw text to clean Markdown."""
    prompt = f"""
    # ATUE COMO ESPECIALISTA EM DOCUMENTAÇÃO TÉCNICA (V1.0)
    
    Sua tarefa é converter o texto bruto extraído de uma proposta em PDF para um formato Markdown (.md) limpo e profissional.
    
    ## DIRETRIZES:
    1. **REMOVA RUÍDOS:** Ignore números de página, cabeçalhos e rodapés repetitivos.
    2. **ESTRUTURA DE HEADERS:** Identifique títulos e subtítulos e use `#`, `##`, `###` apropriadamente.
    3. **PLACEHOLDERS DE IMAGEM (CRÍTICO):** Identifique locais onde o texto sugere a existência de uma imagem, diagrama, planta de layout, foto ou mapa. 
       - Insira um placeholder no formato: `[TAG: IMAGEM_DESCRIÇÃO_CURTA]` (ex: `[TAG: DIAGRAMA_REDE_OT]`, `[TAG: FOTO_RACK_DATACENTER]`).
       - Faça isso sempre que o texto mencionar "conforme figura", "veja no diagrama", "imagem abaixo", ou quando houver uma quebra de assunto onde um visual faria sentido.
    4. **TABELAS:** Formate listas de preços ou cronogramas como tabelas Markdown.
    5. **PRESERVE O CONTEÚDO:** Não resuma nem altere o texto original, apenas o formate para MD.
    6. **VARIÁVEIS:** Identifique elementos personalizados (Cliente, Data, Valores) e os mantenha como estão.
    
    ## TEXTO BRUTO (PDF EXTRACTION):
    {raw_text[:20000]} # Limitando para não estourar o contexto, embora Gemini suporte mais.
    
    Responda APENAS com o conteúdo em Markdown.
    """
    
    return agent.generate_content(prompt, temperature=0.1)

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 src/tools/pdf_to_md.py <caminho_do_pdf> [output_dir]")
        return

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "templates/extracted"
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"[*] Processando: {pdf_path}")
    raw_text = extract_text_from_pdf(pdf_path)
    
    if not raw_text:
        print("[-] Falha na extração de texto.")
        return
        
    print("[*] Convertendo para Markdown via AI...")
    agent = AIAgent()
    md_content = convert_to_md(raw_text, agent)
    
    file_name = Path(pdf_path).stem + ".md"
    final_path = output_path / file_name
    
    with open(final_path, "w", encoding="utf-8") as f:
        f.write(md_content)
        
    print(f"[+] Sucesso! Arquivo salvo em: {final_path}")

if __name__ == "__main__":
    main()
