"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from saturdayintheparkapi.models import ParkArea


class ParkAreaSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    class Meta:
        model = ParkArea
        url = serializers.HyperlinkedIdentityField(
            view_name='parkarea',
            lookup_field='id'
        )
        fields = ("id", "url", "name", "theme")


class ParkAreas(ViewSet):
    """Park Areas for Saturday in the Park"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Attraction instance
        """
        new_data = request.data
        new_park_area = ParkArea.objects.create(
            name=new_data["name"],
            theme=new_data["theme"]
        )

        serializer = ParkAreaSerializer(
            new_park_area, context={"request": request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            parkarea = ParkArea.objects.get(pk=pk)
            serializer = ParkAreaSerializer(
                parkarea, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a park area attraction

        Returns:
            Response -- Empty body with 204 status code
        """
        data = request.data
        parkarea = ParkArea.objects.get(pk=pk)
        parkarea.name = data["name"]
        parkarea.theme = data["theme"]
        parkarea.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single park are

        Returns:
            Response -- 200, 404, or 500 status code
        """
        pass

    def list(self, request):
        """Handle GET requests to itineraries resource

        Returns:
            Response -- JSON serialized list of itineraries
        """
        parkareas = ParkArea.objects.all()

        serializer = ParkAreaSerializer(
            parkareas, many=True, context={"request": request}
        )

        return Response(serializer.data)
