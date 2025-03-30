from django.urls import path
from . import views

urlpatterns = [
    path('', views.translation_page, name='translation_page'),  # Handles the root URL
    path('translate/', views.translation_page, name='translation_page'),
    path('history/', views.history_page, name='history_page'),
    path('api/translate/', views.TranslateView.as_view(), name='translate_api'),
]
