from .workflow import WorkflowStep

class ApprovalManager:
    """Manages approval state and constraints for workflow steps."""
    
    def requires_approval(self, step: WorkflowStep) -> bool:
        """Check if a step requires human/external approval before execution."""
        return step.approval_required

    def request_approval(self, step: WorkflowStep) -> bool:
        """
        Stub for requesting external approval.
        In the future, this will hook into Telegram/Slack or CLI prompts.
        """
        return False
