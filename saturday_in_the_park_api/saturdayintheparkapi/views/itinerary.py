"""View module for handling requests about itineraries"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from saturdayintheparkapi.models import Itinerary, Attraction, Customer


class ItinerarySerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for itineraries

    Arguments:
        serializers
    """
    class Meta:
        model = Itinerary
        url = serializers.HyperlinkedIdentityField(
            view_name='itinerary',
            lookup_field='id'
        )
        fields = ("id", "url", "start_time", "attraction", "customer_id")
        depth = 1
        EXCLUDE = ("customer_id")

    def get_depth_param(self, obj):
        return self.context["depth"]


class Itineraries(ViewSet):
    """itineraries for Kennywood Amusement Park"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Attraction instance
        """

        new_data = request.data
        attraction = Attraction.objects.get(pk=new_data["attraction_id"])
        customer = Customer.objects.get(pk=new_data["customer_id"])
        new_itinerary = Itinerary.objects.create(
            start_time=new_data["start_time"],
            customer=customer,
            attraction=attraction
        )

        serializer = ItinerarySerializer(
            new_itinerary, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single itinerary

        Returns:
            Response -- JSON serialized itinerary instance
        """
        try:
            itinerary = Itinerary.objects.get(pk=pk)
            serializer = ItinerarySerializer(
                itinerary, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a itinerary attraction

        Returns:
            Response -- Empty body with 204 status code
        """
        data = request.data
        itenerary = Itinerary.objects.get(pk=pk)
        attraction = Attraction.objects.get(pk=data["attraction_id"])
        customer = Customer.objects.get(pk=data["customer_id"])
        itenerary.start_time = data["start_time"]
        itenerary.customer = customer
        itenerary.attraction = attraction

        itenerary.save()
        serial
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single itinerary

        Returns:
            Response -- 200, 404, or 500 status code
        """
        pass

    def list(self, request):
        """Handle GET requests to itineraries resource

        Returns:
            Response -- JSON serialized list of itineraries
        """
        itineraries = Itinerary.objects.all()

        attraction = self.request.query_params.get("attraction", None)
        customer = Customer.objects.get(user=request.auth.user)
        

        if attraction is not None:
            itineraries = itineraries.filter(attraction__id=attraction)

        if customer is not None:
            print(customer.id)
            itineraries = itineraries.filter(customer__id=customer.id)

        serializer = ItinerarySerializer(
            itineraries, many=True, context={'request': request, "depth": 1})

        return Response(serializer.data)
