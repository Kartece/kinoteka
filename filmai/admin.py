from django.contrib import admin

from .models import Aktorius, Filmas, FilmasInstance, Review, Profilis, Category
# Register your models here.

class FilmasInstanceInline(admin.TabularInline):
    model = FilmasInstance
    extra = 0


@admin.register(Filmas)
class FilmasAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas', 'aktoriusFK')
    search_fields = ('pavadinimas', 'aktorius__vardas_pavarde')
    inlines = [FilmasInstanceInline]


@admin.register(FilmasInstance)
class FilmasInstanceAdmin(admin.ModelAdmin):
    list_display = ('filmas', 'id', 'reader', 'status', 'due_back')
    list_editable = ('status', 'due_back', 'reader') # redaguojami laukai
    search_fields = ('id', 'filmas__pavadinimas')

    fieldsets = (
        ('General', {'fields': ('id', 'filmas')}),
        ('Availability', {'fields': ('reader', 'status', 'due_back')}),
    )


@admin.register(Aktorius)
class AktoriusAdmin(admin.ModelAdmin):
    list_display = ('vardas_pavarde', 'g_metai')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_date', 'author', 'comment')



admin.site.register(Profilis)
admin.site.register(Category)