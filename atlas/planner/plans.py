from dataclasses import dataclass
from typing import List

@dataclass
class ExecutionPlan:
    """Structured execution plan representing how to achieve a given Intent."""
    intent: str
    goal: str
    modules_required: List[str]
    execution_order: List[str]
    estimated_duration: str
    risk_level: str
    approval_required: bool
    rollback_strategy: str

    def to_dict(self) -> dict:
        """Serialize plan for programmatic consumption by future autonomous agents."""
        return {
            "intent": self.intent,
            "goal": self.goal,
            "modules_required": self.modules_required,
            "execution_order": self.execution_order,
            "estimated_duration": self.estimated_duration,
            "risk_level": self.risk_level,
            "approval_required": self.approval_required,
            "rollback_strategy": self.rollback_strategy
        }
