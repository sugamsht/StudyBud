from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("room/<str:name>/", views.room, name="room"),
    path("create-room/", views.createRoom, name="create-room"),
    path("update-room/<str:name>/", views.updateRoom, name="update-room"),
    path("delete-room/<str:name>/", views.deleteRoom, name="delete-room"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerPage, name="register"),
]
