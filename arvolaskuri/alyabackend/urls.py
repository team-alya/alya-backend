from django.urls import path

from alyabackend import views


urlpatterns = [
    path('', views.Frontpage.as_view(), name="test"),
    path('sendpic', views.ReceivePic.as_view(), name='picture'),

]