from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskStatus(Enum):
    PENDING = "pending"
    COMPLETE = "complete"


@dataclass
class Task:
    name: str
    duration_minutes: int
    priority: Priority
    task_type: str
    preferred_time: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING

    def is_high_priority(self) -> bool:
        """Return True when this task is HIGH priority."""
        return self.priority == Priority.HIGH

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.status = TaskStatus.COMPLETE

    def __repr__(self) -> str:
        """One-line, human-friendly summary of the task."""
        return f"Task({self.name!r}, {self.duration_minutes}min, {self.priority.name})"


@dataclass
class Pet:
    name: str
    species: str
    age: int
    health_notes: str = ""
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, name: str) -> None:
        """Drop every task with a matching name (no-op if none match)."""
        self.tasks = [t for t in self.tasks if t.name != name]

    def list_tasks(self) -> list[Task]:
        """Return a shallow copy of this pet's tasks."""
        return list(self.tasks)


@dataclass
class Owner:
    name: str
    daily_time_budget_minutes: int
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def remove_pet(self, name: str) -> None:
        """Drop every pet with a matching name (no-op if none match)."""
        self.pets = [p for p in self.pets if p.name != name]

    def list_pets(self) -> list[Pet]:
        """Return a shallow copy of this owner's pets."""
        return list(self.pets)


@dataclass
class ScheduledTask:
    start_time: str
    pet: Pet
    task: Task


@dataclass
class DailyPlan:
    scheduled: list[ScheduledTask] = field(default_factory=list)
    skipped: list[tuple[Pet, Task, str]] = field(default_factory=list)
    total_minutes_used: int = 0

    def summary(self) -> str:
        """Return a human-readable text summary of the plan."""
        lines: list[str] = []
        if not self.scheduled:
            lines.append("  (nothing scheduled)")
        else:
            for entry in self.scheduled:
                lines.append(
                    f"  {entry.start_time}  {entry.pet.name:<8}"
                    f"  {entry.task.name:<16}"
                    f"  ({entry.task.duration_minutes:>2} min, {entry.task.priority.value})"
                )
        lines.append("-" * 60)
        lines.append(f"  Total time used: {self.total_minutes_used} min")
        if self.skipped:
            lines.append("")
            lines.append("Skipped:")
            for pet, task, reason in self.skipped:
                lines.append(f"  {pet.name:<8}  {task.name:<16}  — {reason}")
        return "\n".join(lines)


class Scheduler:
    _PRIORITY_ORDER = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}

    def __init__(self, start_hour: int = 8) -> None:
        """Build a scheduler that lays tasks out starting at start_hour (24-hour clock)."""
        self.start_hour = start_hour

    def build_plan(self, owner: Owner) -> DailyPlan:
        """Return a DailyPlan for the owner: high-priority-first, greedy, budget-capped."""
        pet_tasks = [(pet, task) for pet in owner.pets for task in pet.tasks]
        ordered = self._sort_by_priority(pet_tasks)
        fitted, skipped = self._fit_into_budget(
            ordered, owner.daily_time_budget_minutes
        )
        plan = DailyPlan(skipped=skipped)
        current = self.start_hour * 60
        for pet, task in fitted:
            hh, mm = divmod(current, 60)
            plan.scheduled.append(
                ScheduledTask(start_time=f"{hh:02d}:{mm:02d}", pet=pet, task=task)
            )
            plan.total_minutes_used += task.duration_minutes
            current += task.duration_minutes
        return plan

    def _sort_by_priority(
        self, pet_tasks: list[tuple[Pet, Task]]
    ) -> list[tuple[Pet, Task]]:
        """Stable sort by task priority (HIGH → MEDIUM → LOW)."""
        return sorted(pet_tasks, key=lambda pt: self._PRIORITY_ORDER[pt[1].priority])

    def _fit_into_budget(
        self, pet_tasks: list[tuple[Pet, Task]], budget_minutes: int
    ) -> tuple[list[tuple[Pet, Task]], list[tuple[Pet, Task, str]]]:
        """Greedy-fit tasks into the budget; return (fitted, skipped-with-reason)."""
        fitted: list[tuple[Pet, Task]] = []
        skipped: list[tuple[Pet, Task, str]] = []
        used = 0
        for pet, task in pet_tasks:
            if used + task.duration_minutes <= budget_minutes:
                fitted.append((pet, task))
                used += task.duration_minutes
            else:
                skipped.append(
                    (pet, task, f"exceeds daily budget ({budget_minutes} min)")
                )
        return fitted, skipped
