from django.test import TestCase
import json
from apps.api.models import PlayerCategory, Player


class RegistrationTestCase(TestCase):
    def test_registration(self):
        data = {
            "name": "test",
            "email": "test@berserker.group",
            "token": "abcdef"
        }
        response = self.client.post('/api/account/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertTrue(response.data['token'])
        self.assertTrue(response.data['id'])

        # Register again with same info should return 200
        response = self.client.post('/api/account/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertTrue(response.data['token'])
        self.assertTrue(response.data['id'])


class VoteTestCase(TestCase):
    def test_vote(self):
        # Register
        data = {
            "name": "test",
            "email": "test@berserker.group",
            "token": "abcdef"
        }
        response = self.client.post('/api/account/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertTrue(response.data['token'])
        self.assertTrue(response.data['id'])

        # Create players
        category = PlayerCategory.objects.create(name="test")
        player1 = Player.objects.create(name="test1", category=category)
        player2 = Player.objects.create(name="test2", category=category)
        player3 = Player.objects.create(name="test3", category=category)

        # Vote
        votes = [1, 2, 3]
        data = {
            "form": 1,
            "votes": json.dumps(votes)
        }
        print(data)
        # auth header
        headers = {'Authorization': 'Token ' + response.data['token']}

        response = self.client.post('/api/vote/', data=data, headers=headers)
        print(response.content)
        self.assertEqual(response.status_code, 200)


