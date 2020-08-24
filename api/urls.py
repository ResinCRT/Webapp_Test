from django.urls import path, re_path
from api.views import *

urlpatterns = [
    path('bookmark', BookmarkApi.as_view()),
    path('bookmark/<int:id>', BookmarkApi.as_view()),
]