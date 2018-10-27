from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated

from mastermind.models import Game, Play
from mastermind.mixins import PlayMixin
from mastermind.serializers import CreateGameSerializer, GameHistorySerializer


class GameView(mixins.ListModelMixin,
            mixins.CreateModelMixin,
            generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)
    queryset = Game.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateGameSerializer
        return GameHistorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PlayView(PlayMixin,
            generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)
    queryset = Play.objects.all()

    def post(self, request, *args, **kwargs):
        return self.play(request, *args, **kwargs)
