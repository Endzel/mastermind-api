from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated

from mastermind.models import Game, Play
from mastermind.mixins import PlayMixin
from mastermind.serializers import CreateGameSerializer, GameHistorySerializer


class CreateGameView(mixins.CreateModelMixin,
            generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)
    queryset = Game.objects.all()
    serializer_class = CreateGameSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SingleGameView(mixins.RetrieveModelMixin,
            generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)
    queryset = Game.objects.all()
    serializer_class = GameHistorySerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class PlayView(PlayMixin,
            generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)
    queryset = Play.objects.all()

    def post(self, request, *args, **kwargs):
        return self.play(request, *args, **kwargs)
