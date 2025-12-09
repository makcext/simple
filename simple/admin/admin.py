from django.contrib import admin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.contrib import messages

from admin_auto_filters.filters import AutocompleteFilter
from admin_numeric_filter.admin import NumericFilterModelAdmin
from rangefilter.filters import DateRangeFilter
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from simple.models.models import Movie, MovieCategory, Author, Book
from simple.models.weather import Weather
from simple.processes.get_weather import get_weather_data

import logging

logger = logging.getLogger(name="backends")


class CategoryFilter(AutocompleteFilter):
    """Filter movies by category."""

    title = "Category"
    field_name = "category"


class MovieCategoryResource(resources.ModelResource):
    """Resource for import/export of movie categories."""

    movies_count = Field(attribute="movies_count", column_name="Movies Count")

    class Meta:
        model = MovieCategory
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "is_active",
            "created_at",
            "updated_at",
            "movies_count",
        )
        export_order = (
            "id",
            "name",
            "slug",
            "description",
            "is_active",
            "movies_count",
            "created_at",
            "updated_at",
        )

    def before_export(self, queryset, *args, **kwargs):
        """Optimize queryset by annotating movies count before export."""
        return queryset.annotate(movies_count=Count("movies"))

    def dehydrate_movies_count(self, category):
        """Get the count of movies for this category."""
        if hasattr(category, "movies_count"):
            return category.movies_count
        return 0


@admin.register(MovieCategory)
class MovieCategoryAdmin(ImportExportModelAdmin):
    """Admin interface for movie categories."""

    resource_class = MovieCategoryResource
    list_display = (
        "name",
        "slug",
        "description",
        "movies_count",
        "is_active",
        "created_at",
    )
    list_filter = ("created_at", "updated_at", "is_active")
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")

    show_full_result_count = False
    list_per_page = 50

    def get_queryset(self, request):
        """Optimize query by annotating movie counts."""
        queryset = super().get_queryset(request)
        return queryset.annotate(movies_count=Count("movies"))

    def movies_count(self, obj):
        """Display count of movies in this category."""
        return obj.movies_count

    movies_count.admin_order_field = "movies_count"
    movies_count.short_description = "Movies Count"


class AuthorResource(resources.ModelResource):
    """Resource for import/export of authors."""

    books_count = Field(attribute="books_count", column_name="Books Count")

    class Meta:
        model = Author
        fields = (
            "id",
            "first_name",
            "last_name",
            "biography",
            "birth_date",
            "death_date",
            "nationality",
            "is_active",
            "created_at",
            "updated_at",
            "books_count",
        )
        export_order = (
            "id",
            "first_name",
            "last_name",
            "biography",
            "birth_date",
            "death_date",
            "nationality",
            "is_active",
            "books_count",
            "created_at",
            "updated_at",
        )

    def before_export(self, queryset, *args, **kwargs):
        """Optimize queryset by annotating books count before export."""
        return queryset.annotate(books_count=Count("books"))

    def dehydrate_books_count(self, author):
        """Get the count of books for this author."""
        if hasattr(author, "books_count"):
            return author.books_count
        return 0


@admin.register(Author)
class AuthorAdmin(ImportExportModelAdmin):
    """Admin interface for authors."""

    resource_class = AuthorResource
    list_display = (
        "first_name",
        "last_name",
        "biography_short",
        "birth_date",
        "death_date",
        "nationality",
        "books_count",
        "is_active",
    )
    list_filter = ("is_active", "nationality")
    search_fields = ("first_name", "last_name", "biography")
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 50

    def get_queryset(self, request):
        """Optimize query by annotating book counts."""
        queryset = super().get_queryset(request)
        return queryset.annotate(books_count=Count("books"))

    def biography_short(self, obj):
        """Short version of biography for list display."""
        return obj.biography[:100] + "..." if obj.biography else ""

    biography_short.short_description = "Biography"

    def books_count(self, obj):
        """Display count of books for this author."""
        return obj.books_count

    books_count.admin_order_field = "books_count"
    books_count.short_description = "Books Count"


