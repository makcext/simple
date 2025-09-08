from datetime import date, datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class MovieCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Movie Category"
        verbose_name_plural = "Movie Categories"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if not self.slug and self.name:
            from django.utils.text import slugify
            self.slug = slugify(self.name)


class Movie(models.Model):
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField(blank=True)
    release_date = models.DateField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(600)]
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )
    director = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey(MovieCategory, on_delete=models.PROTECT, related_name="movies")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if not self.slug and self.title:
            from django.utils.text import slugify
            self.slug = slugify(self.title)

    @property
    def get_category_name(self):
        return self.category.name if self.category else ""

    @property
    def is_released(self):
        if not self.release_date:
            return False
        return self.release_date <= date.today()


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    biography = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ["last_name", "first_name"]
        indexes = [
            models.Index(fields=["last_name"]),
            models.Index(fields=["first_name"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField(blank=True)
    publication_date = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=20, blank=True)
    page_count = models.PositiveIntegerField(null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name="books")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ["-publication_date", "title"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["publication_date"]),
            models.Index(fields=["author"]),
        ]

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if not self.slug and self.title:
            from django.utils.text import slugify
            self.slug = slugify(self.title)

    @property
    def get_author_name(self):
        return str(self.author) if self.author else ""

    @property
    def is_published(self):
        if not self.publication_date:
            return False
        return self.publication_date <= date.today()


class Weather(models.Model):
    city_name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10)
    longitude = models.FloatField(validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])
    latitude = models.FloatField(validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)])
    weather_id = models.IntegerField()
    weather_main = models.CharField(max_length=50)
    weather_description = models.CharField(max_length=100)
    weather_icon = models.CharField(max_length=10)
    temperature = models.FloatField(validators=[MinValueValidator(0.0)])
    feels_like = models.FloatField(validators=[MinValueValidator(0.0)])
    temp_min = models.FloatField(validators=[MinValueValidator(0.0)])
    temp_max = models.FloatField(validators=[MinValueValidator(0.0)])
    pressure = models.IntegerField(validators=[MinValueValidator(800), MaxValueValidator(1100)])
    humidity = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    visibility = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    wind_speed = models.FloatField(validators=[MinValueValidator(0.0)])
    wind_degree = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(360)])
    wind_gust = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0)])
    clouds = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    sunrise = models.DateTimeField()
    sunset = models.DateTimeField()
    api_timestamp = models.DateTimeField()
    timezone_offset = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Weather Data"
        verbose_name_plural = "Weather Data"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["city_name"]),
            models.Index(fields=["country_code"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["api_timestamp"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["weather_main"]),
            models.Index(fields=["temperature"]),
        ]

    def __str__(self):
        return f"{self.city_name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    def celsius_temperature(self):
        return round(self.temperature - 273.15, 1)

    def fahrenheit_temperature(self):
        return round((self.temperature - 273.15) * 9/5 + 32, 1)

    def celsius_feels_like(self):
        return round(self.feels_like - 273.15, 1)

    def fahrenheit_feels_like(self):
        return round((self.feels_like - 273.15) * 9/5 + 32, 1)

    def visibility_km(self):
        if self.visibility is not None:
            return round(self.visibility / 1000, 1)
        return None

    @property
    def is_current(self):
        return (timezone.now() - self.created_at).total_seconds() < 3600

    def clean(self):
        super().clean()
        if self.temp_min > self.temp_max:
            raise ValidationError("Minimum temperature cannot be greater than maximum temperature")
        if self.temp_min > self.temperature or self.temp_max < self.temperature:
            raise ValidationError("Current temperature must be between minimum and maximum temperatures")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
