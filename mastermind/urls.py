from django.conf.urls import url

from mastermind.endpoints.user import RetrieveTokenView
from mastermind.endpoints.game import SingleGameView, CreateGameView, PlayView

api_urls = [
    url(r'^user$', RetrieveTokenView.as_view(), name='retrieveTokenView'),

    url(r'^game/(?P<pk>\d+)$', SingleGameView.as_view(), name='singleGameView'),
    url(r'^game$', CreateGameView.as_view(), name='createGameView'),
    url(r'^play$', PlayView.as_view(), name='playView'),
]
