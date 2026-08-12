from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.constraints import UniqueConstraint


def capitalize_str(words: str) -> str:
    return " ".join([word.capitalize() for word in words.split()])


class Country(models.Model):
    name = models.CharField(max_length=64, unique=True)
    code = models.CharField(
        max_length=2,
        unique=True,
        help_text="Enter the two-letter ISO country code"
    )

    class Meta:
        verbose_name_plural = "countries"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.code}"

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        self.name = capitalize_str(self.name)
        super().save(*args, **kwargs)


class City(models.Model):
    name = models.CharField(max_length=64)
    country = models.ForeignKey(
        "Country", on_delete=models.CASCADE, related_name="cities"
    )

    class Meta:
        verbose_name_plural = "cities"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.name = capitalize_str(self.name)
        super().save(*args, **kwargs)


class Airport(models.Model):
    name = models.CharField(max_length=255, unique=True)
    timezone = models.CharField(
        max_length=5,
        default="+0",
        help_text="Enter the country's time zone (min: -12, max: +14)"
    )
    city = models.ForeignKey(
        "City", on_delete=models.CASCADE, related_name="airports"
    )

    class Meta:
        verbose_name_plural = "airports"
        ordering = ["city"]

    def __str__(self):
        return f"{self.name} {self.timezone}"


class Route(models.Model):
    distance = models.PositiveIntegerField(
        help_text="Enter the distance in kilometers",
        validators=[MinValueValidator(2), MaxValueValidator(20_000)]
    )
    duration = models.PositiveIntegerField(
        help_text="Enter the duration in minutes",
        validators=[MinValueValidator(5), MaxValueValidator(1_200)]
    )
    source = models.ForeignKey(
        "Airport", on_delete=models.CASCADE, related_name="sources"
    )
    destination = models.ForeignKey(
        "Airport", on_delete=models.CASCADE, related_name="destinations"
    )

    @property
    def duration_in_hours(self) -> float:
        return round(self.duration / 60, 1)

    class Meta:
        verbose_name_plural = "routes"
        ordering = ["distance"]
        constraints = [
            models.UniqueConstraint(
                fields=["source", "destination"],
                name="unique_route",
            ),
        ]

    def __str__(self):
        return f"{self.source} -> {self.destination}"


class AirplaneType(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)


class Airplane(models.Model):
    model = models.CharField(max_length=255)
    rows = models.PositiveIntegerField()
    seats_per_row = models.PositiveIntegerField()
    airplane_type = models.ForeignKey(
        "AirplaneType", on_delete=models.CASCADE, related_name="airplanes"
    )

    @property
    def capacity(self):
        return self.rows * self.seats_per_row

    class Meta:
        verbose_name_plural = "airplanes"
        ordering = ["model"]

    def __str__(self):
        return f"{self.model} - {self.capacity} seats"


class Crew(models.Model):
    ROLE_CHOICES = [
        ("FIRST_PILOT", "First pilot"),
        ("SECOND_PILOT", "Second pilot"),
        ("FLIGHT_MECHANIC", "Flight mechanic"),
        ("FLIGHT_ATTENDANT", "Flight attendant"),
    ]

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    experience = models.PositiveIntegerField(
        help_text="Enter work experience in years. (1-50)",
        validators=[MinValueValidator(1), MaxValueValidator(50)]
    )
    role = models.CharField(
        max_length=64, choices=ROLE_CHOICES, default="FLIGHT_ATTENDANT"
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name_plural = "crews"
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.full_name} - {self.role} {self.experience} years"

    def save(self, *args, **kwargs):
        self.first_name = capitalize_str(self.first_name)
        self.last_name = capitalize_str(self.last_name)
        super().save(*args, **kwargs)


class Flight(models.Model):
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    route = models.ForeignKey(
        "Route", on_delete=models.CASCADE, related_name="flights"
    )
    airplane = models.ForeignKey(
        "Airplane", on_delete=models.CASCADE, related_name="flights"
    )
    crew = models.ManyToManyField("Crew", related_name="flights")

    class Meta:
        verbose_name_plural = "flights"
        ordering = ["-departure_time"]

    def __str__(self):
        return f"{self.route} - {self.airplane}"


class Order(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]

    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="PENDING"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )

    class Meta:
        verbose_name_plural = "orders"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk} - {self.status} - {self.user}"


class Ticket(models.Model):
    CLASS_CHOICES = [
        ("ECONOMY", "Economy"),
        ("PREMIUM_ECONOMY", "Premium Economy"),
        ("BUSINESS", "Business"),
        ("FIRST", "First"),
    ]

    row_number = models.PositiveIntegerField()
    seat_number = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    seat_class = models.CharField(
        max_length=30, choices=CLASS_CHOICES, default="ECONOMY"
    )
    flight = models.ForeignKey(
        "Flight", on_delete=models.CASCADE, related_name="tickets"
    )
    passenger = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    order = models.ForeignKey(
        "Order", on_delete=models.CASCADE, related_name="tickets"
    )

    class Meta:
        verbose_name_plural = "tickets"
        ordering = ["-created_at"]
        constraints = [
            UniqueConstraint(
                fields=["flight", "seat_number", "row_number"],
                name="unique_flight_seat",
            )
        ]

    def __str__(self):
        return f"{self.seat_class}: {self.row_number}/{self.seat_number}"


class Baggage(models.Model):
    length = models.PositiveIntegerField()  # cm
    height = models.PositiveIntegerField()  # cm
    width = models.PositiveIntegerField()  # cm
    weight = models.DecimalField(max_digits=5, decimal_places=2)  # kg
    ticket = models.ForeignKey(
        "Ticket", on_delete=models.CASCADE, related_name="baggage"
    )

    @property
    def volume(self) -> int:
        return self.height * self.width * self.length

    def __str__(self):
        return f"{self.volume}/{self.weight} - {self.ticket}"
