from django.contrib import admin

from .models import *


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Item)
admin.site.register(UserBucked)
admin.site.register(MessageStatus)
admin.site.register(YookassaInfo)
admin.site.register(FAQ)
