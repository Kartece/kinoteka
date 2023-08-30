from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='homepage-url'),
    path('aktoriai/', views.aktoriai, name='aktoriai-visi-url'),
    path('aktoriai/<int:aktorius_id>', views.aktorius, name='aktorius-vienas-url'),
    path('filmai', views.FilmasListView.as_view(), name='filmai-visi-url'),
    path('filmai/<int:pk>', views.FilmasDetailView.as_view(), name='filmas-vienas-url'),
    path('paieska/', views.search, name='paieska-url'),
    ]
