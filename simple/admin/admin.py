from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html

from admin_auto_filters.filters import AutocompleteFilter
from admin_numeric_filter.admin import NumericFilterModelAdmin
from rangefilter.filters import DateRangeFilter
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from simple.models.models import Movie, MovieCategory, Author, Book

import logging


logger = logging.getLogger(name="backends")


class CategoryFilter(AutocompleteFilter):
    """Filter movies by category."""
    title = "Category"
    field_name = "category"


class AuthorFilter(AutocompleteFilter):
    """Filter books by author."""
    title = "Author"
    field_name = "author"


class MovieCategoryResource(resources.ModelResource):
    """Resource for import/export of movie categories."""

    movies_count = Field(
        attribute="movies_count",
        column_name="Movies Count"
    )

    class Meta:
        model = MovieCategory
        fields = (
            "id", "name", "slug", "description",
            "is_active", "movies_count"
        )
        export_order = fields

    def before_export(self, queryset, *args, **kwargs):
        """Optimize queryset by annotating movies count before export.""" 
        return queryset.annotate(movies_count=Count("movies"))

    def dehydrate_movies_count(self, category):
        """Get the count of movies for this category."""
        return getattr(category, "movies_count", 0)


class AuthorResource(resources.ModelResource):
    """Resource for importing/exporting authors."""

    books_count = Field(
        attribute="books_count",
        column_name="Books Count"
    )

    class Meta:
        model = Author
        fields = (
            "id", "last_name", "first_name",
            "nationality", "birth_date",
            "is_active", "books_count"
        )
        export_order = fields

    def before_export(self, queryset, *args, **kwargs):
        """Annotates the number of books before exporting."""
        return queryset.annotate(books_count=Count("books"))

    def dehydrate_books_count(self, author):
        """Returns the number of books by the author."""
        return getattr(author, "books_count", 0)


class BookResource(resources.ModelResource):
    """Resource for importing/exporting books."""

    class Meta:
        model = Book
        fields = (
            "id", "title", "author",
            "publication_date", "isbn", "is_active"
        )
        export_order = fields


@admin.register(MovieCategory)
class MovieCategoryAdmin(ImportExportModelAdmin):
    """Admin panel for movie categories."""

    resource_class = MovieCategoryResource
    list_display = (
        "name", "slug", "is_active",
        "movies_count", "created_at"
    )
    list_filter = ("is_active", ("created_at", DateRangeFilter))
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 30

    def get_queryset(self, request):
        """Returns a QuerySet with an annotation of the number of movies."""
        return super().get_queryset(request).annotate(
            movies_count=Count("movies")
        )

    def movies_count(self, obj):
        """Displays the number of movies in a category."""
        return obj.movies_count

    movies_count.admin_order_field = "movies_count"
    movies_count.short_description = "Movies Count"


@admin.register(Movie)
class MovieAdmin(NumericFilterModelAdmin):
    """Admin interface for movies."""

    list_display = (
        "title",
        "director",
        "display_category",
        "release_date",
        "display_duration",
        "display_rating",
        "is_active",
    )
    list_filter = (
        "is_active",
        ("release_date", DateRangeFilter),
        CategoryFilter,
    )
    search_fields = ("title", "director")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    list_select_related = ("category",)
    list_per_page = 30
    ordering = ("-release_date", "title")

    fieldsets = (
        (None, {"fields": ("title", "slug", "description")}),
        (
            "Details",
            {
                "fields": (
                    "director", "duration_minutes",
                    "rating", "release_date", "category"
                )
            }
        ),
        ("Status", {"fields": ("is_active", "created_at", "updated_at")}),
    )
    
    def get_queryset(self, request):
        """Optimize query by selecting related category."""
        queryset = super().get_queryset(request)
        return queryset.select_related("category")

    def display_duration(self, obj):
        """Format duration in hours and minutes."""
        if not obj.duration_minutes:
            return "-"
        hours, minutes = divmod(obj.duration_minutes, 60)
        return f"{hours}h {minutes}m" if hours else f"{minutes}m"

    display_duration.short_description = "Duration"

    def display_rating(self, obj):
        """Display rating."""
        return obj.rating or "-"

    display_rating.short_description = "Rating"

    def display_category(self, obj):
        """Display category name."""
        if obj.category:
            return obj.category.name
        return "-"

    display_category.short_description = "Category"
    display_category.admin_order_field = "category__name"

    def is_released(self, obj):
        """Check if movie is released."""
        return obj.is_released

    is_released.short_description = "Released"
    is_released.boolean = True

    actions = ["mark_as_active", "mark_as_inactive"]

    def mark_as_active(self, request, queryset):
        """Mark selected movies as active."""
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f"{updated} {'movies were' if updated != 1 else 'movie was'} "
            f"marked as active.",
        )
        logger.info(
            "Admin user marked movies as active",
            extra={
                "user_id": request.user.id,
                "username": request.user.username,
                "count": updated,
            },
        )

    mark_as_active.short_description = "Mark selected movies as active"

    def mark_as_inactive(self, request, queryset):
        """Mark selected movies as inactive."""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f"{updated} {'movies were' if updated != 1 else 'movie was'} "
            f"marked as inactive.",
        )
        logger.info(
            "Admin user marked movies as inactive",
            extra={
                "user_id": request.user.id,
                "username": request.user.username,
                "count": updated,
            },
        )

    mark_as_inactive.short_description = "Mark selected movies as inactive"


