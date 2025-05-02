
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class UserManager(models.Manager):
    def create_user(self, email, password=None, **extra_fields):
        """Создает и сохраняет обычного пользователя."""
        if not email:
            raise ValueError('Email должен быть указан')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создает и сохраняет суперпользователя."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)  # Поле для идентификации
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    photoPath = models.CharField(max_length=255, blank=True, null=True, default='/pictures/users/default.png')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()  # Подключаем кастомный менеджер

    # Поля для Django
    USERNAME_FIELD = 'email'  # Используется для аутентификации
    REQUIRED_FIELDS = ['name']  # Дополнительные поля для createsuperuser

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def is_authenticated(self):
        """Всегда возвращает True для авторизованных пользователей."""
        return True

    @property
    def is_anonymous(self):
        """Всегда возвращает False для авторизованных пользователей."""
        return False

    class Meta:
        db_table = 'users'
        managed = True

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)

    class Meta:
        db_table = 'categories'
        managed = True
    

class Picture(models.Model):
    id = models.AutoField(primary_key=True)
    picturePath = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'pictures'
        managed = True

class Status(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)

    class Meta:
        db_table = 'statuses'
        managed = True

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    cost = models.FloatField()
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE, related_name='pictures')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='statuses')
    createdTime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'products'
        managed = True

class FavoriteCollection(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')

    class Meta:
        db_table = 'favoriteCollections'
        managed = True

class Favorite(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    favoriteCollection = models.ForeignKey(FavoriteCollection, on_delete=models.CASCADE, related_name='favoriteCollections')

    class Meta:
        db_table = 'favorites'
        managed = True


class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    firstUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_as_first_user')
    secondUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_as_second_user')

    class Meta:
        db_table = 'chats'
        managed = True
    

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    message = models.CharField(max_length=255)
    sendingTime = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    isRead = models.BooleanField(default=False)

    class Meta:
        db_table = 'messages'
        managed = True

class RecoveryCode(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requesting_code')
    usage = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'recoveryCodes'
        managed = True




    