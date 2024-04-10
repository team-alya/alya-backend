from django.urls import path
from alyabackend import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('instructions', views.InstructionsJson.as_view(), name="instructions"),
    path('sendpic', views.ReceivePic.as_view(), name='picture'),
    path('askprice', views.AskPrice.as_view(), name='askprice'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)