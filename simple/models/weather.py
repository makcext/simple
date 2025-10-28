from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Weather(models.Model):
    """
    Model for weather data from OpenWeatherMap API.
    Stores comprehensive weather information for specific locations and times.
    """

    city_name = models.CharField(
        verbose_name="City Name",
        max_length=100,
        help_text="Name of the city for weather data",
    )
    country_code = models.CharField(
        verbose_name="Country Code",
        max_length=10,
        help_text="ISO country code (e.g., RU, US, GB)",
    )
    longitude = models.FloatField(
        verbose_name="Longitude",
        validators=[
            MinValueValidator(-180.0, "Longitude too low"),
            MaxValueValidator(180.0, "Longitude too high"),
        ],
        help_text="Geographical longitude coordinate",
    )
    latitude = models.FloatField(
        verbose_name="Latitude",
        validators=[
            MinValueValidator(-90.0, "Latitude too low"),
            MaxValueValidator(90.0, "Latitude too high"),
        ],
        help_text="Geographical latitude coordinate",
    )
    weather_id = models.IntegerField(
        verbose_name="Weather ID",
        help_text="OpenWeatherMap weather condition ID",
    )
    weather_main = models.CharField(
        verbose_name="Weather Main",
        max_length=50,
        help_text="Weather parameters group",
    )
    weather_description = models.CharField(
        verbose_name="Weather Description",
        max_length=100,
        help_text="Weather condition within the group",
    )
    weather_icon = models.CharField(
        verbose_name="Weather Icon",
        max_length=10,
        help_text="Weather icon code",
    )
    temperature = models.FloatField(
        verbose_name="Temperature",
        help_text="Temperature value in Kelvin",
    )
    feels_like = models.FloatField(
        verbose_name="Feels Like",
        help_text="Human perception of temperature",
    )
    temp_min = models.FloatField(
        verbose_name="Min Temperature",
        help_text="Minimum temperature",
    )
    temp_max = models.FloatField(
        verbose_name="Max Temperature",
        help_text="Maximum temperature",
    )
    pressure = models.IntegerField(
        verbose_name="Pressure (hPa)",
        validators=[
            MinValueValidator(800, "Pressure too low"),
            MaxValueValidator(1100, "Pressure too high"),
        ],
        help_text="Atmospheric pressure in hPa",
    )
    humidity = models.IntegerField(
        verbose_name="Humidity (%)",
        validators=[
            MinValueValidator(0, "Humidity too low"),
            MaxValueValidator(100, "Humidity too high"),
        ],
        help_text="Humidity percentage",
    )
    visibility = models.IntegerField(
        verbose_name="Visibility (m)",
        null=True,
        blank=True,
        help_text="Visibility in meters",
    )
    wind_speed = models.FloatField(
        verbose_name="Wind Speed (m/s)",
        validators=[
            MinValueValidator(0.0, "Wind speed negative"),
        ],
        help_text="Wind speed in meters per second",
    )
    wind_degree = models.IntegerField(
        verbose_name="Wind Degree",
        validators=[
            MinValueValidator(0, "Wind degree too low"),
            MaxValueValidator(360, "Wind degree too high"),
        ],
        help_text="Wind direction in degrees",
    )
    clouds = models.IntegerField(
        verbose_name="Cloudiness (%)",
        validators=[
            MinValueValidator(0, "Cloudiness too low"),
            MaxValueValidator(100, "Cloudiness too high"),
        ],
        help_text="Cloudiness percentage",
    )
    sunrise = models.DateTimeField(
        verbose_name="Sunrise",
        help_text="Sunrise time",
    )
    sunset = models.DateTimeField(
        verbose_name="Sunset",
        help_text="Sunset time",
    )
    api_timestamp = models.DateTimeField(
        verbose_name="API Timestamp",
        help_text="Time when data was received from API",
    )
    timezone_offset = models.IntegerField(
        verbose_name="Timezone Offset",
        help_text="Shift in seconds from UTC",
    )
    is_active = models.BooleanField(
        verbose_name="Active",
        default=True,
        help_text="Whether weather record is active",
    )
    created_at = models.DateTimeField(
        verbose_name="Created At",
        auto_now_add=True,
        help_text="Time when record was created",
    )
    updated_at = models.DateTimeField(
        verbose_name="Updated At",
        auto_now=True,
        help_text="Time when record was updated",
    )

    class Meta:
        verbose_name = "Weather Data"
        verbose_name_plural = "Weather Data"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["city_name"]),
            models.Index(fields=["country_code"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["weather_main"]),
            models.Index(fields=["temperature"]),
        ]

    def __str__(self):
        """String representation of the weather data."""
        return f"{self.city_name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    @property
    def temperature_celsius(self):
        """Convert temperature from Kelvin to Celsius."""
        return round(self.temperature - 273.15, 2)

    @property
    def temperature_fahrenheit(self):
        """Convert temperature from Kelvin to Fahrenheit."""
        return round((self.temperature - 273.15) * 9/5 + 32, 2)

    @property
    def temperature_celsius(self) -> float:
        return self.temperature

    @property
    def temperature_fahrenheit(self) -> float:
        return round((self.temperature * 9/5) + 32, 1)

    def clean(self):
        """Validate the model."""
        super().clean()
