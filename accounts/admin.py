from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'is_guest', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_guest', 'is_staff', 'is_active')
    ordering = ('id',)

