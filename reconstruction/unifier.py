# reconstruction/unifier.py

def unify_results(shared_state):
    """
    Merge:
    - matched rules
    - violations
    - explanations
    - severity
    - confidence
    - rewrites
    Into ONE unified structure.
    """

    violations = shared_state.get("violations", [])
    explanations = shared_state.get("explanations", {})
    rewrites = shared_state.get("rewrite_suggestions", [])
    confidences = shared_state.get("confidence_scores", {})

    # ---------------------------------------------------------
    # 🔧 PATCH: Normalize confidence_scores into key=(rule_id, section)
    # ---------------------------------------------------------
    normalized_conf = {}

    # confidences currently looks like:
    # { "R1": [ {"section": "...", "confidence": 0.87}, ... ], ... }

    for rule_id, entries in confidences.items():
        for entry in entries:
            section = entry.get("section")
            score = entry.get("confidence", 0.0)
            normalized_conf[(rule_id, section)] = score

    confidences = normalized_conf
    # ---------------------------------------------------------

    # Convert rewrites list into dict for quick lookup
    rewrite_map = {
        (r["rule_id"], r["original"]): r["rewrite"]
        for r in rewrites
    }

    unified = []

    for v in violations:
        rule_id = v.get("rule_id")
        section = v.get("section")

        # Find explanation (list under rule_id)
        rule_expls = explanations.get(rule_id, [])
        explanation_text = "(no explanation found)"

        for e in rule_expls:
            if e["section"] == section:
                explanation_text = e["explanation"]
                break

        # 🔍 Confidence score lookup AFTER normalization
        confidence = confidences.get((rule_id, section), 0.0)

        # Rewrite suggestion lookup
        rewrite_text = rewrite_map.get((rule_id, section), None)

        unified.append({
            "rule_id": rule_id,
            "rule_text": v.get("rule_text"),
            "section": section,
            "status": v.get("status", "Violation"),
            "evidence": v.get("evidence", ""),
            "explanation": explanation_text,
            "severity": v.get("severity", "Medium"),
            "confidence": confidence,
            "rewrite": rewrite_text
        })

    return unified
