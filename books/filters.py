import django_filters.rest_framework as filters

from books.models import Author, Book, Genre


class BookFilters(filters.FilterSet):
    title = filters.CharFilter(lookup_expr="icontains")
    genres = filters.ModelMultipleChoiceFilter(
        queryset=Genre.objects.all(), label="Genres"
    )
    authors = filters.ModelMultipleChoiceFilter(
        queryset=Author.objects.all(), label="Authors"
    )

    class Meta:
        model = Book
        fields = (
            "title",
            "genres",
            "authors",
            "pub_date",
        )
