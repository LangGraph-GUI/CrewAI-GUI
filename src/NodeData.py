"""
Data models for the CrewAI-GUI node graph.
"""

from dataclasses import dataclass, asdict, field
from typing import List


@dataclass
class Serializable:
    """Mixin that adds ``to_dict`` / ``from_dict`` round-tripping."""

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


@dataclass
class NodeData(Serializable):
    """A single node in the visual workflow graph.

    Every node holds position, size, and type-specific configuration.
    Connection topology is stored via ``uniq_id`` references in ``prevs``
    (upstream nodes) and ``nexts`` (downstream nodes).
    """

    # Node type: "None", "Start", "Agent", "Task", "Step", "Team"
    type: str = ""

    # Tools assigned to this node's agent
    tools: List[str] = field(default_factory=list)

    # Unique identifier (string, not int — JSON keys are strings)
    uniq_id: str = ""

    # Position and size in the editor canvas
    pos_x: float = 0.0
    pos_y: float = 0.0
    width: float = 200.0
    height: float = 200.0

    # Display name
    name: str = ""

    # Agent configuration
    role: str = ""
    goal: str = ""
    backstory: str = ""

    # Task configuration
    agent: str = ""
    description: str = ""
    expected_output: str = ""

    # Step configuration
    tool: str = ""
    arg: str = ""
    output_var: str = ""

    # Graph topology — IDs are strings matching ``uniq_id``
    nexts: List[str] = field(default_factory=list)
    prevs: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
