print("Teste de Execucao")
import os
from pathlib import Path
print(f"CWD: {os.getcwd()}")
print(f"Library exists: {Path('templates/library').exists()}")
from src.models import ProposalData
print("Import Models OK")
