import os
import re
from pathlib import Path

library_dir = Path("templates/library")

def clean_block(content):
    # Remove # 11. ... and # 12. ... if they appear at the end of a block
    content = re.split(r'\n# \d+\.', content)[0]
    # Remove redundant ## wrappers if they were inside # (md_segmenter artifact)
    # Actually, keep ## but ensure they are consistent level
    return content.strip()

for root, dirs, files in os.walk(library_dir):
    for file in files:
        if file.endswith(".md"):
            path = Path(root) / file
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            cleaned = clean_block(content)
            
            if cleaned != content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(cleaned)
                print(f"Cleaned {path}")
