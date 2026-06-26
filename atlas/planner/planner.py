from .intent import Intent
from .plans import ExecutionPlan

class AtlasPlanner:
    """The orchestration layer that maps Intents to structured ExecutionPlans."""
    
    def create_plan(self, intent_str: str) -> ExecutionPlan:
        try:
            intent = Intent(intent_str.lower())
        except ValueError:
            raise ValueError(f"Unsupported intent: {intent_str}")

        if intent == Intent.STABILIZE:
            return ExecutionPlan(
                intent=intent.value,
                goal="Assess state and ensure baseline stability.",
                modules_required=["Doctor", "Status", "Reports", "Git"],
                execution_order=["Doctor", "Status", "Auth Checks", "Reports", "Git Status"],
                estimated_duration="20 seconds",
                risk_level="Read-only",
                approval_required=True,
                rollback_strategy="None required"
            )
        elif intent == Intent.DOCTOR:
            return ExecutionPlan(
                intent=intent.value,
                goal="Run authentication and health checks.",
                modules_required=["Doctor"],
                execution_order=["Doctor"],
                estimated_duration="5 seconds",
                risk_level="Read-only",
                approval_required=False,
                rollback_strategy="None required"
            )
        elif intent == Intent.RELEASE:
            return ExecutionPlan(
                intent=intent.value,
                goal="Publish changes and tag a new release.",
                modules_required=["Status", "Doctor", "Git", "Reports"],
                execution_order=["Status", "Doctor", "Git Commit", "Git Push", "Reports"],
                estimated_duration="30 seconds",
                risk_level="Low (Reversible)",
                approval_required=True,
                rollback_strategy="Git revert to previous commit"
            )
        elif intent == Intent.DIAGNOSE:
            return ExecutionPlan(
                intent=intent.value,
                goal="Deep check of system state for troubleshooting.",
                modules_required=["Doctor", "Status", "Reports"],
                execution_order=["Doctor", "Status", "Log Analysis", "Reports"],
                estimated_duration="45 seconds",
                risk_level="Read-only",
                approval_required=False,
                rollback_strategy="None required"
            )
        # Generic fallback for other intents
        return ExecutionPlan(
            intent=intent.value,
            goal=f"Execute {intent.value} workflow.",
            modules_required=[intent.value.capitalize()],
            execution_order=[intent.value.capitalize()],
            estimated_duration="Unknown",
            risk_level="Unknown",
            approval_required=True,
            rollback_strategy="Manual intervention"
        )
