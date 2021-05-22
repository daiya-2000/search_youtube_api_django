from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    # rは正規表現　^先頭一文字 $最後の一文字
    path('', views.index, name="index"),
]
