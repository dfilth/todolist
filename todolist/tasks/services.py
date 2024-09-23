from .models import Task


class TaskService:
    @staticmethod
    def get_all_tasks():
        return Task.objects.all()

    @staticmethod
    def get_task_by_id(id):
        try:
            return Task.objects.get(id=id)
        except Task.DoesNotExist:
            return None

    @staticmethod
    def update_task(id, data):
        task = TaskService.get_task_by_id(id)
        if task:
            for key, value in data.items():
                setattr(task, key, value)
            task.save()
            return task
        return None

    @staticmethod
    def delete_task(id):
        task = TaskService.get_task_by_id(id)
        if task:
            task.delete()
            return True
        return False
