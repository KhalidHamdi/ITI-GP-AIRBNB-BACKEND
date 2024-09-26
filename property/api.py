from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .forms import PropertyForm
from .models import Property
from .serializers import PropertiesListSerializer , PropertiesDetailSerializer
from django.shortcuts import get_object_or_404



@api_view(['GET'])
@permission_classes([AllowAny])
@permission_classes([])

def properties_list(request):
        properties = Property.objects.all()

        landlord_id = request.GET.get('landlord_id', '')
        if landlord_id:
            properties = properties.filter(landlord_id=landlord_id)

        serializer = PropertiesListSerializer(properties, many=True)
        return JsonResponse({
            'data': serializer.data
        })

@api_view(['POST'])
@permission_classes([AllowAny])  
def create_property(request):
    form = PropertyForm(request.POST, request.FILES)

    if form.is_valid():
        property = form.save(commit=False)
        property.save()

        return JsonResponse({'success': True})
    else:
        print('error', form.errors, form.non_field_errors)
        return JsonResponse({'errors': form.errors.as_json()}, status=400)



@api_view(['GET'])
@permission_classes([AllowAny])
@permission_classes([])
def properties_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    serializer = PropertiesDetailSerializer(property, many=False)
    return JsonResponse(serializer.data)