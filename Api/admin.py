from django.contrib import admin
from .models import Customer,Comment,User



class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'auth_provider', 'created_at']

admin.site.register(Customer)
admin.site.register(Comment)
admin.site.register(User,UserAdmin)