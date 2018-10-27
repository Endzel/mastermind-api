from rest_framework import serializers

from mastermind.models import Play, Game, Code, Feedback, CustomUser


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('alias', 'email', 'password')


class CodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Code
        exclude = ('id',)


class SecretCodeSerializer(serializers.ModelSerializer):

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
        fields = ('id', 'user', 'game', 'code', 'feedback',)


class GameHistorySerializer(serializers.ModelSerializer):

    plays = PlaySerializer(required=False, many=True, source="get_all_plays")

    class Meta:
        model = Game
        fields = ('id', 'codebreaker', 'codemaker', 'plays', 'completed',)


class CreateGameSerializer(serializers.ModelSerializer):

    secret_code = CodeSerializer(required=True)
    codebreaker = serializers.CharField(required=True)
    id = serializers.IntegerField(required=False, read_only=True)

    class Meta:
        model = Game
        fields = ('id', 'codebreaker', 'secret_code',)

    def create(self, validated_data):
        code_data = validated_data.pop('secret_code')
        email = validated_data.pop('codebreaker')
        codebreaker = CustomUser.objects.get(email=email)
        secret_code = CodeSerializer.create(CodeSerializer(), validated_data=code_data)
        validated_data['codemaker'] = self.context['request'].user
        validated_data['secret_code'] = secret_code
        validated_data['codebreaker'] = codebreaker
        game = Game.objects.create(**validated_data)
        return game
