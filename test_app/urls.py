from django.urls import path

from test_app import views


app_name = "test_app"
urlpatterns = [
    path("", views.index, name="name")
]