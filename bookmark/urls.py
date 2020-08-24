from django.urls import path
from bookmark.views import *

app_name = 'bookmark'

urlpatterns = [
    path('', index, name='index'),
    path('<int:pk>/', BookmarkDV.as_view(), name='detail'),
    # Example: /bookmark/add/
    path('add/', BookmarkCreateView.as_view(), name="add"),
    # Example: /bookmark/change/
    path('change/', BookmarkChangeLV.as_view(), name="change"),
    # Example: /bookmark/99/update/
    path('<int:pk>/update/', BookmarkUpdateView.as_view(), name="update"),
    # Example: /bookmark/99/delete/
    path('<int:pk>/delete/', BookmarkDeleteView.as_view(), name="delete"),
]