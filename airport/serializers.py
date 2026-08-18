from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from airport.models import (
    Country,
    City,
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight,
    Order,
    Ticket,
    Baggage,
)


TICKET_PRICES = {
    "ECONOMY": (Decimal("50.00"), Decimal("0.01")),
    "PREMIUM_ECONOMY": (Decimal("75.00"), Decimal("0.015")),
    "BUSINESS": (Decimal("100.00"), Decimal("0.02")),
    "FIRST": (Decimal("150.00"), Decimal("0.025")),
}

def calculate_ticket_price(seat_class: str, distance: int) -> Decimal:
    base_price, distance_rate = TICKET_PRICES[seat_class]
    return base_price + Decimal(distance) * distance_rate


# SHORT-CITY
class CityShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name")


# SHORT-AIRPORT
class AirportShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name")


# COUNTRY
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("id", "name", "code")


class CountryListSerializer(serializers.ModelSerializer):
    cities_count = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ("id", "name", "code", "cities_count")

    def get_cities_count(self, obj):
        return obj.cities.count()


class CountryRetrieveSerializer(serializers.ModelSerializer):
    cities = CityShortSerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ("id", "name", "code", "cities")


# CITY
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name", "country")


class CityListSerializer(CitySerializer):
    country = serializers.SlugRelatedField(read_only=True, slug_field="name")


class CityRetrieveSerializer(CityListSerializer):
    airports = AirportShortSerializer(read_only=True, many=True)

    class Meta(CityListSerializer.Meta):
        fields = CityListSerializer.Meta.fields + ("airports",)

# AIRPORT
class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "city", "timezone")


class AirportListSerializer(serializers.ModelSerializer):
    city = CityShortSerializer(read_only=True)

    class Meta:
        model = Airport
        fields = ("id", "name", "city")


class AirportRetrieveSerializer(AirportSerializer):
    city = CityShortSerializer(read_only=True)


# ROUTE
class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance", "duration")


class RouteListSerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(
        read_only=True, slug_field="name"
    )
    destination = serializers.SlugRelatedField(
        read_only=True, slug_field="name"
    )

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "duration_in_hours")


class RouteRetrieveSerializer(RouteListSerializer):
    class Meta(RouteListSerializer.Meta):
        fields = RouteListSerializer.Meta.fields + ("distance", "duration")


# AIRPLANETYPE
class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneTypeListSerializer(AirplaneTypeSerializer):
    airplane_count = serializers.SerializerMethodField()

    class Meta(AirplaneTypeSerializer.Meta):
        fields = AirplaneTypeSerializer.Meta.fields + ("airplane_count",)

    def get_airplane_count(self, obj):
        return obj.airplanes.count()


class AirplaneTypeRetrieveSerializer(AirplaneTypeSerializer):
    airplanes = serializers.SlugRelatedField(
        read_only=True, many=True, slug_field="model"
    )

    class Meta(AirplaneTypeSerializer.Meta):
        fields = AirplaneTypeSerializer.Meta.fields + ("airplanes",)


# AIRPLANE
class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "airplane_type", "model", "rows", "seats_per_row")


class AirplaneListSerializer(serializers.ModelSerializer):
    airplane_type = serializers.SlugRelatedField(
        read_only=True, slug_field="name"
    )

    class Meta:
        model = Airplane
        fields = ("id", "airplane_type", "model", "capacity")


class AirplaneRetrieveSerializer(AirplaneSerializer):
    airplane_type = serializers.SlugRelatedField(
        read_only=True, slug_field="name"
    )

    class Meta(AirplaneSerializer.Meta):
        fields = AirplaneSerializer.Meta.fields + ("capacity",)


# CREW
class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "role", "first_name", "last_name", "experience")


class CrewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "role", "full_name")


