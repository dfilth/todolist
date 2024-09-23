from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from .services import TaskService


class TaskViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            tasks = TaskService.get_all_tasks()
            serializer = TaskSerializer(tasks, many=True)

            if not tasks:
                return Response(
                    data={
                        "message": "No tasks available.",
                        "tasks": [],
                    },
                    status=status.HTTP_204_NO_CONTENT,
                )

            return Response(
                data={
                    "message": "Tasks retrieved successfully",
                    "tasks": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                data={"message": "Failed to retrieve tasks.", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def retrieve(self, request, pk=None):
        try:
            task = TaskService.get_task_by_id(pk)

            if task is None:
                return Response(
                    data={"message": f"The task with id {pk} does not exist."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = TaskSerializer(task)

            return Response(
                data={
                    "message": "Task retrieved successfully",
                    "task": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Task.DoesNotExist:
            return Response(
                data={"message": f"The task with id {pk} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"message": "Failed to retrieve task.", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def create(self, request):
        serializer = TaskSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                data={
                    "message": "Task created successfully",
                    "task": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception:
            return Response(
                data={
                    "message": "Failed to create task",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def update(self, request, pk=None):
        task = TaskService.get_task_by_id(pk)
        if not task:
            return Response(
                data={"message": f"The task with id {pk} doesn't exists."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TaskSerializer(task, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                data={
                    "message": "Task updated successfully",
                    "task": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception:
            return Response(
                data={
                    "message": "Failed to update task",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, pk=None):
        if TaskService.delete_task(pk):
            return Response(
                data={
                    "message": f"The task with id {pk} "
                    f"has been deleted successfully."
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            data={"error": f"The task with id {pk} does not exist."},
            status=status.HTTP_404_NOT_FOUND,
        )
