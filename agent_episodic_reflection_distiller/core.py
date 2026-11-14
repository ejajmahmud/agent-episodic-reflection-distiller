"""Core episodic reflection distiller implementation."""
from typing import List, Dict, Any, Optional

class RuleExtraction:
    def __init__(self, condition: str, recommendation: str, confidence: float):
        self.condition = condition
        self.recommendation = recommendation
        self.confidence = confidence

    def to_dict(self) -> Dict[str, Any]:
        return {
            "condition": self.condition,
            "recommendation": self.recommendation,
            "confidence": self.confidence
        }

class TrajectorySummary:
    def __init__(self, session_id: str, success: bool, steps: List[str], error_message: Optional[str] = None):
        self.session_id = session_id
        self.success = success
        self.steps = steps
        self.error_message = error_message

class ReflectionDistiller:
    def __init__(self):
        self.rulebook: List[RuleExtraction] = []

    def distill(self, trajectories: List[TrajectorySummary]) -> List[RuleExtraction]:
        extracted = []
        for t in trajectories:
            if not t.success and t.error_message:
                err = t.error_message.lower()
                if "port" in err and "already in use" in err:
                    r = RuleExtraction(
                        condition="bind_failure_port_in_use",
                        recommendation="Check and terminate conflicting zombie process before bind",
                        confidence=0.95
                    )
                    extracted.append(r)
                elif "permission" in err or "access denied" in err:
                    r = RuleExtraction(
                        condition="permission_denied",
                        recommendation="Verify filesystem write permissions and chmod flags",
                        confidence=0.90
                    )
                    extracted.append(r)
                else:
                    r = RuleExtraction(
                        condition=f"error_{err[:20].strip().replace(' ', '_')}",
                        recommendation=f"Review input parameters for {t.steps[-1] if t.steps else 'step'}",
                        confidence=0.70
                    )
                    extracted.append(r)

        self.rulebook.extend(extracted)
        return extracted
