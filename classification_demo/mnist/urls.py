from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from mnist import views

urlpatterns = [
    url(r'^classify/$', views.ImageView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)