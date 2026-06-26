from .registry import ModuleRegistry, AtlasModule
from .config import config

# Central registry for all Atlas modules
registry = ModuleRegistry()

def bootstrap_registry():
    """Register initial Control Plane modules."""
    registry.register(AtlasModule(
        name="Doctor",
        version="1.0.0",
        description="Authentication and health checks",
        available_commands=["doctor"],
        health_status="Healthy",
        dependencies=[]
    ))
    registry.register(AtlasModule(
        name="Status",
        version="1.0.0",
        description="Runtime state collection and rendering",
        available_commands=["status", "collect"],
        health_status="Healthy",
        dependencies=[]
    ))
    registry.register(AtlasModule(
        name="Git",
        version="1.0.0",
        description="Git awareness and version control",
        available_commands=["git-status"],
        health_status="Healthy",
        dependencies=[]
    ))
    registry.register(AtlasModule(
        name="Reports",
        version="1.0.0",
        description="Markdown report generation",
        available_commands=["report"],
        health_status="Healthy",
        dependencies=[]
    ))
    registry.register(AtlasModule(
        name="Inventory",
        version="1.0.0",
        description="Tracked assets and endpoints",
        available_commands=[],
        health_status="Healthy",
        dependencies=[]
    ))
    registry.register(AtlasModule(
        name="Policies",
        version="1.0.0",
        description="Operational policies",
        available_commands=[],
        health_status="Healthy",
        dependencies=[]
    ))
    registry.register(AtlasModule(
        name="Playbooks",
        version="1.0.0",
        description="Automation playbooks",
        available_commands=[],
        health_status="Healthy",
        dependencies=[]
    ))
    registry.register(AtlasModule(
        name="Timeline",
        version="0.0.0",
        description="Event timeline (placeholder)",
        available_commands=[],
        health_status="Unknown",
        dependencies=[],
        status="Planned"
    ))
    registry.register(AtlasModule(
        name="Fleet",
        version="0.0.0",
        description="Fleet manager (placeholder)",
        available_commands=[],
        health_status="Unknown",
        dependencies=[],
        status="Planned"
    ))

# Initialize the core registry at load time
bootstrap_registry()
