from rest_framework import serializers

from mastermind.models import Play, Game, Code, Feedback



class CodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Code
        exclude = ('id',)


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        exclude = ('id',)


class PlaySerializer(serializers.ModelSerializer):

    code = CodeSerializer(required=False)
    feedback = FeedbackSerializer(required=False)

    class Meta:
        model = Play
        fields = ('id', 'user', 'game', 'code', 'serializer',)
