from django.urls import path
from . import views

app_name = 'posto'

urlpatterns = [
    path('posto/', views.PostoList.as_view(), name='posto_list'),
    path('posto/details/<pk>/', views.PostoRetrieve.as_view(), name='posto_details'),
    path('posto/update/', views.PostoUpdate.as_view(), name='posto_update'),  
    path('posto/preco/create/', views.PrecoCreate.as_view(), name='preco_create'),
    path('posto/preco/<pk>/', views.PrecoRetrieve.as_view(), name='preco_retrieve'),    
    path('user/changepassword', views.UserChangePassword.as_view(), name='user_change_password'),  
    path('user/create/', views.UserCreate.as_view(), name='user_create'),
    path('user/details/<pk>/', views.UserRetrieve.as_view(), name="user_details"),
    path('user/delete/', views.UserDelete.as_view(), name="user_delete"),
    path('denuncia/create/', views.DenunciaCreate.as_view(), name="denuncia_create"),
    path('device/gcm/', views.DeviceCreate.as_view(), name="gcm_device_create"),    
]
