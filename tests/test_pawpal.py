from pawpal_system import Pet, Priority, Task, TaskStatus


def test_mark_complete_changes_status() -> None:
    task = Task(
        name="Morning walk",
        duration_minutes=30,
        priority=Priority.HIGH,
        task_type="walk",
    )
    assert task.status == TaskStatus.PENDING
    task.mark_complete()
    assert task.status == TaskStatus.COMPLETE


def test_add_task_increases_pet_task_count() -> None:
    pet = Pet(name="Mochi", species="dog", age=3)
    assert len(pet.tasks) == 0
    pet.add_task(Task("Feed", 10, Priority.HIGH, "feed"))
    assert len(pet.tasks) == 1
    pet.add_task(Task("Fetch", 20, Priority.MEDIUM, "play"))
    assert len(pet.tasks) == 2
