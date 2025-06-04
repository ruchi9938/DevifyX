from django.contrib import admin
from .models import QuesModel, Category, QuizAttempt, UserProfile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

@admin.register(QuesModel)
class QuesModelAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'created_by', 'time_limit', 'points', 'created_at')
    list_filter = ('category', 'created_by', 'created_at')
    search_fields = ('question', 'category__name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'selected_answer', 'is_correct', 'time_taken', 'attempted_at')
    list_filter = ('is_correct', 'attempted_at')
    search_fields = ('user__username', 'question__question')
    readonly_fields = ('attempted_at',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_admin', 'max_attempts', 'total_score', 'quizzes_completed')
    list_filter = ('is_admin',)
    search_fields = ('user__username',)
