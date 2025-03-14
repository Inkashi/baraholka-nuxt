from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from .models import User, Product, Category, PicturesCollection, Chat, Message
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.serializers import serialize
from django.contrib.auth.hashers import make_password
import base64, json
from django.db.models import Q

# Регистрация
class RegisterView(APIView):
    def post(self, request):
        # Извлечение данных из запроса
        name = request.data.get('name')
        password = request.data.get('password')
        email = request.data.get('email')
        photoPath = request.data.get('photoPath', '')  # Необязательное поле

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Пользователь с таким email уже существует'}, status=status.HTTP_400_BAD_REQUEST)

        # Хеширование пароля
        hashed_password = make_password(password)

        # Создание пользователя
        user = User.objects.create(
            name=name,
            password=hashed_password,
            email=email,
            photoPath=photoPath
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

            product_data.append(
                    {
                    'id': product.id,
                    'seller': user,
                    'title':product.title,
                    'description':product.description,
                    'category':category,
                    'cost': product.cost,
                    'picturesCollection':product.picturesCollection.id,
                    })

        
        
        return JsonResponse(product_data ,safe=False)

class createProduct(APIView):
    def post(self, request):
        title = request.data.get('name')
        description = request.data.get('description')
        category = Category.objects.get(id = request.data.get('category'))
        seller = User.objects.get(id = request.data.get('seller'))
        cost = request.data.get('cost')
        picturesCollection = PicturesCollection.objects.create()

        try:
            Product.objects.create(title=title,
                                    description=description,
                                    category=category,
                                    cost=cost,
                                    seller = seller,
                                    picturesCollection = picturesCollection)
            return Response('All good', status=status.HTTP_200_OK)
        except: 
            return Response('Something is wrong', status=status.HTTP_400_BAD_REQUEST)
        
class getCategories(APIView):
    def get(self, request):
        
        categories = Category.objects.all()
        serialized_data = serialize('json', categories)
        return JsonResponse(serialized_data, safe=False)
    
class getUser(APIView):
    def get(self, request):
        token = request.data.get('token')
        
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
        first = request.data.get('firstUser')
        firstUser = User.objects.get(id=first)
        second = request.data.get('secondUser')
        secondUser = User.objects.get(id=second)
        try:
            chat = Chat.objects.filter(
                firstUser=firstUser, secondUser=secondUser
            ).first() or Chat.objects.filter(
                firstUser=secondUser, secondUser=firstUser
            ).first()

            if chat:
                # Если чат существует, возвращаем его ID
                return Response({'chat_id': chat.id}, status=status.HTTP_200_OK)
            chat = Chat.objects.create(
                    firstUser = firstUser,
                    secondUser = secondUser
                )
            return Response({'chat_id': chat.id}, status=status.HTTP_200_OK)
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
        message = request.data.get('message')
        sendingTime = request.data.get('sendingTime')

        try:
            messsage = Message.objects.create(
                chat = chat,
                message = message,
                sendingTime = sendingTime,
                sender = senderUser,
                receiver = receiverUser
            ) 
            return Response('All good', status=status.HTTP_200_OK)
        except: 
            return Response('Something is wrong', status=status.HTTP_400_BAD_REQUEST)
        
class getChats(APIView):
    def get(self,request):
        userId = request.data.get('user_id')
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
            chats.append(
                {
                    'id':chat.id,
                    'firstUser':firstUser,
                    'secondUser':secondUser
                }
            )
        return Response({'chats':chats}, status=status.HTTP_200_OK)




    
   
