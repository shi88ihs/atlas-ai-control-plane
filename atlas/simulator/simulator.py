import time
from pathlib import Path
from atlas.config import config
from atlas.planner.planner import AtlasPlanner
from atlas.executive.executive import AtlasExecutive
from atlas.simulator.scenarios import get_scenario_impact

class AtlasSimulator:
    def __init__(self):
        self.planner = AtlasPlanner()
        self.executive = AtlasExecutive()
        
    def simulate(self, intent_str: str) -> dict:
        plan = self.planner.create_plan(intent_str)
        workflow = self.executive.generate_workflow(plan)
        impact = get_scenario_impact(intent_str)
        
        result = {
            "intent": workflow.intent,
            "goal": plan.goal,
            "modules": workflow.modules,
            "files_touched": impact["files"],
            "services_affected": impact["services"],
            "risk_level": workflow.risk,
            "approval_required": any(step.approval_required for step in workflow.steps),
            "rollback_strategy": plan.rollback_strategy,
            "steps": workflow.steps
        }
        
        self._write_reports(result)
        return result
        
    def _write_reports(self, result: dict):
        timestamp = int(time.time())
        report_content = f"# Atlas Simulation Report: {result['intent']}\n\n"
        report_content += f"**Goal**: {result['goal']}\n"
        report_content += f"**Risk Level**: {result['risk_level']}\n"
        report_content += f"**Approval Required**: {result['approval_required']}\n"
        report_content += f"**Rollback Strategy**: {result['rollback_strategy']}\n\n"
        
        report_content += "## Modules Involved\n"
        for m in result['modules']:
            report_content += f"- {m}\n"
            
        report_content += "\n## Files Touched\n"
        for f in result['files_touched']:
            report_content += f"- {f}\n"
        if not result['files_touched']:
            report_content += "- None\n"
            
        report_content += "\n## Services Affected\n"
        for s in result['services_affected']:
            report_content += f"- {s}\n"
        if not result['services_affected']:
            report_content += "- None\n"
            
        report_content += "\n## Workflow Steps\n"
        for step in result['steps']:
            report_content += f"**Step {step.step_number}**: {step.module}\n"
            report_content += f"- Objective: {step.objective}\n"
            report_content += f"- Approval: {'Required' if step.approval_required else 'Not required'}\n"
        
        config.reports_dir.mkdir(exist_ok=True)
        latest = config.reports_dir / "latest-simulation-report.md"
        ts_report = config.reports_dir / f"simulation-{timestamp}.md"
        
        latest.write_text(report_content)
        ts_report.write_text(report_content)
