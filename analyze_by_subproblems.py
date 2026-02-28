import json

def parse_subproblems(sub_json_str: str) -> list:
    """
    Reconstructed missing function for the reproducibility assignment.
    The original authors forgot to commit 'analyze_by_subproblems.py' to their repository.
    
    This function parses the JSON string output from the Subproblem Agent
    and extracts the SQL clauses needed for the query plan.
    """
    try:
        data = json.loads(sub_json_str)
        clauses = []
        # The prompt specifies returning: { "subproblems": [ { "clause": "SELECT", ... } ] }
        for sub in data.get("subproblems", []):
            clause = sub.get("clause")
            if clause:
                clauses.append(clause.upper().strip())
        return clauses
    except json.JSONDecodeError:
        print("[Warning] Failed to decode subproblem JSON.")
        return []
    except Exception as e:
        print(f"[Warning] Error parsing subproblems: {e}")
        return []