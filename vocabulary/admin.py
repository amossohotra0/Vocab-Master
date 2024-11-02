from django.contrib import admin
from .models import WordsBank, WordList, WordType, DifficultyLevel, UserProgress, UserProfile, WordRelationship

@admin.register(WordList)
class WordListAdmin(admin.ModelAdmin):
    list_display = ['word_list_name', 'created_at']
    search_fields = ['word_list_name']

@admin.register(WordType)
class WordTypeAdmin(admin.ModelAdmin):
    list_display = ['word_type', 'abbreviation']
    search_fields = ['word_type']

@admin.register(DifficultyLevel)
class DifficultyLevelAdmin(admin.ModelAdmin):
    list_display = ['level']

@admin.register(WordsBank)
class WordsBankAdmin(admin.ModelAdmin):
    list_display = ['word', 'word_type', 'difficulty_level', 'is_favorite', 'times_reviewed']
    list_filter = ['word_type', 'difficulty_level', 'is_favorite', 'word_lists']
    search_fields = ['word', 'meaning_english', 'meaning_urdu', 'synonyms']
    filter_horizontal = ['word_lists']
    ordering = ['word']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['word', 'user', 'mastery_level', 'times_correct', 'times_incorrect']
    list_filter = ['mastery_level']
    search_fields = ['word__word', 'user__email']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'subscription_status', 'created_at']
    list_filter = ['subscription_status', 'country']
    search_fields = ['user__email', 'first_name', 'last_name', 'google_id']
    readonly_fields = ['google_id', 'created_at', 'updated_at']

@admin.register(WordRelationship)
class WordRelationshipAdmin(admin.ModelAdmin):
    list_display = ['word1', 'word2', 'relationship_type', 'created_at']
    list_filter = ['relationship_type', 'created_at']
    search_fields = ['word1__word', 'word2__word']
    autocomplete_fields = ['word1', 'word2']