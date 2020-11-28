from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Usuário customizavel onde o e-mail e a chave primária para autenticação ao inves do campo username
    """
    
    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError('O email deve ser declarado')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)        
        user.set_password(password)        
        user.save() 
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('O superusuario deve ter  o campo is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('O superusuario deve ter  o campo is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)     