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


# COUNTRY
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("id", "name", "code")


# CITY
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name", "country")


# AIRPORT
class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "city", "timezone")


# ROUTE
class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance", "duration")


# AIRPLANETYPE
class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")


# AIRPLANE
class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "airplane_type", "model", "rows", "seats_per_row")


# CREW
class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "role", "experience")


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


# ORDER
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "user", "status", "total_price", "created_at")


# TICKET
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "id",
            "flight",
            "passenger",
            "order",
            "seat_number",
            "row_number",
            "seat_class",
            "price",
            "created_at",
        )


# BAGGAGE
class BaggageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Baggage
        fields = ("id", "ticket", "length", "width", "weight", "height")
