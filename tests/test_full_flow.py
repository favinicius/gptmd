
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_full_flow():
    print("🚀 Starting Full HITL Flow Test...")
    
    # 1. Analyze
    print("\n[Step 1] Initializing Analysis...")
    instruction = "Cliente: Indústria XYZ. Projeto: Modernização de Rede. Preciso de 2 switches e 1000m de cabo óptico."
    
    # Use dummy file content if needed, but ContextLoader handles empty fine
    # For now, let's send just instruction
    try:
        resp = requests.post(f"{BASE_URL}/analyze", data={"instruction": instruction})
        if resp.status_code != 200:
            print(f"❌ Analysis failed: {resp.text}")
            return
        intent = resp.json()
        print(f"✅ Analysis OK. Items: {len(intent.get('scope_items', []))}")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        return

    # Mock User Validation (Scope is fine)
    
    # 2. Logistics Plan
    print("\n[Step 2] Planning Logistics...")
    try:
        resp = requests.post(f"{BASE_URL}/plan-logistics", json=intent)
        if resp.status_code != 200:
            print(f"❌ Logistics Plan failed: {resp.text}")
            return
        log_plan = resp.json()
        print(f"✅ Logistics Plan OK. Flight: {log_plan.get('requires_flight')}")
        
        # Update Intent with detailed logistiics
        intent["detailed_logistics"] = log_plan
        # Also need logistics_override? Pricing engine looks at detailed_logistics for calculation of LOG-MOB items?
        # Actually LaborEngine CalculateLogistics uses intent.logistics_override OR detailed_logistics?
        # Let's check LaborEngine.
        # It uses intent.logistics_override to set team size, but detailed_logistics for flight costs etc?
        # Re-reading LaborEngine: _calculate_logistics_mirroring uses intent.logistics_override.
        # LogisticsEngine.calculate_logistics uses intent.
    except Exception as e:
        print(f"❌ Logistics Error: {e}")
        return

    # 3. Pricing
    print("\n[Step 3] Calculating Pricing...")
    try:
        resp = requests.post(f"{BASE_URL}/pricing", json=intent)
        if resp.status_code != 200:
            print(f"❌ Pricing failed: {resp.text}")
            return
        proposal = resp.json()
        print(f"✅ Pricing OK. Grand Total: {proposal.get('grand_total_venda')}")
    except Exception as e:
        print(f"❌ Pricing Error: {e}")
        return

    # 4. Redaction
    print("\n[Step 4] Generating Texts...")
    try:
        req_redaction = {"intent": intent, "proposal": proposal}
        resp = requests.post(f"{BASE_URL}/redaction", json=req_redaction)
        if resp.status_code != 200:
             # Fallback retry logic might be needed here or in app
            print(f"❌ Redaction failed: {resp.text}")
            # Mock redaction for assembly if fail
            text_blocks = {}
        else:
            text_blocks = resp.json()
            print(f"✅ Redaction OK. Blocks: {len(text_blocks)}")
    except Exception as e:
        print(f"❌ Redaction Error: {e}")
        text_blocks = {}

    # 5. Assemble
    print("\n[Step 5] Assembling Final Files...")
    try:
        req_assemble = {
            "intent": intent, 
            "proposal": proposal,
            "text_blocks": text_blocks
        }
        resp = requests.post(f"{BASE_URL}/assemble", json=req_assemble)
        if resp.status_code != 200:
            print(f"❌ Assembly failed: {resp.text}")
            return
        result = resp.json()
        print(f"✅ Assembly OK. Output: {result.get('output_dir')}")
        print(f"   Files: {len(result.get('files', []))}")
    except Exception as e:
        print(f"❌ Assembly Error: {e}")
        return

if __name__ == "__main__":
    test_full_flow()
