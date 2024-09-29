from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import User
from .serializers import UserDetailSerializer

from property.serializers import PropertiesListSerializer
from Reservation.serializers import ReservationsListSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserDetailSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserDetailSerializer


from dj_rest_auth.views import LoginView
from rest_framework.response import Response



from rest_framework.response import Response
from dj_rest_auth.views import LoginView
from .serializers import UserDetailSerializer
from .serializers import UserUpdateSerializer

class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if 'key' not in response.data:
            print("Login failed: No token returned.")
            return Response(
                {"error": "Login failed. Token not found in response."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Add user details to the response
        user = request.user
        user_data = UserDetailSerializer(user).data
        
        # Return both the key and user data in the response
        response_data = {
            'key': response.data.get('key'),
            'user_id': user.id,  # or any user details you want to include
            'user': user_data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    
    
class RegisterView(APIView):
    def post(self, request):
        serializer = UserDetailSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": UserDetailSerializer(user).data,
                "message": "User Created Successfully.",
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def landlord_detail(request, username):
    user = User.objects.get(username=username)
    print("User", user)

    serializer = UserDetailSerializer(user, many=False)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def reservations_list(request):
    reservations = request.user.reservations.all()

    print('user', request.user)
    print(reservations)
    
    serializer = ReservationsListSerializer(reservations, many=True)
    return JsonResponse(serializer.data, safe=False)




from rest_framework.authentication import TokenAuthentication

@api_view(['GET', 'PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    
    if request.method == 'GET':
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserDetailSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)