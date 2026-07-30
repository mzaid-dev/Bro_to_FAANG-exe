import json
from datetime import date
from typing import Literal
from pydantic import BaseModel , Field , ValidationError

# ==========================================
# 1. DEFINE & CONSTRAIN (The Application Schema)
# ==========================================
class ActionItem(BaseModel):
    task: str = Field(min_length=1) # Task cannot be empty
    owner: str | None = None        # Owner can be missing
    deadline: date | None = None    # Deadline can be missing

class MeetingExtraction(BaseModel):
    status: Literal["ok", "no_items"]
    action_items: list[ActionItem] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)  

# ==========================================
# 2. DOMAIN VALIDATION (Business Rules)
# ==========================================
def enforce_extraction_rules(result: MeetingExtraction) -> MeetingExtraction:
    # Rule 1: If status is no_items, there must be NO action items.
    if result.status == "no_items" and result.action_items:
        raise ValueError("Domain Error: A no_items result cannot contain action items.")
    
    # Rule 2: If status is ok, there must be at least ONE action item.
    if result.status == "ok" and not result.action_items:
        raise ValueError("Domain Error: An ok result must contain at least one action item.")
    
    return result

# ==========================================
# 3. PARSE & VALIDATE PIPELINE (The Guard)
# ==========================================
def process_model_output(raw_text: str):
    print("\n--- Processing New AI Output ---")
    try:
        # Step 1: Parse JSON (Syntax Check)
        payload = json.loads(raw_text)
        
        # Step 2: Schema Check (Pydantic)
        parsed = MeetingExtraction.model_validate(payload)
        
        # Step 3: Domain Check (Business Rules)
        final_result = enforce_extraction_rules(parsed)
        
        # Step 4: USE (Success!)
        print("✅ SUCCESS! Data accepted and safe to use.")
        print(final_result.model_dump_json(indent=2))
        
    except json.JSONDecodeError:
        print("❌ REJECTED: Syntax Error (AI gave bad JSON)")
    except ValidationError as e:
        print(f"❌ REJECTED: Schema Error (Wrong types or missing fields)\n{e}")
    except ValueError as e:
        print(f"❌ REJECTED: {e}")


# ==========================================
# 4. SIMULATE GENERATION (Testing 3 Cases)
# ==========================================
if __name__ == "__main__":
    
    # Case 1: Perfect Output
    good_output = '{"status": "ok", "action_items": [{"task": "Send report", "owner": "Ali", "deadline": "2026-08-01"}], "warnings": []}'
    
    # Case 2: Schema Error (Task is an empty string, which violates min_length=1)
    bad_schema_output = '{"status": "ok", "action_items": [{"task": "", "owner": "Ali"}], "warnings": []}'
    
    # Case 3: Domain Error (Status says no_items, but AI gave an action item - Contradiction!)
    bad_domain_output = '{"status": "no_items", "action_items": [{"task": "Send report"}], "warnings": []}'

    # Run all 3 cases
    process_model_output(good_output)
    process_model_output(bad_schema_output)
    process_model_output(bad_domain_output)