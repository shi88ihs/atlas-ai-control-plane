from dataclasses import dataclass, field
from typing import List

@dataclass
class WorkflowStep:
    """Represents a single executable step in an Atlas Workflow."""
    step_number: int
    module: str
    objective: str
    prerequisites: List[str]
    approval_required: bool
    rollback_strategy: str
    verification_step: str
    estimated_duration: str

    def to_dict(self) -> dict:
        return {
            "step_number": self.step_number,
            "module": self.module,
            "objective": self.objective,
            "prerequisites": self.prerequisites,
            "approval_required": self.approval_required,
            "rollback_strategy": self.rollback_strategy,
            "verification_step": self.verification_step,
            "estimated_duration": self.estimated_duration
        }

@dataclass
class Workflow:
    """A generated workflow detailing how a plan will be executed."""
    workflow_id: str
    intent: str
    risk: str
    modules: List[str]
    steps: List[WorkflowStep]
    estimated_duration: str
    execution_state: str = "Generated"

    def to_dict(self) -> dict:
        return {
            "workflow_id": self.workflow_id,
            "intent": self.intent,
            "risk": self.risk,
            "modules": self.modules,
            "steps": [s.to_dict() for s in self.steps],
            "estimated_duration": self.estimated_duration,
            "execution_state": self.execution_state
        }
