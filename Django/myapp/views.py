from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from .models import User, Product, Category, Chat, Message, Picture
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.serializers import serialize
from django.contrib.auth.hashers import make_password
import base64, json
from django.db.models import Q
import os
from datetime import datetime
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


# Регистрация
class RegisterView(APIView):
    def post(self, request):
        # Извлечение данных из запроса
        name = request.data.get('name')
        password = request.data.get('password')
        email = request.data.get('email')

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Пользователь с таким email уже существует'}, status=status.HTTP_400_BAD_REQUEST)

        # Хеширование пароля
        hashed_password = make_password(password)

        # Создание пользователя
        user = User.objects.create(
            name=name,
            password=hashed_password,
            email=email,
        )

        # Создание JWT-токенов
        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Регистрация успешна',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
# Авторизация
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)
        if user is None:
            return Response({'error': 'Неверное имя пользователя или пароль'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Авторизация успешна',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)

# Выход
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Выход выполнен успешно'}, status=status.HTTP_200_OK)
    

class getProducts(APIView):
    def get(self, request):
        start = request.data.get('start')
        end = request.data.get('end')
        products = Product.objects.all()[start:end]
        return JsonResponse(products, safe=False)
    
class getProductsById(APIView):
    def get(self, request):
        id = request.data.get('id')
        start = request.data.get('start')
        end = request.data.get('end')

        product_data = []
        products = Product.objects.filter(seller = id)[int(start):int(end)]

        usr = User.objects.get(id=id)
        user = {
        'id':usr.id,
        'email':usr.email,
        'name':getattr(usr, 'name', None)
        }

        for product in products:
            
            categry = Category.objects.get(id=product.category.id)
            category = {
                'id': categry.id,
                'title': categry.title
            }
            pictre = Picture.objects.get(id=product.picture.id)
            picture = {
                'id': pictre.id,
                'photoPath': pictre.picturePath
            }

            product_data.append(
                    {
                    'id': product.id,
                    'seller': user,
                    'title':product.title,
                    'description':product.description,
                    'category':category,
                    'cost': product.cost,
                    'picture':picture,
                    })

        
        
        return JsonResponse(product_data ,safe=False)

class createProduct(APIView):
    def post(self, request):
        title = request.data.get('name')
        description = request.data.get('description')
        category = Category.objects.get(id = request.data.get('category'))
        seller = User.objects.get(id = request.data.get('seller'))
        cost = request.data.get('cost')
        picture = request.FILES.get('picture')
        pic = None

        try:
            target_directory = os.path.join(os.getcwd(), '../public/pictures')
            os.makedirs(target_directory, exist_ok=True)

            fileName = picture.name
            file_name = self.generate_unique_filename(fileName)

            target_path = os.path.join(target_directory, file_name)

            with open(target_path, 'wb') as destination:
                for chunk in picture.chunks():
                    destination.write(chunk)
            pic = Picture.objects.create(picturePath = f'/pictures/{file_name}')

            Product.objects.create(title=title,
                                    description=description,
                                    category=category,
                                    cost=cost,
                                    seller = seller,
                                    picture = pic
                                    )
            return Response('All good', status=status.HTTP_200_OK)
        except: 
            return Response('Something is wrong', status=status.HTTP_400_BAD_REQUEST)
        
    def generate_unique_filename(self, original_name):
        name, ext = os.path.splitext(original_name)
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_name = f"{name}_{timestamp}{ext}"
        
        return unique_name
        
class getCategories(APIView):
    def get(self, request):
        
        categories = Category.objects.all()
        serialized_data = serialize('json', categories)
        return JsonResponse(serialized_data, safe=False)
    
class getUser(APIView):
    def get(self, request):
        token = request.query_params.get('token')
        print(token)
        res = token.split('.')[1]
        return JsonResponse(self.decode_jwt_part(res))
    def decode_jwt_part(self, base64url_string):
        padding = len(base64url_string) % 4
        if padding != 0:
            base64url_string += "=" * (4 - padding)

        base64_string = base64url_string.replace('-', '+').replace('_', '/')
        
        decoded_bytes = base64.b64decode(base64_string)
        decoded_string = decoded_bytes.decode('utf-8')
        userId = json.loads(decoded_string)['user_id']

        user = User.objects.get(id = userId)

        data = {
            'id':user.id,
            'email':user.email,
            'name':getattr(user, 'name', None)
        }
        
        return data
    
class getMessages(APIView):
    def get(self, request):
        tmp = request.query_params.get('chat')
        messages = []
        try:
            chat = Chat.objects.get(id = tmp)
            if chat:
                messags = Message.objects.filter(chat = chat)
                for mes in messags:
                    messages.append(
                        {
                            'message': mes.message,
                            'sendingTime': mes.sendingTime,
                            'sender': mes.sender.id,
                            'receiver': mes.receiver.id
                        }
                    )
                
            return Response({'messages':messages}, status=status.HTTP_200_OK)
        except:
            return Response('Something is wrong', status=status.HTTP_400_BAD_REQUEST)
        
    def post(self,request):
        sender = request.data.get('sender')
        senderUser = User.objects.get(id=sender)
        receiver = request.data.get('receiver')
        receiverUser = User.objects.get(id=receiver)

        chat = Chat.objects.filter(
            firstUser = senderUser , secondUser = receiverUser
            ).first() or Chat.objects.filter(
                firstUser = receiverUser , secondUser = senderUser
                ).first()
        mesage = request.data.get('message')


        try:
            message = Message.objects.create(
                chat = chat,
                message = mesage,
                sender = senderUser,
                receiver = receiverUser
            )
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'chat_{chat.id}',  # Группа WebSocket для чата
                {
                    'type': 'chat_message',  # Тип события
                    'message': {
                        'id': message.id,
                        'text': message.message,
                        'sender': message.sender.id,
                        'receiver': message.receiver.id,
                        'sendingTime': message.sendingTime.isoformat(),
                    },
                }
            ) 
            return Response('All good', status=status.HTTP_200_OK)
        except: 
            return Response('Something is wrong', status=status.HTTP_400_BAD_REQUEST)
        
class getChats(APIView):
    def get(self,request):
        userId = request.query_params.get('user_id')
        user = User.objects.get(id = userId)

        chats = []
        filteredChats = Chat.objects.filter(Q(firstUser = user) | Q(secondUser = user))
        
        
        for chat in filteredChats:
            firstUser = {
                'id': chat.firstUser.id,
                'name': chat.firstUser.name,
                'photo': chat.firstUser.photoPath 
            }
            secondUser = {
                'id': chat.secondUser.id,
                'name': chat.secondUser.name,
                'photo': chat.secondUser.photoPath 
            }
            messge = Message.objects.filter(chat = chat.id).last()
            if messge:
                message = messge.message
            else: 
                message = ''
            chats.append(
                {
                    'id':chat.id,
                    'firstUser':firstUser,
                    'secondUser':secondUser,
                    'lastMessage': message
                }
            )
        return Response({'chats':chats}, status=status.HTTP_200_OK)
    
class changeUserProfile(APIView):
    def post(self,request):
        userId = request.data.get('user_id')
        photo = request.FILES.get('photo')
        name = request.data.get('name')

        user = User.objects.get(id = userId)
        try:
            if photo:
                target_directory = os.path.join(os.getcwd(), '../public/pictures/users/')
                os.makedirs(target_directory, exist_ok=True)

                fileName = photo.name
                file_name = self.generate_unique_filename(fileName)
                target_path = os.path.join(target_directory, file_name)

                with open(target_path, 'wb') as destination:
                    for chunk in photo.chunks():
                        destination.write(chunk)

                user.photoPath = f'/pictures/{file_name}'
            if name:
                user.name = name
            user.save()
            return Response('All good', status=status.HTTP_200_OK)
        except:
            return Response('Something wrong', status=status.HTTP_400_BAD_REQUEST)
        
    def generate_unique_filename(self, original_name):
        name, ext = os.path.splitext(original_name)
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_name = f"{name}_{timestamp}{ext}"
        
        return unique_name
    
class getUsersByChat(APIView):
    def get(self,request):
        chat_id = request.query_params.get('chat')
        chat = Chat.objects.get(id = chat_id)

        firstUsr = chat.firstUser
        firstUser = {
            'id': firstUsr.id,
            'name': firstUsr.name,
            'photo': firstUsr.photoPath
        }

        secondUsr = chat.secondUser
        secondUser = {
            'id': secondUsr.id,
            'name': secondUsr.name,
            'photo': secondUsr.photoPath
        }

        users = {
        'firstUser': firstUser,
        'secondUser': secondUser
        }

        return Response(users, status=status.HTTP_200_OK)

        





    
   
