from django.urls import path
from apps.api.views import VoteView, csv_votes

urlpatterns = [
    path('vote/', VoteView.as_view(), name='vote'),
    path('csv/votes', csv_votes, name='vote_csv'),
]
