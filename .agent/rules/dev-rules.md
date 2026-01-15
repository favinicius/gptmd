---
trigger: always_on
---

# PROJECT DEVELOPMENT CONSTITUTION
The following rules are mandatory and must be adhered to without exception throughout the development lifecycle.

1. **NO SIMPLIFICATION (BUNDLE EXPLOSION):**
   You are STRICTLY PROHIBITED from removing or simplifying the "Bundle Explosion" (WBS) logic. Every single hardware item must ALWAYS instantiate a minimum of 5 sub-activities: 
   *   Receiving (Recebimento)
   *   Assembly (Montagem)
   *   Firmware Update (Firmware)
   *   Configuration (Configuração)
   *   Testing (Testes)

2. **EXPLICIT HOURS DISTRIBUTION RULE:**
   If the parameter `explicit_total_hours` is provided, it must NEVER cause the topic to collapse into a single line item. Instead, the provided hours must be **PROPORTIONALLY DISTRIBUTED** across the sub-activities of the corresponding bundle.

3. **LOGIC PRESERVATION:**
   Adjustments to the User Interface (UI) or output visibility must NEVER override, bypass, or alter the core mathematical logic defined in `calculator.py`. The backend calculation integrity is paramount.

4. **FILE NAMING CONVENTION:**
   All output files generated within a timestamped directory must include the specific timestamp string in their filenames. 
   *   *Example:* `MOD_20260115_1400.md`.

5. **AI MODEL GOVERNANCE:**
   The project must ALWAYS use the most advanced available models for extraction and planning. DO NOT downgrade models unless explicitly requested for cost-testing.
   *   **Production (Fast/Efficient):** `gemini-2.5-flash`
   *   **Production (Advanced Reasoning):** `gemini-2.5-pro`
   *   **Experimental/Cutting Edge:** `gemini-3-flash-preview` ou `gemini-3-pro-preview`.
   *   **Fallback (Stable):** `gemini-1.5-flash`.
   *   **Prohibition:** Avoid models older than 1.5 unless the user specifies. Any mention of "Gemini 2.x" or "Gemini 3.x" in the code must be preserved.