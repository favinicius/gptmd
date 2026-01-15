import os
from pathlib import Path
from pypdf import PdfReader
from typing import List
import logging

logging.getLogger("pypdf").setLevel(logging.ERROR)

class ContextLoader:
    def __init__(self, docs_path: str = "input/docs", style_path: str = "input/style"):
        self.docs_path = Path(docs_path)
        self.style_path = Path(style_path)

    def _read_pdf_text(self, pdf_path: Path) -> str:
        """Extrai texto de um arquivo PDF."""
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += (page.extract_text() or "") + "\n"
            return text
        except Exception as e:
            print(f"Erro ao ler PDF {pdf_path}: {e}")
            return ""
        
        if not text.strip():
            print(f"\n[WARNING] O PDF {pdf_path.name} retornou texto vazio. Possível necessidade de OCR ou arquivo corrompido.")
            
        return text

    def _read_file_content(self, file_path: Path) -> str:
        """Lê o conteúdo de um arquivo (PDF, TXT ou MD)."""
        if not file_path.exists():
            print(f"Arquivo não encontrado: {file_path}")
            return ""
        
        if file_path.suffix.lower() == ".pdf":
            return self._read_pdf_text(file_path)
        elif file_path.suffix.lower() in [".txt", ".md"]:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                print(f"Erro ao ler arquivo {file_path}: {e}")
                return ""
        return ""

    def load_technical_docs(self) -> str:
        """Lê os documentos técnicos (arquivo ou pasta)."""
        if self.docs_path.is_file():
            content = self._read_file_content(self.docs_path)
            print(f"Lendo PDF Técnico... ({len(content)} caracteres extraídos)")
            return content
            
        combined_text = ""
        if self.docs_path.exists() and self.docs_path.is_dir():
            files = sorted(self.docs_path.glob("*"))
            if files:
                for file in files:
                    if file.suffix.lower() in [".pdf", ".txt", ".md"]:
                        content = self._read_file_content(file)
                        print(f"Lendo PDF Técnico: {file.name} ({len(content)} caracteres extraídos)")
                        combined_text += f"\n--- Documento: {file.name} ---\n"
                        combined_text += content
            else:
                print("[WARNING] Pasta de documentos técnicos vazia.")
        return combined_text

    def load_style_guide(self) -> str:
        """Lê o guia de estilo (arquivo ou pasta)."""
        if self.style_path.is_file():
            content = self._read_file_content(self.style_path)
            print(f"Lendo PDF de Estilo... ({len(content)} caracteres extraídos)")
            return content

        combined_text = ""
        if self.style_path.exists() and self.style_path.is_dir():
            for file in sorted(self.style_path.glob("*")):
                if file.suffix.lower() in [".pdf", ".txt", ".md"]:
                    content = self._read_file_content(file)
                    print(f"Lendo PDF de Estilo: {file.name} ({len(content)} caracteres extraídos)")
                    combined_text += f"\n--- Estilo: {file.name} ---\n"
                    combined_text += content
        return combined_text
