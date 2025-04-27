from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="trivias.index"),
    path('<int:id>/', views.show, name='trivias.show'),
    path('leaderboard/', views.leaderboard, name='trivias.leaderboard'),
    path('trivia/<int:trivia_id>/save_score/', views.save_score, name='save_score'),
    path('trivia/<int:id>/', views.show, name='show'),
]
