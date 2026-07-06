from django.contrib import admin
from django.urls import path
from shift_app import views
from django.http import HttpResponse

def home(request):
    return HttpResponse("Shift App is running")

urlpatterns = [
    path('', home),  # ← これを追加
    path('admin/', admin.site.urls),
    path('shift/search/', views.shift_search, name='shift_search'),
    path('shift/result/', views.shift_search, name='shift_result'),
]

