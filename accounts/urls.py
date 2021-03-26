from django.urls import path
from django.contrib.auth import views as auth_views

from . import views as v


urlpatterns = [
    path('signup/', v.SignUpView.as_view(), name='signup'),
    path('set_permissions/', v.set_permissions, name='set_perm' ),
    path('login/', auth_views.LoginView.as_view(), name='accounts_login'),
    #path('password/', auth_views.PasswordChangeView.as_view(),name='change-password')
    path('password/', v.ChangePassWordView.as_view(template_name='registration/changepassword.html')),
    path('password_success', v.password_success, name="password_success"),
]