class CrewRetrieveSerializer(CrewSerializer):
    routes = serializers.SerializerMethodField()

    class Meta(CrewSerializer.Meta):
        fields = CrewSerializer.Meta.fields + ("routes",)

    def get_routes(self, obj):
        return [flight.route.full_route for flight in obj.flights.all()]


# FLIGHT
class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
        )


class FlightListSerializer(serializers.ModelSerializer):
    route = RouteListSerializer(read_only=True)

    class Meta:
        model = Flight
        fields = ("id", "route", "departure_time", "arrival_time")


class FlightRetrieveSerializer(FlightSerializer):
    route = RouteListSerializer(read_only=True)
    crew = CrewListSerializer(many=True, read_only=True)
    airplane = serializers.SlugRelatedField(
        read_only=True, slug_field="model"
    )


# BAGGAGE
class BaggageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Baggage
        fields = ("id", "length", "height", "width", "weight")


class BaggageListSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source="ticket.passenger", read_only=True)

    class Meta:
        model = Baggage
        fields = ("id", "owner", "weight", "volume")


class BaggageRetrieveSerializer(BaggageSerializer):
    owner = serializers.CharField(source="ticket.passenger", read_only=True)

    class Meta(BaggageSerializer.Meta):
        fields = BaggageSerializer.Meta.fields + ("volume", "owner")


# TICKET
class TicketSerializer(serializers.ModelSerializer):
    baggage = BaggageSerializer(many=True, required=False)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "flight",
            "row_number",
            "seat_number",
            "seat_class",
            "price",
            "baggage",
        ]
        read_only_fields = ["id", "price"]

    def validate(self, attrs):
        flight = attrs["flight"]
        row_number = attrs["row_number"]
        seat_number = attrs["seat_number"]
        airplane = flight.airplane

        if row_number > airplane.rows:
            raise serializers.ValidationError({
                "row_number": f"Airplane has only {airplane.rows} rows."
            })
        if seat_number > airplane.seats_per_row:
            raise serializers.ValidationError({
                "seat_number": (
                    f"Airplane has only {airplane.seats_per_row} "
                    f"seats per row."
                )
            })
        if Ticket.objects.filter(
            flight=flight, row_number=row_number, seat_number=seat_number
        ).exists():
            raise serializers.ValidationError({
                "seat": "This seat is already booked."
            })
        return attrs


class TicketListSerializer(serializers.ModelSerializer):
    route = serializers.CharField(source="flight.route.full_route")

    class Meta:
        model = Ticket
        fields = ("id", "route", "price")


class TicketRetrieveSerializer(TicketListSerializer):
    baggage = BaggageSerializer(many=True, read_only=True)

    class Meta(TicketListSerializer.Meta):
        fields = TicketListSerializer.Meta.fields + (
            "seat_class", "row_number", "seat_number", "baggage"
        )


# ORDER
class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, allow_empty=False)

    class Meta:
        model = Order
        fields = ["id", "status", "total_price", "created_at", "tickets"]
        read_only_fields = ["id", "status", "total_price", "created_at"]

    @transaction.atomic
    def create(self, validated_data):
        total_price = Decimal("0.00")
        tickets_data = validated_data.pop("tickets")
        order = Order.objects.create(
            user=self.context["request"].user,
            total_price=Decimal("0.00")
        )

        for ticket_data in tickets_data:
            baggage_data = ticket_data.pop("baggage", [])
            flight = ticket_data["flight"]
            seat_class = ticket_data["seat_class"]
            ticket_price = calculate_ticket_price(
                seat_class=seat_class,
                distance=flight.route.distance
            )
            ticket = Ticket.objects.create(
                order=order,
                passenger=self.context["request"].user,
                price=ticket_price,
                **ticket_data,
            )

            for baggage_data_item in baggage_data:
                Baggage.objects.create(ticket=ticket, **baggage_data_item)

            total_price += ticket_price

        order.total_price = total_price
        order.save(update_fields=["total_price"])

        return order


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "status", "created_at")


class OrderRetrieveSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