@admin.register(Author)
class AuthorAdmin(ImportExportModelAdmin):
    """Admin panel for authors."""

    resource_class = AuthorResource
    list_display = (
        "last_name",
        "first_name",
        "nationality",
        "books_count",
        "is_active",
        "created_at"
    )
    list_filter = (
        "is_active",
        "nationality",
        ("birth_date", DateRangeFilter),
    )
    search_fields = ("last_name", "first_name", "biography")
    readonly_fields = ("created_at", "updated_at")  # Убрано prepopulated_fields
    list_per_page = 30
    ordering = ("last_name", "first_name")

    fieldsets = (
        (None, {"fields": ("first_name", "last_name", "nationality")}),
        (
            "Biography",
            {
                "fields": ("birth_date", "death_date", "biography"),
                "classes": ("collapse",)
            }
        ),
        ("Status", {"fields": ("is_active", "created_at", "updated_at")}),
    )

    def get_queryset(self, request):
        """Returns a QuerySet with an annotation of the number of books."""
        return super().get_queryset(request).annotate(
            books_count=Count("books")
        )

    def books_count(self, obj):
        """Displays the number of books by the author."""
        return obj.books_count

    books_count.admin_order_field = "books_count"
    books_count.short_description = "Books Count"


@admin.register(Book)
class BookAdmin(ImportExportModelAdmin):
    """Admin interface for books."""

    resource_class = BookResource
    list_display = (
        "title",
        "display_author",
        "publication_date",
        "isbn",
        "is_active",
        "created_at"
    )
    list_filter = (
        "is_active",
        ("publication_date", DateRangeFilter),
        AuthorFilter,
    )
    search_fields = ("title", "original_title", "isbn", "description")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    list_select_related = ("author",)
    list_per_page = 30
    ordering = ("-publication_date", "title")

    fieldsets = (
        (None, {"fields": ("title", "slug", "author", "description")}),
        (
            "Details",
            {
                "fields": (
                    "original_title",
                    "publication_date",
                    "isbn",
                    "page_count"
                )
            }
        ),
        ("Status", {"fields": ("is_active", "created_at", "updated_at")}),
    )

    def display_author(self, obj):
        """Displays the author with a link to his edit page."""
        if obj.author:
            return format_html(
                '<a href="/admin/simple/author/{}/change/">{}</a>',
                obj.author.id,
                f"{obj.author.last_name} {obj.author.first_name}"
            )
        return "-"

    display_author.short_description = "Author"
    display_author.admin_order_field = "author__last_name"

    actions = ["mark_as_active", "mark_as_inactive"]

    def mark_as_active(self, request, queryset):
        """Mark selected books as active."""
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f"{updated} {'books were' if updated != 1 else 'book was'} "
            f"marked as active.",
        )
        logger.info(
            "Admin user marked books as active",
            extra={
                "user_id": request.user.id,
                "username": request.user.username,
                "count": updated,
            },
        )

    mark_as_active.short_description = "Mark selected books as active"

    def mark_as_inactive(self, request, queryset):
        """Mark selected books as inactive."""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f"{updated} {'books were' if updated != 1 else 'book was'} "
            f"marked as inactive.",
        )
        logger.info(
            "Admin user marked books as inactive",
            extra={
                "user_id": request.user.id,
                "username": request.user.username,
                "count": updated,
            },
        )

    mark_as_inactive.short_description = "Mark selected books as inactive"