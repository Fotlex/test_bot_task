from django.db import models


class User(models.Model):
    id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    
    def __str__(self):
        return f'{self.id}: {self.first_name} {self.last_name}'


class Category(models.Model):
    name = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name
    
    
class Subcategory(models.Model):
    name = models.CharField(max_length=128)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    
class Item(models.Model):
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    caption = models.CharField(max_length=950, blank=True)
    image = models.ImageField(upload_to='media/')
    name = models.CharField(max_length=32)
    price = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name
    
    
class UserBucked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.IntegerField()
    
    def __str__(self):
        return f'{self.user.first_name} | {self.item.name} | {self.count}'
    
    
class MessageStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message_id = models.BigIntegerField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    
    def __str__(self):
        return self.message_id