class BookResource(resources.ModelResource):
    """Resource for import/export of books."""

    author_name = Field(attribute="get_author_name", column_name="Author")

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "original_title",
            "slug",
            "description",
            "publication_date",
            "isbn",
            "page_count",
            "author",
            "author_name",
            "is_active",
            "created_at",
            "updated_at",
        )
        export_order = (
            "id",
            "title",
            "original_title",
            "slug",
            "description",
            "publication_date",
            "isbn",
            "page_count",
            "author_name",
            "is_active",
            "created_at",
            "updated_at",
        )


@admin.register(Book)
class BookAdmin(ImportExportModelAdmin):
    """Admin interface for books."""

    resource_class = BookResource
    list_display = (
        "title",
        "author",
        "publication_date",
        "page_count",
        "isbn",
        "is_active",
    )
    list_filter = (
        "is_active",
        ("publication_date", DateRangeFilter),
        "author",
    )
    search_fields = (
        "title",
        "original_title",
        "isbn",
        "author__first_name",
        "author__last_name",
    )
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    list_select_related = ("author",)
    list_per_page = 50

    fieldsets = (
        (None, {"fields": ("title", "original_title", "slug", "description")}),
        (
            "Details",
            {
                "fields": (
                    "author",
                    "publication_date",
                    "isbn",
                    "page_count",
                )
            },
        ),
        ("Status", {"fields": ("is_active", "created_at", "updated_at")}),
    )

    actions = ["mark_as_active", "mark_as_inactive"]

    def mark_as_active(self, request, queryset):
        """Mark selected books as active."""
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f"{updated} {'books were' if updated != 1 else 'book was'} marked as active.",
        )

    def mark_as_inactive(self, request, queryset):
        """Mark selected books as inactive."""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f"{updated} {'books were' if updated != 1 else 'book was'} marked as inactive.",
        )


