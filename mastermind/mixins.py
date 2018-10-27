from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from mastermind.models import Game, Play, Code, Feedback
from mastermind.serializers import PlaySerializer

class PlayMixin(object):

    def check_position(self, code1, code2, position, all_positions):
        if getattr(code1, position) == getattr(code2, position):
            return 'black'
        elif getattr(code1, position) in all_positions:
            return "white"
        else:
            return "wrong"

    def give_feedback(self, code1, code2):
        feedback = {}
        all_positions = [code2.first, code2.second, code2.third, code2.fourth]
        for position in code1._meta.get_fields():
            field = position.name
            if (field is 'first') or (field is 'second') or (field is 'third') or (field is 'fourth'):
                feedback[field] = self.check_position(code1, code2, field, all_positions)
        return Feedback.objects.create(**feedback)


    def play(self, request, *args, **kwargs):
        try:
            game = Game.objects.get(id=request.data['game'])
            if game.codebreaker != request.user:
                return Response({"Sorry": "You are not assigned as a codebreaker for this game."})
            if game.tries == game.limit_guesses:
                return Response({"Sorry": "You already lost this game... Maximum tries exceeded."})
            if game.completed:
                return Response({"Sorry": "You already WON this game... Why would you play it again?"})
            game.tries += 1
            code = Code.objects.create(**request.data['code'])
            feedback = self.give_feedback(code, game.secret_code)
            if feedback.is_all_black():
                game.completed = True
                game.save()
                return Response({"Congratulations": "You WON this MasterMind's game!"}, status=HTTP_200_OK)
            play = Play.objects.create(user=request.user, feedback=feedback, game=game, code=code)
            game.save()
            serializer = PlaySerializer(play)
            return Response(serializer.data, status=HTTP_200_OK)
        except Exception as e:
            return Response({"ERROR": "Uncontrolled error:" + str(e)}, status=HTTP_400_BAD_REQUEST)
