from django.db.models import Q
from .models import Film

class FilterStrategy:
    def filter(self, query):
        raise NotImplementedError("Filter method not implemented")

class TitleOrDirectorFilterStrategy(FilterStrategy):
    def filter(self, query):
        return Film.objects.filter(Q(title__icontains=query) | Q(director__icontains=query))

class AllFilmsStrategy(FilterStrategy):
    def filter(self, query):
        return Film.objects.all()