import uuid
from typing import List
from atlas.planner.plans import ExecutionPlan
from atlas.executive.workflow import Workflow, WorkflowStep
from atlas.executive.history import WorkflowHistory

history_manager = WorkflowHistory()

class AtlasExecutive:
    """
    Atlas Executive is the bridge between planning and execution.
    It takes an approved ExecutionPlan and builds a detailed, ordered Workflow.
    It does NOT execute the workflow directly.
    """
    
    def generate_workflow(self, plan: ExecutionPlan) -> Workflow:
        workflow_id = f"wf-{uuid.uuid4().hex[:8]}"
        
        steps = []
        for i, module_str in enumerate(plan.execution_order, 1):
            # Map planner abstract steps to concrete workflow modules
            module_name = module_str
            objective = f"Execute {module_name} tasks"
            approval = False
            
            if module_str == "Doctor":
                objective = "Verify current health"
            elif module_str == "Status":
                objective = "Generate live report"
            elif module_str in ["Auth Checks", "Authentication Checks", "Authentication"]:
                module_name = "Authentication"
                objective = "Verify Google ADC"
            elif module_str in ["Git Status", "Git"]:
                module_name = "Git"
                objective = "Verify clean working tree"
            elif module_str == "Reports":
                module_name = "Reports"
                objective = "Generate operational summary"
                approval = True
            elif module_str == "Git Commit":
                objective = "Stage and commit changes"
            elif module_str == "Git Push":
                objective = "Push to upstream remote"
                approval = True
            elif module_str == "Log Analysis":
                objective = "Analyze current logs"
            
            step = WorkflowStep(
                step_number=i,
                module=module_name,
                objective=objective,
                prerequisites=[],
                approval_required=approval,
                rollback_strategy=plan.rollback_strategy,
                verification_step="Check step exit code",
                estimated_duration="Unknown"
            )
            steps.append(step)
            
        wf = Workflow(
            workflow_id=workflow_id,
            intent=plan.intent,
            risk=plan.risk_level,
            modules=plan.modules_required,
            steps=steps,
            estimated_duration=plan.estimated_duration,
            execution_state="Generated"
        )
        
        # Record the generated workflow to history
        history_manager.record(wf)
        return wf
