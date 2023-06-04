from django.urls import path

from users import views

urlpatterns = [
    path('<str:username>/', views.UserRetrieveAPIView.as_view())
]
