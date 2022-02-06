from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('<int:superior_id>', views.index, name='index'),
    path('edit/', views.edit_worker, name='edit'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]
