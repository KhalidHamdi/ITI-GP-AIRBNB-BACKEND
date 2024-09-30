from django.shortcuts import render

# Create your views here.
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
