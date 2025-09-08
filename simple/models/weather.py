from django.db import models
from django.utils import timezone


class Weather(models.Model):
    city_name = models.CharField(max_length=100, verbose_name="Название города")
    country_code = models.CharField(max_length=10, verbose_name="Код страны")

    longitude = models.FloatField(verbose_name="Долгота")
    latitude = models.FloatField(verbose_name="Широта")

    weather_id = models.IntegerField(verbose_name="ID погоды")
    weather_main = models.CharField(max_length=50, verbose_name="Основное описание")
    weather_description = models.CharField(
        max_length=100, verbose_name="Детальное описание"
    )
    weather_icon = models.CharField(max_length=10, verbose_name="Иконка")

    temperature = models.FloatField(verbose_name="Температура (K)")
    feels_like = models.FloatField(verbose_name="Ощущается как (K)")
    temp_min = models.FloatField(verbose_name="Минимальная температура (K)")
    temp_max = models.FloatField(verbose_name="Максимальная температура (K)")
    pressure = models.IntegerField(verbose_name="Давление (hPa)")
    humidity = models.IntegerField(verbose_name="Влажность (%)")

    visibility = models.IntegerField(
        verbose_name="Видимость (метры)", null=True, blank=True
    )
    wind_speed = models.FloatField(verbose_name="Скорость ветра (m/s)")
    wind_degree = models.IntegerField(verbose_name="Направление ветра (градусы)")
    wind_gust = models.FloatField(
        verbose_name="Порывы ветра (m/s)", null=True, blank=True
    )

    clouds = models.IntegerField(verbose_name="Облачность (%)")

    sunrise = models.DateTimeField(verbose_name="Восход солнца")
    sunset = models.DateTimeField(verbose_name="Закат солнца")

    api_timestamp = models.DateTimeField(verbose_name="Время данных API")
    timezone_offset = models.IntegerField(
        verbose_name="Смещение часового пояса (секунды)"
    )

    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Время создания записи"
    )

    class Meta:
        verbose_name = "Данные о погоде"
        verbose_name_plural = "Данные о погоде"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.city_name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    def celsius_temperature(self):
        """Конвертировать температуру из Кельвинов в Цельсии"""
        return round(self.temperature - 273.15, 1)

    def fahrenheit_temperature(self):
        """Конвертировать температуру из Кельвинов в Фаренгейты"""
        return round((self.temperature - 273.15) * 9 / 5 + 32, 1)
