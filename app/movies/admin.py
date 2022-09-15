from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Genre, Person, Filmwork, GenreFilmwork, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    ordering = ('full_name',)
    search_fields = ('full_name',)


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    autocomplete_fields = ('genre',)
    verbose_name = _('Genre')
    verbose_name_plural = _('Genres')


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ('person',)
    verbose_name = _('Person')
    verbose_name_plural = _('Persons')


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline,)

    list_display = (
        'title',
        'type',
        'creation_date',
        'rating',
        'get_genres',
    )
    list_prefetch_related = ('genres', 'persons',)
    list_filter = ('type',)
    search_fields = ('title', 'description', 'id')

    def get_queryset(self, request):
        queryset = (
            super()
            .get_queryset(request)
            .prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genres.order_by('name')])

    get_genres.short_description = _('Genres of the film')
