from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Task:
    name: str
    duration_minutes: int
    priority: Priority
    task_type: str
    preferred_time: Optional[str] = None

    def is_high_priority(self) -> bool:
        ...

    def __repr__(self) -> str:
        ...


@dataclass
class Pet:
    name: str
    species: str
    age: int
    health_notes: str = ""
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        ...

    def remove_task(self, name: str) -> None:
        ...

    def list_tasks(self) -> list[Task]:
        ...


@dataclass
class Owner:
    name: str
    daily_time_budget_minutes: int
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        ...

    def remove_pet(self, name: str) -> None:
        ...

    def list_pets(self) -> list[Pet]:
        ...


@dataclass
class DailyPlan:
    scheduled: list[tuple[str, Task]] = field(default_factory=list)
    skipped: list[tuple[Task, str]] = field(default_factory=list)
    total_minutes_used: int = 0

    def summary(self) -> str:
        ...


class Scheduler:
    def __init__(self, start_hour: int = 8) -> None:
        self.start_hour = start_hour

    def build_plan(self, owner: Owner, tasks: list[Task]) -> DailyPlan:
        ...

    def _sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        ...

    def _fit_into_budget(
        self, tasks: list[Task], budget_minutes: int
    ) -> tuple[list[Task], list[tuple[Task, str]]]:
        ...
