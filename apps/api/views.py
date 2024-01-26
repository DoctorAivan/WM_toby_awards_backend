import csv
import json
import requests
from django.conf import settings
from django.http import HttpResponse
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import views, status

from apps.api.management.commands.get_votes import VotesCsv

from apps.api.models import Vote, Player
from apps.api.serializers import VoteSerializer


class VoteView(views.APIView):

    # Add Votes
    def post(self, request):
        serializer = VoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        form = data['form']
        votes_in = json.loads(data['votes'])

        # Captcha Check
        if not settings.TESTING:
            captcha_token = data['token']

        # Validate Captcha Response
        if self.captcha_check(request, captcha_token):
            votes = []
            for vote in votes_in:
                player = Player.objects.get(id=vote)
                v = Vote(
                    form=form,
                    player=player
                )
                votes.append(v)
            Vote.objects.bulk_create(votes)

        return Response(status=status.HTTP_200_OK)

    # Validate Captcha
    def captcha_check(self, request, captcha_token):
        try:
            turnstile_api = settings.TURNSTILE_API_PROXY
            turnstile_body = {
                'secret': settings.TURNSTILE_SECRET,
                'response': captcha_token,
                'remoteip': request.META.get('REMOTE_ADDR', '')
            }
            api = requests.post(turnstile_api, json=turnstile_body, timeout=3)
            api_response = api.json()

            if api_response.get("success") is not True:
                return False
            else:
                return True

        except Exception as e:
            return True


@api_view(['GET'])
def csv_votes(request):
    form = request.query_params.get('form')

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename="votos_form_{form}.csv"'}
    )
    writer = csv.writer(response)

    final_csv = VotesCsv()
    headers, rows = final_csv.process_csv(write=False, form=form)

    writer.writerow(headers)
    for row in rows:
        writer.writerow(row.values())

    return response


def index(request):
    return HttpResponse("")