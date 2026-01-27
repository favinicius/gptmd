
import requests
import os

BASE_URL = "http://localhost:8000"

def test_health():
    print("Testing /health...")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ Backend is up (Docs accessible)")
        else:
            print(f"❌ Backend returned {response.status_code}")
    except Exception as e:
        print(f"❌ Could not connect to backend: {e}")

def test_history():
    print("\nTesting /history...")
    try:
        response = requests.get(f"{BASE_URL}/history")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ History fetched. Items: {len(data)}")
        else:
            print(f"❌ History failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Could not connect to backend: {e}")


def test_generation():
    print("\nTesting /generate (Mock)...")
    try:
        # Mock payload
        payload = {
            "instruction": "Cliente: Acme Corp. Contato: John Doe. Projeto: Migração de Servidores. Preciso de uma cotação para 2 servidores Dell PowerEdge R750 para virtualização.",
            "sizing": "standard",
            "contingency": "standard",
            "term": "30",
            "output_mode": "unified",
            "separate_opex": "false"
        }
        # We need to send a dummy file because the API expects UploadFile list, 
        # but it defaults to None in the signature? 
        # Let's check api/main.py signature again. 
        # It says files: List[UploadFile] = File(None). So it is optional.
        
        response = requests.post(f"{BASE_URL}/generate", data=payload)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Generation successful!")
            print(f"   Status: {result.get('status')}")
            print(f"   Files generated: {len(result.get('files', []))}")
        else:
            print(f"❌ Generation failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Could not connect to backend: {e}")

if __name__ == "__main__":
    test_health()
    test_history()
    test_generation()
