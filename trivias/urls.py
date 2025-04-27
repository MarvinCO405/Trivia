from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="trivias.index"),
    path('<int:id>/', views.show, name='trivias.show'),
    path('trivia/<int:trivia_id>/leaderboard/', views.leaderboard, name='leaderboard'),
    path('trivia/<int:trivia_id>/save_score/', views.save_score_and_redirect, name='save_score_and_redirect'),
    path('trivia/<int:id>/', views.show, name='show'),
]
