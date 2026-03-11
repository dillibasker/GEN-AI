"""
Shared A2A Protocol Models
Defines all data structures used in Agent-to-Agent communication.
"""

from dataclasses import dataclass, field
from typing import Any, Optional
from enum import Enum
import uuid
import time


class TaskState(str, Enum):
    SUBMITTED = "submitted"
    WORKING = "working"
    COMPLETED = "completed"
    FAILED = "failed"
    REJECTED = "rejected"


class MessageRole(str, Enum):
    USER = "user"
    AGENT = "agent"


@dataclass
class Skill:
    """Represents a capability that an agent can perform."""
    id: str
    name: str
    description: str
    tags: list[str] = field(default_factory=list)
    examples: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "examples": self.examples,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Skill":
        return cls(**data)


@dataclass
class AgentCard:
    """
    Agent Card — the metadata document exposed by every A2A server agent.
    Agent-1 reads this to discover Agent-2's capabilities before delegating.
    """
    name: str
    description: str
    version: str
    url: str
    skills: list[Skill] = field(default_factory=list)
    supports_streaming: bool = False
    protocol_version: str = "1.0"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "url": self.url,
            "protocol_version": self.protocol_version,
            "supports_streaming": self.supports_streaming,
            "skills": [s.to_dict() for s in self.skills],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AgentCard":
        skills = [Skill.from_dict(s) for s in data.get("skills", [])]
        return cls(
            name=data["name"],
            description=data["description"],
            version=data["version"],
            url=data["url"],
            skills=skills,
            supports_streaming=data.get("supports_streaming", False),
            protocol_version=data.get("protocol_version", "1.0"),
        )


@dataclass
class Message:
    """A single message in a Task conversation."""
    role: MessageRole
    content: str
    timestamp: float = field(default_factory=time.time)
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict:
        return {
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp,
            "message_id": self.message_id,
        }


@dataclass
class Artifact:
    """A produced output artifact (e.g., generated code)."""
    artifact_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    content: str = ""
    mime_type: str = "text/plain"
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "artifact_id": self.artifact_id,
            "name": self.name,
            "content": self.content,
            "mime_type": self.mime_type,
            "metadata": self.metadata,
        }


@dataclass
class Task:
    """
    Core A2A unit of work sent from Client Agent → Server Agent.
    """
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    state: TaskState = TaskState.SUBMITTED
    messages: list[Message] = field(default_factory=list)
    artifacts: list[Artifact] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "session_id": self.session_id,
            "state": self.state.value,
            "messages": [m.to_dict() for m in self.messages],
            "artifacts": [a.to_dict() for a in self.artifacts],
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclass
class A2ARequest:
    """The envelope sent over the wire from Agent-1 to Agent-2."""
    method: str          # e.g. "tasks/send"
    task: Task
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict:
        return {
            "jsonrpc": "2.0",
            "method": self.method,
            "id": self.request_id,
            "params": self.task.to_dict(),
        }


@dataclass
class A2AResponse:
    """The envelope returned by Agent-2 to Agent-1."""
    request_id: str
    task: Optional[Task] = None
    error: Optional[dict] = None

    def to_dict(self) -> dict:
        base = {"jsonrpc": "2.0", "id": self.request_id}
        if self.error:
            base["error"] = self.error
        else:
            base["result"] = self.task.to_dict() if self.task else {}
        return base
