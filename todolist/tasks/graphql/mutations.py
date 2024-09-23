import strawberry
from .types import TaskType
from ..models import Task


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_task(
        self, title: str, description: str, completed: bool
    ) -> TaskType:
        task = Task.objects.create(
            title=title, description=description, completed=completed
        )
        return task

    @strawberry.mutation
    def update_task(
        self,
        id: int,
        title: str = None,
        description: str = None,
        completed: bool = None,
    ) -> TaskType:
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            raise Exception("Task not found")

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed

        task.save()
        return task

    # Eliminar una tarea
    @strawberry.mutation
    def delete_task(self, id: int) -> bool:
        task = Task.objects.get(pk=id)
        task.delete()
        return True
