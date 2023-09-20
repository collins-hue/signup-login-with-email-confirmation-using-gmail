from django.urls import path

from mainapp import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.signup, name='signup'),
    path('home', views.home, name='home'),
    path('login/', views.login_request, name='login'),
    path('finalactivate/<uidb64>/<token>', views.finalactivation, name='finalactivate'),

]
