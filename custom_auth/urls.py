from django.urls import path, include
from .views import RegisterView, ProfileView, LoginView, LogoutView, RuleViewSet

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Правила доступа (admin)
    path('rules/', RuleViewSet.as_view({'get': 'list', 'post': 'create'}), name='rule-list'),
    path('rules/<int:pk>/', RuleViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}), name='rule-detail'),
]
