from rest_framework import serializers
from .models import Conversation , ConversationMessage
# from useraccount.serializers import UserDetailSerializer

class ConversationListSerializer(serializers.ModelSerializer):
    # user=UserDetailSerializer(many=True,read_only=True)
    class Meta:
        model=Conversation
        fileds=('id','users','modified_at')