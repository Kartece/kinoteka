from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='homepage-url'),
    path('aktoriai/', views.aktoriai, name='aktoriai-visi-url'),
    path('aktoriai/<int:aktorius_id>', views.aktorius, name='aktorius-vienas-url'),
    path('filmai', views.FilmasListView.as_view(), name='filmai-visi-url'),
    path('filmai/<int:pk>', views.FilmasDetailView.as_view(), name='filmas-vienas-url'),
    path('register/', views.register, name='register-url'),
    path('profilis/', views.profilis, name='profilis-url'),
    path('success/', views.success, name='success-url'),
    path('rate/<int:id>', views.rate, name='rate-url'),
    path('paieska/', views.search, name='paieska-url'),
    path('mybooks/new', views.FilmasByUserCreateView.as_view(), name='my-borrowed-new'),
    path('mybooks/<uuid:pk>/update', views.FilmasByUserUpdateView.as_view(), name='my-borrowed-update'),
    path('mybooks/<uuid:pk>/delete', views.FilmasByUserDeleteView.as_view(), name='my-borrowed-delete'),
    path('mybooks/', views.LoanedFilmaiByUserListView.as_view(), name='my-borrowed'),
    ]