@admin.register(Movie)
class MovieAdmin(NumericFilterModelAdmin):
    """Admin interface for movies."""

    list_display = (
        "title",
        "director",
        "release_date",
        "is_active",
        "display_duration",
        "display_rating",
        "display_category",
        "is_released",
    )
    list_filter = (
        "is_active",
        ("release_date", DateRangeFilter),
        CategoryFilter,
    )
    search_fields = ("title", "original_title")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    list_select_related = ("category",)
    list_per_page = 50
    show_full_result_count = False

    ordering = ("-release_date", "title")

    fieldsets = (
        (None, {"fields": ("title", "original_title", "slug", "description")}),
        (
            "Details",
            {
                "fields": (
                    "director",
                    "duration_minutes",
                    "rating",
                    "release_date",
                    "category",
                )
            },
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
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"

    display_duration.short_description = "Duration"
    display_duration.admin_order_field = "duration_minutes"

    def display_rating(self, obj):
        """Display rating."""
        if not obj.rating:
            return "-"
        return obj.rating

    display_rating.short_description = "Rating"
    display_rating.admin_order_field = "rating"

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
            f"{updated} {'movies were' if updated != 1 else 'movie was'} marked as active.",
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
            f"{updated} {'movies were' if updated != 1 else 'movie was'} marked as inactive.",
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


class WeatherResource(resources.ModelResource):
    """Resource for import/export of weather data."""

    temperature_celsius = Field(attribute="temperature_celsius", column_name="Temperature (°C)")
    temperature_fahrenheit = Field(
        attribute="temperature_fahrenheit", column_name="Temperature (°F)"
    )

    class Meta:
        model = Weather
        fields = (
            "id",
            "city_name",
            "country_code",
            "temperature_celsius",
            "temperature_fahrenheit",
            "weather_main",
            "weather_description",
            "pressure",
            "humidity",
            "wind_speed",
            "clouds",
            "created_at",
        )
        export_order = (
            "id",
            "city_name",
            "country_code",
            "temperature_celsius",
            "temperature_fahrenheit",
            "weather_main",
            "weather_description",
            "pressure",
            "humidity",
            "wind_speed",
            "clouds",
            "created_at",
        )


@admin.register(Weather)
class WeatherAdmin(ImportExportModelAdmin):
    """Admin interface for weather data."""

    resource_class = WeatherResource
    list_display = (
        "city_name",
        "temperature_celsius_display",
        "weather_description",
        "humidity",
        "pressure",
        "wind_speed",
        "created_at",
    )
    list_filter = (
        "city_name",
        "weather_main",
        ("created_at", DateRangeFilter),
    )
    search_fields = ("city_name", "weather_description", "weather_main")
    readonly_fields = (
        "created_at",
        "updated_at",
        "api_timestamp",
        "temperature_celsius",
        "temperature_fahrenheit",
        "feels_like_celsius",
        "feels_like_fahrenheit",
        "temp_min",
        "temp_max",
    )
    list_per_page = 50
    show_full_result_count = False

    actions = ["fetch_weather_action", "delete_old_records"]

    def fetch_weather_action(self, request, queryset=None):
        """Admin action to fetch current weather data."""
        success, message = get_weather_data()

        if success:
            self.message_user(request, message, messages.SUCCESS)
            logger.info(
                "Weather data fetched successfully via admin action",
                extra={
                    "user_id": request.user.id,
                    "username": request.user.username,
                },
            )
        else:
            self.message_user(
                request, f"Failed to fetch weather data: {message}", messages.ERROR
            )
            logger.error(
                "Failed to fetch weather data via admin action",
                extra={
                    "user_id": request.user.id,
                    "username": request.user.username,
                    "error": message,
                },
            )

        return HttpResponseRedirect(request.get_full_path())

    fetch_weather_action.short_description = "Get current weather data"
    fetch_weather_action.allowed_permissions = ("change",)

    def temperature_celsius_display(self, obj):
        """Display temperature in Celsius."""
        return f"{obj.temperature_celsius}°C"

    temperature_celsius_display.short_description = "Temperature"
    temperature_celsius_display.admin_order_field = "temperature"

    def temperature_fahrenheit_display(self, obj):
        """Display temperature in Fahrenheit."""
        return f"{obj.temperature_fahrenheit}°F"

    temperature_fahrenheit_display.short_description = "Temperature (F)"

    def delete_old_records(self, request, queryset):
        """Delete weather records older than 30 days."""
        from django.utils import timezone
        from datetime import timedelta

        if not queryset.exists():
            queryset = self.get_queryset(request)

        cutoff_date = timezone.now() - timedelta(days=30)
        old_records = queryset.filter(created_at__lt=cutoff_date)
        count = old_records.count()

        if count > 0:
            old_records.delete()
            self.message_user(
                request,
                f"Successfully deleted {count} old weather records.",
                messages.SUCCESS,
            )
            logger.info(
                "Deleted old weather records",
                extra={
                    "user_id": request.user.id,
                    "username": request.user.username,
                    "count": count,
                },
            )
        else:
            self.message_user(
                request,
                "No old weather records found to delete.",
                messages.INFO,
            )

    delete_old_records.short_description = "Delete records older than 30 days"

    def get_actions(self, request):
        """Override to ensure actions are properly configured."""
        actions = super().get_actions(request)

        if "fetch_weather_action" in actions:

            def fetch_wrapper(modeladmin, request, queryset):
                return self.fetch_weather_action(request, queryset)

            fetch_wrapper.short_description = "Get current weather data"
            fetch_wrapper.allowed_permissions = ("change",)

            actions["fetch_weather_action"] = (
                fetch_wrapper,
                "fetch_weather_action",
                "Get current weather data",
            )

        return actions

    def changelist_view(self, request, extra_context=None):
        """Custom changelist view to handle actions without selection."""
        if request.method == "POST":
            if "action" in request.POST and request.POST["action"] == "fetch_weather_action":
                return self.fetch_weather_action(request, None)

        return super().changelist_view(request, extra_context)

    def has_fetch_weather_permission(self, request):
        """Check if user has permission to fetch weather."""
        return request.user.has_perm("simple.change_weather")
