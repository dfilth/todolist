import strawberry


@strawberry.type
class TaskType:
    id: int
    title: str
    description: str
    completed: bool
