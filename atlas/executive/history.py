import json
import time
from pathlib import Path
from atlas.config import config
from .workflow import Workflow

class WorkflowHistory:
    """Records generated workflows for auditing and future execution tracking."""
    
    def __init__(self):
        self.history_dir = config.root_dir / "logs"
        self.history_dir.mkdir(exist_ok=True)
        self.history_file = self.history_dir / "workflow_history.json"
        if not self.history_file.exists():
            self.history_file.write_text("[]")

    def record(self, workflow: Workflow) -> None:
        """Append a newly generated workflow to the history log."""
        record_entry = {
            "timestamp": time.time(),
            "workflow_id": workflow.workflow_id,
            "intent": workflow.intent,
            "risk": workflow.risk,
            "modules": workflow.modules,
            "execution_state": workflow.execution_state
        }
        
        try:
            with open(self.history_file, "r") as f:
                history = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            history = []
            
        history.append(record_entry)
        
        with open(self.history_file, "w") as f:
            json.dump(history, f, indent=2)
