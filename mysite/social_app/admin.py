from django.contrib import admin

from .models import UserMessage, ConvoPreview, Post_Likes

admin.site.register(UserMessage)
admin.site.register(ConvoPreview)
admin.site.register(Post_Likes)

#
# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 3
#
#
# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,               {'fields': ['question_text']}),
#         ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
#     ]
#     inlines = [ChoiceInline]
#     list_display = ('question_text', 'pub_date', 'was_published_recently')
