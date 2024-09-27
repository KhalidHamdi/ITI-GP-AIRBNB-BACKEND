from django.db import models
import uuid
from useraccount.models import User



class Conversation(models.Model):
    id= models.UUIDField(primary_key=True , default=uuid.uuid4 , editable=False)
    users=models.ManyToManyField(User, related_name='conversations')
    created_at= models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        users = self.users.all()
        if users.exists():
            user_list = ', '.join(user.name for user in users)
            return f"Conversation between {user_list}"
        else:
            print(f"Conversation ID {self.id} has no users.") 
            return "Conversation with no users"


class ConversationMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField()
    sent_to = models.ForeignKey(User, related_name='messages_sent', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='messages_received', on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    def  __str__(self):
        return f"Message from {self.created_by} to {self.sent_to}"
