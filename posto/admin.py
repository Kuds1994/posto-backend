from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser, Posto, Precos, Denuncia

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        
        model = CustomUser
        fields = ('email',) 

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('id','first_name','email', 'is_staff', 'is_active')
    list_filter = ('email', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('first_name','last_name','email', 'password', 'last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'email', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )
    search_fields = ('email',)
    ordering = ('id',)

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Posto)
class PostoAdmin(admin.ModelAdmin):
    list_display = ('id','cnpj', 'ltd', 'lgt','user')
    list_filter = ('cnpj',)
    search_fields = ('cnpj',)    
    raw_id_fields = ('user',)
    ordering = ('cnpj',)

@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ('id','denuncia', 'posto')
    list_filter = ('id',)
    search_fields = ('id',)   
    ordering = ('id',)    

@admin.register(Precos)
class PrecosAdmin(admin.ModelAdmin):
    list_display = ('id','gasolina', 'posto')
    list_filter = ('id',)
    search_fields = ('id',)    
    raw_id_fields = ('posto',)
    ordering = ('id',)    