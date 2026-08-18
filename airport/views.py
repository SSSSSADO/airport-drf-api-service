from django.db.models import F, Count, Prefetch

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from airport.permissions import (
    IsStaffOrReadOnly, IsOwnerOrStaff, IsBaggageOwnerOrStaff
    )
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
    BaggageRetrieveSerializer,
)


class CountryViewSet(ModelViewSet):
    queryset = Country.objects.all()
    permission_classes = [IsStaffOrReadOnly]

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["id", "name", "code"]
    ordering_fields = ["name", "code"]

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
    permission_classes = [IsStaffOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["country"]
    search_fields = ["id", "name", "country__name"]
    ordering_fields = ["name", "country"]

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
    permission_classes = [IsStaffOrReadOnly]

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["id", "name", "city__name"]
    ordering_fields = ["name", "city__name"]

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
    permission_classes = [IsStaffOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["source", "destination"]
    search_fields = ["id", "source__name", "destination__name"]
    ordering_fields = ["distance", "duration"]

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
    permission_classes = [IsStaffOrReadOnly]

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["id", "name"]
    ordering_fields = ["name", "airplane_count"]

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneTypeListSerializer
        elif self.action == "retrieve":
            return AirplaneTypeRetrieveSerializer
        return AirplaneTypeSerializer

    def get_queryset(self):
        qs = self.queryset
        if self.action in ("list", "retrieve"):
            return qs.prefetch_related("airplanes").annotate(
                airplane_count=Count("airplanes")
            )
        return qs


class AirplaneViewSet(ModelViewSet):
    queryset = Airplane.objects.all()
    permission_classes = [IsStaffOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["airplane_type"]
    search_fields = ["id", "model"]
    ordering_fields = ["airplane_type", "model", "capacity_ordering"]

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        elif self.action == "retrieve":
            return AirplaneRetrieveSerializer
        return AirplaneSerializer

    def get_queryset(self):
        qs = self.queryset
        if self.action in ("list", "retrieve"):
            return qs.select_related("airplane_type").annotate(
                capacity_ordering=F("rows") * F("seats_per_row")
            )
        return qs


class CrewViewSet(ModelViewSet):
    queryset = Crew.objects.all()
    permission_classes = [IsStaffOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["role"]
    search_fields = ["id", "first_name", "last_name"]
    ordering_fields = ["first_name", "experience"]

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
                        "route__source", "route__destination"
                    ),
                )
            )
        return qs


class FlightViewSet(ModelViewSet):
    queryset = Flight.objects.all()
    permission_classes = [IsStaffOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["route", "airplane"]
    search_fields = ["id", "route__source__name", "route__destination__name"]
    ordering_fields = ["departure_time", "arrival_time"]

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
                "route", "route__source", "route__destination"
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
    permission_classes = [IsBaggageOwnerOrStaff]

    filter_backends = [SearchFilter, OrderingFilter]
    # search_fields = ["id", "ticket__passanger__first_name"] # Need override User model
    ordering_fields = ["weight"]

    def get_serializer_class(self):
        if self.action == "list":
            return BaggageListSerializer
        elif self.action == "retrieve":
            return BaggageRetrieveSerializer
        return BaggageSerializer

    def get_queryset(self):
        qs = self.queryset

        if not self.request.user.is_staff:
            qs = qs.filter(ticket__passenger=self.request.user)

        if self.action in ("list", "retrieve"):
            return qs.select_related("ticket__passenger")
        return qs


class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["order__status"]
    search_fields = [
        "id",
        "flight__route__source__name",
        "flight__route__destination__name"
    ]
    ordering_fields = ["created_at"]

    def get_permissions(self):
        if self.action == "retrieve":
            permission_classes = [IsAuthenticated, IsOwnerOrStaff]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        elif self.action == "retrieve":
            return TicketRetrieveSerializer
        return TicketSerializer

    def get_queryset(self):
        qs = self.queryset
        if self.action == "list":
            qs = qs.select_related(
                "flight__route__source",
                "flight__route__destination",
            )
        elif self.action == "retrieve":
            qs = qs.select_related(
                "flight__route__source",
                "flight__route__destination",
            ).prefetch_related("baggage")
        return qs


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsOwnerOrStaff]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status"]
    search_fields = ["id", "created_at"]
    ordering_fields = ["created_at"]

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        elif self.action == "retrieve":
            return OrderRetrieveSerializer
        return OrderSerializer

    def get_queryset(self):
        qs = self.queryset

        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)

        if self.action == "retrieve":
            return qs.prefetch_related(
                Prefetch(
                    "tickets",
                    queryset=Ticket.objects.select_related(
                        "flight__route__source", "flight__route__destination"
                    ).prefetch_related("baggage"),
                )
            )
        return qs
