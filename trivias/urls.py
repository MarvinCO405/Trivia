from django.urls import path
from . import views

app_name = "trivias"  # This is important for namespacing!

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:category_id>/", views.trivia_category, name="trivia_category"),  # This must match the template
]
