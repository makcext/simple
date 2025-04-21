from datetime import date

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class MovieCategory(models.Model):
    """
    Model for movie categories.

    Allows classification of movies by various genres and types.
    """

    name = models.CharField(
        verbose_name="Name",
        max_length=100,
        unique=True,
        help_text="Category name (e.g. Action, Drama, Comedy)",
    )
    description = models.TextField(
        verbose_name="Description",
        blank=True,
        help_text="Description of this category",
    )
    slug = models.SlugField(
        verbose_name="Slug",
        unique=True,
        max_length=100,
        help_text="URL-friendly name",
    )
    is_active = models.BooleanField(
        verbose_name="Active",
        default=True,
        help_text="Whether this category is active and should be displayed",
    )
    created_at = models.DateTimeField(
        verbose_name="Created at",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="Updated at",
        auto_now=True,
    )

    class Meta:
        verbose_name = "Movie Category"
        verbose_name_plural = "Movie Categories"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self) -> str:
        """
        String representation of the category.

        Returns:
            str: The name of the category.
        """
        return self.name

    def clean(self) -> None:
        """Validate the model."""
        super().clean()
        if not self.slug and self.name:
            from django.utils.text import slugify

            self.slug = slugify(self.name)


class Movie(models.Model):
    """
    Movie model.

    Contains all information about a movie, including title, description, rating,
    duration and relationship with category.
    """

    title = models.CharField(
        verbose_name="Title",
        max_length=255,
        help_text="Movie title",
    )
    original_title = models.CharField(
        verbose_name="Original Title",
        max_length=255,
        blank=True,
        help_text="Original title if different from main title",
    )
    slug = models.SlugField(
        verbose_name="Slug",
        unique=True,
        max_length=255,
        help_text="URL-friendly title",
    )
    description = models.TextField(
        verbose_name="Description",
        blank=True,
        help_text="Movie plot summary",
    )
    release_date = models.DateField(
        verbose_name="Release Date",
        null=True,
        blank=True,
        help_text="Movie release date",
    )
    duration_minutes = models.PositiveIntegerField(
        verbose_name="Duration (minutes)",
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1, "Duration must be at least 1 minute"),
            MaxValueValidator(600, "Duration cannot exceed 600 minutes"),
        ],
        help_text="Movie duration in minutes",
    )
    rating = models.DecimalField(
        verbose_name="Rating",
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0.0, "Rating cannot be less than 0"),
            MaxValueValidator(10.0, "Rating cannot exceed 10"),
        ],
        help_text="Movie rating (0-10)",
    )
    director = models.CharField(
        verbose_name="Director",
        max_length=255,
        blank=True,
        help_text="Movie director",
    )
    category = models.ForeignKey(
        MovieCategory,
        verbose_name="Category",
        on_delete=models.PROTECT,
        related_name="movies",
        help_text="Movie category",
    )
    is_active = models.BooleanField(
        verbose_name="Active",
        default=True,
        help_text="Whether this movie is active and should be displayed",
    )
    created_at = models.DateTimeField(
        verbose_name="Created at",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="Updated at",
        auto_now=True,
    )

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"
        ordering = ["-release_date", "title"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["release_date"]),
            models.Index(fields=["rating"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self) -> str:
        """
        String representation of the movie.

        Returns:
            str: The title of the movie.
        """
        return self.title

    def clean(self) -> None:
        """Validate the model."""
        super().clean()
        if not self.slug and self.title:
            from django.utils.text import slugify

            self.slug = slugify(self.title)

    @property
    def get_category_name(self) -> str:
        """
        Returns the name of the movie category.

        Returns:
            str: Category name.
        """
        return self.category.name if self.category else ""

    @property
    def is_released(self) -> bool:
        """
        Checks if the movie is released (release date is in the past).

        Returns:
            bool: True if the movie is released, False otherwise.
        """
        if not self.release_date:
            return False
        return self.release_date <= date.today()
