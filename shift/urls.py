from django.contrib import admin
from django.urls import path
from shift_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shift/search/', views.shift_search, name='shift_search'),
    path('shift/result/', views.shift_search, name='shift_result'),
]

