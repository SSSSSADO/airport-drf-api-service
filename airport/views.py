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


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CityListSerializer
        elif self.action == "retrieve":
            return CityRetrieveSerializer
        return CitySerializer


class AirportViewSet(ModelViewSet):
    queryset = Airport.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return AirportListSerializer
        elif self.action == "retrieve":
            return AirportRetrieveSerializer
        return AirportSerializer


class RouteViewSet(ModelViewSet):
    queryset = Route.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        elif self.action == "retrieve":
            return RouteRetrieveSerializer
        return RouteSerializer


class AirplaneTypeViewSet(ModelViewSet):
    queryset = AirplaneType.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneTypeListSerializer
        elif self.action == "retrieve":
            return AirplaneTypeRetrieveSerializer
        return AirplaneTypeSerializer


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


class FlightViewSet(ModelViewSet):
    queryset = Flight.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        elif self.action == "retrieve":
            return FlightRetrieveSerializer
        return FlightSerializer


class BaggageViewSet(ModelViewSet):
    queryset = Baggage.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return BaggageListSerializer
        elif self.action == "retrieve":
            return BaggageRetrieveSerializer
        return BaggageSerializer


class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        elif self.action == "retrieve":
            return TicketRetrieveSerializer
        return TicketSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        elif self.action == "retrieve":
            return OrderRetrieveSerializer
        return OrderSerializer
