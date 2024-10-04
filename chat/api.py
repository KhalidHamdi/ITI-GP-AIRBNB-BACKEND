from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes

from .models import Conversation, ConversationMessage
from .serializers import ConversationListSerializer, ConversationDetailSerializer, ConversationMessageSerializer

from useraccount.models import User
from rest_framework.permissions import AllowAny 

from django.db.models import Prefetch
from django.core.paginator import Paginator

@api_view(['GET'])
def conversations_list(request):
    conversations = Conversation.objects.prefetch_related(
        'users',
        Prefetch('messages', queryset=ConversationMessage.objects.select_related('created_by', 'sent_to'))
    ).all()
    serializer = ConversationListSerializer(conversations, many=True) 
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def conversations_detail(request, pk):
    conversation = request.user.conversations.prefetch_related(
        'users',
        Prefetch('messages', queryset=ConversationMessage.objects.select_related('created_by', 'sent_to'))
    ).get(pk=pk)
    messages = ConversationMessage.objects.filter(conversation=conversation).order_by('created_at')
    # Set up pagination
    paginator = Paginator(messages, 10) 
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  
    conversation_serializer = ConversationDetailSerializer(conversation, many=False)
    messages_serializer = ConversationMessageSerializer(conversation.messages.all(), many=True)

    return JsonResponse({
        'conversation': conversation_serializer.data,
        'messages': messages_serializer.data,
        'page': page_number,
        'has_next': page_obj.has_next(),  
        'has_previous': page_obj.has_previous(),
        'total_pages': paginator.num_pages,  
    }, safe=False)




@api_view(['GET'])
def conversations_start(request, user_id):
    conversations = Conversation.objects.filter(users__in=[user_id]).filter(users__in=[request.user.id])

    if conversations.count() > 0:
        conversation = conversations.first()
        
        return JsonResponse({'success': True, 'conversation_id': conversation.id})
    else:
        user = User.objects.get(pk=user_id)
        conversation = Conversation.objects.create()
        conversation.users.add(request.user)
        conversation.users.add(user)

        return JsonResponse({'success': True, 'conversation_id': conversation.id})