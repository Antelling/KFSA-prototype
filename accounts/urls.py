from django.urls import path
from django.contrib.auth import views as auth_views

from . import views as v


urlpatterns = [
    path('signup/', v.SignUpView.as_view(), name='signup'),
    path('set_permissions/', v.set_permissions, name='set_perm' ),
    path('login/', auth_views.LoginView.as_view(), name='accounts_login')
]
