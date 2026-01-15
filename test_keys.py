import re
import os

def test_regex():
    content = """
#fa.vinicius.bezerra@gmail.com
GEMINI_API_KEY-1=KEY_ONE

#fabio.bezerra@egesolucoes
GEMINI_API_KEY_2=KEY_TWO

#Nossa Grana
GEMINI_API_KEY=KEY_MAIN

#desenvolvimento@egesolucoes
#GEMINI_API_KEY_3=KEY_THREE
"""
    # Regex atualizada para ser mais precisa
    matches = re.findall(r"(?:#\s*)?(GEMINI_API_KEY[A-Za-z0-9_\-]*)\s*=\s*([A-Za-z0-9_-]+)", content)
    keys = []
    for var, val in matches:
        print(f"Encontrado: {var} -> {val}")
        if val not in keys:
            keys.append(val)
    print(f"Lista final: {keys}")

if __name__ == "__main__":
    test_regex()
