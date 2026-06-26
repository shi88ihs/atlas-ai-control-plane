from pathlib import Path

class AtlasConfig:
    """Central Atlas configuration object."""
    def __init__(self):
        self.root_dir = Path(__file__).resolve().parents[1]
        self.scripts_dir = self.root_dir / "scripts"
        self.reports_dir = self.root_dir / "reports"
        self.inventory_dir = self.root_dir / "inventory"
        self.policies_dir = self.root_dir / "policies"
        self.playbooks_dir = self.root_dir / "playbooks"

config = AtlasConfig()
