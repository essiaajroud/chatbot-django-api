from django.http import JsonResponse
from django.contrib.auth import login,logout, authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated   
from .forms import CustomUserCreationForm
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomLoginSerializer
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
import json
from django.views.decorators.http import require_POST


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        print(request.data) 
        form = CustomUserCreationForm({
            'username': request.data['username'],
            'email': request.data['email'],
            'password1': request.data['password'],
            'password2': request.data['confirm_password'],
        })
        if form.is_valid():
            authentication_backend = 'users.backends.EmailBackend'
            user = form.save()
           # user.backend = authentication_backend
            user = authenticate(
                request, email=user.email, password=form.cleaned_data['password1'],
                 backend=authentication_backend)
            token,created = Token.objects.get_or_create(user=user)
            login(request, user)
            response_data = {
                'message': 'Registration successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                },
                'token': token.key,
            }
            response_data['Access-Control-Allow-Origin'] = 'http://localhost:65306'
            response_data['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response_data['Access-Control-Allow-Methods'] = 'POST'
            print(form.errors)
            return JsonResponse(response_data, status=201)       
        else:
            return JsonResponse({'error': form.errors}, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    if request.method == 'POST':
        serializer = CustomLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                token = user.auth_token.key 
                response_data = {
                    'message': 'Login successful',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                    },
                    'token': token,
                }
                return JsonResponse(response_data)
            else:                
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_logout(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful'})

@require_POST
@permission_classes([IsAuthenticated])
def save_chat_message(request):
    try:
        data = json.loads(request.body)
        message_text = data.get('message', '')
        
        # Create and save a new ChatMessage instance
        chat_message = ChatMessage(user=request.user, message=message_text)
        chat_message.save()        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)})
    

def get_user_chat_messages(request):
    user_chat_messages = ChatMessage.objects.filter(user=request.user)
    messages = [{'message': chat.message, 'timestamp': chat.timestamp} for chat in user_chat_messages]
    
    return JsonResponse({'status': 'success', 'messages': messages})


class CustomLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                
                response_data = {
                    'message': 'Login successful',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                    },
                    'token': token.key,
                }

                return Response(response_data, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)