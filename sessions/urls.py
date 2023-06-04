from django.urls import path

from sessions import views

urlpatterns = [
    path('', views.SessionListCreateAPIView.as_view()),
    path('<int:pk>', views.SessionRetrieveUpdateDestroyAPIView.as_view()),
    path('<int:pk>/join/', views.SessionJoinOrLeaveAPIView.as_view())
]
