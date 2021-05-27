from rest_framework import serializers
from .user_serializer import UserSerializer
from ..models import Event


class EventSerializer(serializers.ModelSerializer):
    """
    On writes,\n
    - user expects a primary key\n

    On reads,\n
    - user is a serialized user object\n

    The autogenerated documentation does not account for this
    """

    id = serializers.ReadOnlyField()
    created = serializers.DateTimeField(read_only=True)
    event_type = serializers.ReadOnlyField()
    user = UserSerializer(many=False)
    object_id = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = [
            "id", "team_id", "created", "event_type", "user", "user_id",
            "description", "object_id"
        ]
