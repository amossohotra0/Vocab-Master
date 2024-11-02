from django.urls import path
from . import views

app_name = 'vocabulary'

urlpatterns = [
    path('', views.home, name='home'),
    path('words/', views.word_list, name='word_list'),
    path('flashcards/', views.flashcard_view, name='flashcards'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-word/', views.add_word, name='add_word'),
    path('edit-word/<int:word_id>/', views.edit_word, name='edit_word'),
    path('user-management/', views.user_management, name='user_management'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('toggle-user/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('manage-categories/', views.manage_categories, name='manage_categories'),
    path('add-word-type/', views.add_word_type, name='add_word_type'),
    path('add-difficulty/', views.add_difficulty, name='add_difficulty'),
    path('add-word-list/', views.add_word_list, name='add_word_list'),
    path('word-relationships/', views.word_relationships, name='word_relationships'),
    path('add-relationship/', views.add_relationship, name='add_relationship'),
]