from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.db import connection, reset_queries
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import Filmwork, PersonFilmwork


class MoviesApiMixin:
    model = Filmwork
    paginate_by = 50
    http_method_names = ['get']

    def get_queryset(self):
        return Filmwork.objects.prefetch_related('genres', 'persons').values(
            'id',
            'title',
            'description',
            'creation_date',
            'rating',
            'type'
        ).annotate(
            genres=ArrayAgg(
                'genres__name',
                distinct=True
            ),
            actors=ArrayAgg(
                'persons__full_name',
                filter=Q(personfilmwork__role=PersonFilmwork.RoleTypes.ACTOR),
                distinct=True
            ),
            directors=ArrayAgg(
                'persons__full_name',
                filter=Q(personfilmwork__role=PersonFilmwork.RoleTypes.DIRECTOR),
                distinct=True
            ),
            writers=ArrayAgg(
                'persons__full_name',
                filter=Q(personfilmwork__role=PersonFilmwork.RoleTypes.SCREENWRITER),
                distinct=True
            ),
        )

    def render_to_response(self, context, **kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):

    def get(self, request, *args, **kwargs):
        reset_queries()
        response = super().get(request, *args, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }
        return context

class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get(self, request, *args, **kwargs):
        reset_queries()
        response = super().get(request, *args, **kwargs)
        return response

    def get_context_data(self, object, **kwargs):
        return object
