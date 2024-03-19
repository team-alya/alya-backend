from django.urls import path

from alyabackend import views


urlpatterns = [
    path('instructions', views.InstructionsJson.as_view(), name="instructions"),
    path('sendpic', views.ReceivePic.as_view(), name='picture'),

]