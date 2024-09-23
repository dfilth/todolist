from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def validate_title(self, value):
        """Validate that the title is not empty
        and has an appropriate length."""
        if not value:
            raise serializers.ValidationError("The title cannot be empty.")
        if len(value) > 100:
            raise serializers.ValidationError(
                "The title cannot exceed 100 characters."
            )
        return value

    def validate_description(self, value):
        """Validate that the description does not
        exceed a maximum length."""
        if len(value) > 500:
            raise serializers.ValidationError(
                "The description cannot exceed 500 characters."
            )
        return value

    def validate(self, data):
        """Additional validations involving multiple fields."""
        if data.get("completed") and not data.get("description"):
            raise serializers.ValidationError(
                "If the task is completed, it must have a description."
            )
        return data
