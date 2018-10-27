from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from mastermind.models import Game, Play, Code, Feedback
from mastermind.serializers import PlaySerializer

class PlayMixin(object):

    def check_position(self, code1, code2, position, all_positions):
        if code1[position.__name__] == code2[position.__name__]:
            return 'black'
        elif code1[position.__name__] in all_positions:
            return "white"
        else:
            return "wrong"

    def give_feedback(self, code1, code2):
        feedback = {}
        all_positions = (code2.first, code2.second, code2.third, code2.fourth)
        for position in code1:
            feedback[position.__name__] = self.check_position(code1, code2, position, all_positions)
        return Feedback.objects.create(feedback)


    def play(self, request, *args, **kwargs):
        try:
            game = Game.objects.get(id=request.data['game'])
            if game.codebreaker != request.user:
                return Response({"Sorry": "You are not assigned as a codebreaker for this game."})
            if game.retries == game.limit_guesses:
                return Response({"Sorry": "You already lost this game... Maximum tries exceeded."})
            game.tries += 1
            game.save()
            code = Code.objects.create(request.data['code'])
            feedback = self.give_feedback(code, game.secret_code)
            if feedback.is_all_white():
                game.completed = True
                game.save()
                return Response({"Congratulations": "You WON this MasterMind's game!"}, status=HTTP_200_OK)
            play = Play.objects.create(user=request.user, feedback=feedback, game=game, code=code)
            serializer = PlaySerializer(play)
            return Response(serializer.data, status=HTTP_200_OK)
        except Exception as e:
            return Response({"ERROR": "Uncontrolled error:" + str(e)}, status=HTTP_400_BAD_REQUEST)
