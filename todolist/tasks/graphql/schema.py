import strawberry
from todolist.tasks.graphql.mutations import Mutation
from todolist.tasks.graphql.types import TaskType
from todolist.tasks.models import Task


@strawberry.type
class Query:
    all_tasks: list[TaskType] = strawberry.field(
        resolver=lambda: Task.objects.all()
    )

    @strawberry.field
    def task_by_id(self, id: int) -> TaskType:
        return Task.objects.get(pk=id)


schema = strawberry.Schema(query=Query, mutation=Mutation)
