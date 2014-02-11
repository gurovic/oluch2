from django.contrib import admin
from oluch.models import Problem, Submit, Contest, UserProfile, Mark

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('contest', 'number', 'title', 'sort_order')
    list_display_links = ('number', 'title')

@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'title', 'accept_submits', 'show_results', 'sort_order')
    list_display_links = ('short_title', 'title')

@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('contest', 'title', 'sort_order')

admin.site.register(UserProfile)
admin.site.register(Submit)
