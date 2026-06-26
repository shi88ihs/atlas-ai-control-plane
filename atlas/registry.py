from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class AtlasModule:
    """Represents a registered Atlas Control Plane module."""
    name: str
    version: str
    description: str
    available_commands: List[str]
    health_status: str
    dependencies: List[str]
    status: str = "Loaded"  # E.g., "Loaded" or "Planned"

class ModuleRegistry:
    """Maintains a registry of Atlas modules."""
    def __init__(self):
        self._modules: Dict[str, AtlasModule] = {}

    def register(self, module: AtlasModule) -> None:
        """Register a new module."""
        self._modules[module.name] = module

    def get_module(self, name: str) -> AtlasModule:
        """Retrieve a specific module."""
        return self._modules.get(name)

    def list_modules(self) -> List[AtlasModule]:
        """List all registered modules."""
        return list(self._modules.values())
