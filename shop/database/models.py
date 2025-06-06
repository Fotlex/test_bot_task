from django.db import models


class User(models.Model):
    id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    
    def __str__(self):
        return f'{self.id}: {self.first_name} {self.last_name}'
    
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'



class Category(models.Model):
    name = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name = 'Катугория'
        verbose_name_plural = 'Категории'

    
    
class Subcategory(models.Model):
    name = models.CharField(max_length=128)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    
    
class Item(models.Model):
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    caption = models.CharField(max_length=950, blank=True)
    image = models.ImageField(upload_to='media/')
    name = models.CharField(max_length=32)
    price = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name
    
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    
    
class UserBucked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.IntegerField()
    
    def __str__(self):
        return f'{self.user.first_name} | {self.item.name} | {self.count}'
    
    
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    
    
class MessageStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message_id = models.BigIntegerField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    
    def __str__(self):
        return self.message_id
    
    
class YookassaInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=1024)
    number = models.CharField(max_length=20)
    adress = models.CharField(max_length=256)
    bucked_id = models.IntegerField(default=0)
    
    
    def __str__(self):
        return self.number
    
    
    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    
    
class FAQ(models.Model):
    question = models.CharField(max_length=512)
    answer = models.CharField(max_length=2048)
    
    def __str__(self):
        return self.question
    
    
    class Meta:
        verbose_name = 'Вопросы и ответы'
        verbose_name_plural = 'Вопросы и ответы'
        
        
class Broadcast(models.Model):
    message = models.CharField(max_length=3000)
    send = models.BooleanField(default=False)
    
    def __str__(self):
        return self.message
    
    
    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    