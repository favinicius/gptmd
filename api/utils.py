from pathlib import Path
from fastapi import UploadFile
import shutil
from typing import List

def save_upload_files(files: List[UploadFile], upload_dir: Path) -> List[str]:
    """Salva lista de UploadFile no diretório especificado e retorna caminhos absolutos."""
    saved_paths = []
    if not files:
        return saved_paths

    for file in files:
        # Sanitize filename if needed, but keeping simple for now
        file_path = upload_dir / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_paths.append(str(file_path.absolute()))
    
    return saved_paths

def sanitize_content(content: str, client_name: str) -> str:
    """Sanitizes content by replacing placeholders or sensitive info."""
    if not content: return ""
    # Basic replacement of common placeholders if any
    content = content.replace("[NOME_CLIENTE]", client_name)
    content = content.replace("[Client Name]", client_name)
    return content
