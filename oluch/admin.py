from django.contrib import admin
from oluch.models import Problem, Submit, Contest, UserProfile

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('number', 'contest', 'sort_order',)
    list_display_links = ('number', )

@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'title', 'accept_submits', 'show_results', 'sort_order')
    list_display_links = ('short_title', 'title')



@admin.register(Submit)
class Submit(admin.ModelAdmin):
    list_display = ('id', author_lastname, 'problem', 'datetime', )
    list_display_links = ('id', )

admin.site.register(UserProfile)
