
import requests
import json

BASE_URL = "http://localhost:8000"

def test_analyze():
    print("Testing /analyze endpoint...")
    
    instruction = "Cliente: Acme Inc. Projeto: Migração Azure. Preciso de 5 servidores físicos para banco de dados e 2 storages."
    
    try:
        response = requests.post(
            f"{BASE_URL}/analyze",
            data={"instruction": instruction}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ /analyze Success!")
            print(f"   Client: {data.get('client_name')}")
            print(f"   Items Detected: {len(data.get('scope_items', []))}")
            for item in data.get('scope_items', []):
                print(f"     - [{item.get('detected_quantity')}] {item.get('name')} ({item.get('action_type')})")
        else:
            print(f"❌ /analyze Failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    test_analyze()
