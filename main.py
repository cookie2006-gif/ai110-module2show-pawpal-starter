from pawpal_system import Owner, Pet, Priority, Scheduler, Task


def main() -> None:
    owner = Owner(name="Jordan", daily_time_budget_minutes=60)

    mochi = Pet(name="Mochi", species="dog", age=3, health_notes="loves walks")
    bella = Pet(name="Bella", species="cat", age=5, health_notes="daily thyroid med")

    mochi.add_task(Task("Morning walk", 30, Priority.HIGH, "walk", preferred_time="08:00"))
    mochi.add_task(Task("Feed", 10, Priority.HIGH, "feed"))
    mochi.add_task(Task("Fetch", 20, Priority.MEDIUM, "play"))

    bella.add_task(Task("Feed", 5, Priority.HIGH, "feed"))
    bella.add_task(Task("Thyroid med", 5, Priority.HIGH, "med", preferred_time="10:00"))
    bella.add_task(Task("Groom", 15, Priority.LOW, "grooming"))

    owner.add_pet(mochi)
    owner.add_pet(bella)

    scheduler = Scheduler(start_hour=8)
    plan = scheduler.build_plan(owner)

    print("=" * 60)
    print(
        f"Today's Schedule — {owner.name} "
        f"(budget: {owner.daily_time_budget_minutes} min)"
    )
    print("=" * 60)
    print(plan.summary())


if __name__ == "__main__":
    main()
