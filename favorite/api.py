from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Favorite, Property
from .serializers import FavoriteSerializer
from django.shortcuts import get_object_or_404

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite(request, pk):
    user = request.user
    property = get_object_or_404(Property, pk=pk)

    if Favorite.objects.filter(user=user, property=property).exists():
        return JsonResponse({'error': 'Property already in favorites.'}, status=400)

    favorite = Favorite.objects.create(user=user, property=property)
    serializer = FavoriteSerializer(favorite)

    return JsonResponse(serializer.data, status=201)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_favorite(request, pk):
    user = request.user
    property = get_object_or_404(Property, pk=pk)

    favorite = Favorite.objects.filter(user=user, property=property).first()
    if favorite:
        favorite.delete()
        return JsonResponse({'success': True}, status=204)
    else:
        return JsonResponse({'error': 'Favorite not found.'}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_favorites(request):
    user = request.user
    favorites = Favorite.objects.filter(user=user)
    serializer = FavoriteSerializer(favorites, many=True)

    return JsonResponse(serializer.data, safe=False, status=200)
