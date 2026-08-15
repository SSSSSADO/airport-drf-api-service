from django.db.models import Prefetch
from rest_framework.viewsets import ModelViewSet

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
from airport.serializers import (
    CountrySerializer,
    CountryListSerializer,
    CountryRetrieveSerializer,
    CitySerializer,
    CityListSerializer,
    CityRetrieveSerializer,
    AirportSerializer,
    AirportListSerializer,
    AirportRetrieveSerializer,
    RouteSerializer,
    RouteListSerializer,
    RouteRetrieveSerializer,
    AirplaneTypeSerializer,
    AirplaneTypeListSerializer,
    AirplaneTypeRetrieveSerializer,
    AirplaneSerializer,
    AirplaneListSerializer,
    AirplaneRetrieveSerializer,
    CrewSerializer,
    CrewListSerializer,
    CrewRetrieveSerializer,
    FlightSerializer,
    FlightListSerializer,
    FlightRetrieveSerializer,
    OrderSerializer,
    OrderListSerializer,
    OrderRetrieveSerializer,
    TicketSerializer,
    TicketListSerializer,
    TicketRetrieveSerializer,
    BaggageSerializer,
    BaggageListSerializer,
    BaggageRetrieveSerializer
)


class CountryViewSet(ModelViewSet):
    queryset = Country.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CountryListSerializer
        elif self.action == "retrieve":
            return CountryRetrieveSerializer
        return CountrySerializer

    def get_queryset(self):
        qs = self.queryset
        if self.action == "list":
            return qs.prefetch_related("cities")
        return qs


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CityListSerializer
        elif self.action == "retrieve":
            return CityRetrieveSerializer
        return CitySerializer

    def get_queryset(self):
        qs = self.queryset
        if self.action == "list":
            return qs.select_related("country")
        elif self.action == "retrieve":
            return qs.select_related("country").prefetch_related("airports")
        return qs


class AirportViewSet(ModelViewSet):
    queryset = Airport.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return AirportListSerializer
        elif self.action == "retrieve":
            return AirportRetrieveSerializer
        return AirportSerializer

    def get_queryset(self):
        qs = self.queryset
        if self.action in ("list", "retrieve"):
            return qs.select_related("city")
        return qs


class RouteViewSet(ModelViewSet):
    queryset = Route.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        elif self.action == "retrieve":
            return RouteRetrieveSerializer
        return RouteSerializer

    def get_queryset(self):
        qs = self.queryset
        if self.action in ("list", "retrieve"):
            return qs.select_related("source", "destination")
        return qs


class AirplaneTypeViewSet(ModelViewSet):
    queryset = AirplaneType.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneTypeListSerializer
        elif self.action == "retrieve":
            return AirplaneTypeRetrieveSerializer
        return AirplaneTypeSerializer

    def get_queryset(self):
        qs = self.queryset
        if self.action in ("list", "retrieve"):
            return qs.prefetch_related("airplanes")
        return qs


class AirplaneViewSet(ModelViewSet):
    queryset = Airplane.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        elif self.action == "retrieve":
            return AirplaneRetrieveSerializer
        return AirplaneSerializer


class CrewViewSet(ModelViewSet):
    queryset = Crew.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CrewListSerializer
        elif self.action == "retrieve":
            return CrewRetrieveSerializer
        return CrewSerializer

    def get_queryset(self):
        qs = self.queryset
        if self.action == "retrieve":
            return qs.prefetch_related(
                Prefetch(
                    "flights",
                    queryset=Flight.objects.select_related(
                        "route__source",
                        "route__destination"
                    )
                )
            )
        return qs


class FlightViewSet(ModelViewSet):
    queryset = Flight.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        elif self.action == "retrieve":
            return FlightRetrieveSerializer
        return FlightSerializer

    def get_queryset(self):
        qs = self.queryset
        if self.action == "list":
            return qs.select_related(
                "route",
                "route__source",
                "route__destination"
            )
        elif self.action == "retrieve":
            return qs.select_related(
                "route",
                "route__source",
                "route__destination",
                "airplane",
            ).prefetch_related("crew")
        return qs


class BaggageViewSet(ModelViewSet):
    queryset = Baggage.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return BaggageListSerializer
        elif self.action == "retrieve":
            return BaggageRetrieveSerializer
        return BaggageSerializer

    def get_queryset(self):
        qs = self.queryset
        if self.action in ("list", "retrieve"):
            return qs.select_related("ticket__passenger")
        return qs


class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        elif self.action == "retrieve":
            return TicketRetrieveSerializer
        return TicketSerializer

    def get_queryset(self):
        qs = self.queryset
        if self.action == "list":
            return qs.select_related(
                "flight__route__source",
                "flight__route__destination"
            )
        elif self.action == "retrieve":
            return qs.select_related(
                "flight__route__source",
                "flight__route__destination"
            ).prefetch_related("baggage")
        return qs


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        elif self.action == "retrieve":
            return OrderRetrieveSerializer
        return OrderSerializer

    def get_queryset(self):
        qs = self.queryset
        if self.action == "retrieve":
            return qs.prefetch_related(
                Prefetch(
                    "tickets",
                    queryset=Ticket.objects.select_related(
                        "flight__route__source",
                        "flight__route__destination"
                    ).prefetch_related("baggage")
                )
            )
        return qs
