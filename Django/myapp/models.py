
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    photoPath = models.CharField(max_length=255, blank=True, null=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    
    class Meta:
        db_table = 'users'
        managed = True


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)

    class Meta:
        db_table = 'categories'
        managed = True


class PicturesCollection(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'picturesCollections'
        managed = True
    

class Picture(models.Model):
    id = models.AutoField(primary_key=True)
    picturesPath = models.CharField(max_length=255)
    picturesCollection = models.ForeignKey(PicturesCollection, on_delete=models.CASCADE, related_name='pictures')
    
    class Meta:
        db_table = 'pictures'
        managed = True


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    cost = models.FloatField()
    picturesCollection = models.ForeignKey(PicturesCollection, on_delete=models.CASCADE, related_name='products')

    class Meta:
        db_table = 'products'
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

    class Meta:
        db_table = 'messages'
        managed = True

    