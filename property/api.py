from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


from .models import Property
from .serializers import PropertiesListSerializer


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
@permission_classes([])

def properties_list(request):
        properties = Property.objects.all()
        serializer = PropertiesListSerializer(properties, many=True)
        return JsonResponse({
            'data': serializer.data
        })
