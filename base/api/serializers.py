from rest_framework.serializers import ModelSerializer
from base.models import Room


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
        # fields = ("id", "name", "description", "created_at", "updated_at")
        # read_only_fields = ("id", "created_at", "updated_at")
