from pathlib import Path
import json

from unittest import TestCase
from unittest.mock import patch, call
from tests.helpers.response import MockResponse

import vercel

class TestTeams(TestCase):

    def setUp(self):
        vercel.api_key = 'fake-api-key'
        vercel.team_id = 'fake-team-id'

    def tearDown(self):
        vercel.api_key = None
        vercel.team_id = None

    @patch('requests.request')
    def test_create_v1(self, mock_request):
        mock_request.return_value = MockResponse(response={
          'id': 'team-id'
        })

        team = vercel.Team.create('my-team')

        assert isinstance(team, vercel.Team)
        assert team.id == 'team-id'
        
        assert [
            call(
                method='POST',
                url='https://api.vercel.com/v1/teams',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer fake-api-key'
                },
                json={
                  'slug': 'my-team'
                },
                params={
                    'teamId': 'fake-team-id'
                }
            )
        ] == mock_request.mock_calls
        
    @patch('requests.request')
    def test_delete_v1(self, mock_request):
        mock_v4_get = Path('tests/fixtures/responses/teams/v1/get.json')
        mock_request.return_value = MockResponse(response=json.loads(mock_v4_get.open().read()))

        team = vercel.Team.get('my-team')
        team.delete()
        
        assert [
            call(
                method='GET',
                url='https://api.vercel.com/v1/teams',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer fake-api-key'
                },
                params={
                    'teamId': 'fake-team-id',
                    'slug': 'my-team'
                }
            ),
            call(
                method='DELETE',
                url='https://api.vercel.com/v1/teams/team-id',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer fake-api-key'
                },
                params={
                    'teamId': 'fake-team-id'
                }
            )
        ] == mock_request.mock_calls
        
    @patch('requests.request')
    def test_update_v1(self, mock_request):
        mock_v4_get = Path('tests/fixtures/responses/teams/v1/get.json')
        mock_request.return_value = MockResponse(response=json.loads(mock_v4_get.open().read()))

        team = vercel.Team.get('my-team')
        team.update(
          slug='new-slug',
          name='New Name'
        )
        
        assert [
            call(
                method='GET',
                url='https://api.vercel.com/v1/teams',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer fake-api-key'
                },
                params={
                    'teamId': 'fake-team-id',
                    'slug': 'my-team'
                }
            ),
            call(
                method='PATCH',
                url='https://api.vercel.com/v1/teams/team-id',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer fake-api-key'
                },
                json={
                  'slug': 'new-slug',
                  'name': 'New Name'
                },
                params={
                    'teamId': 'fake-team-id'
                }
            )
        ] == mock_request.mock_calls
        
    @patch('requests.request')
    def test_get_v1(self, mock_request):
        mock_v1_get = Path('tests/fixtures/responses/teams/v1/get.json')
        mock_request.return_value = MockResponse(response=json.loads(mock_v1_get.open().read()))

        team = vercel.Team.get('my-team')

        assert isinstance(team, vercel.Team)
        
        assert team.name == 'My Team'
        assert team.id == 'team-id'
        assert team.slug == 'my-team'
        assert team.creator_id == 'creator-id'
        assert team.created == '2017-04-29T17:21:54.514Z'
        assert team.avatar == None
        
        assert [
            call(
                method='GET',
                url='https://api.vercel.com/v1/teams',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer fake-api-key'
                },
                params={
                    'teamId': 'fake-team-id',
                    'slug': 'my-team'
                }
            )
        ] == mock_request.mock_calls

    @patch('requests.request')
    def test_invite_user_v1(self, mock_request):
        mock_v1_get = Path('tests/fixtures/responses/teams/v1/get.json')
        mock_v1_invite_user = Path('tests/fixtures/responses/teams/v1/invite_user.json')
        mock_request.side_effect = [
            MockResponse(response=json.loads(mock_v1_get.open().read())),
            MockResponse(response=json.loads(mock_v1_invite_user.open().read()))
        ]

        team = vercel.Team.get('my-team')
        team.invite_user(
            email='test@email.com',
            role='MEMBER'
        )
        
        assert [
            call(
                method='GET',
                url='https://api.vercel.com/v1/teams',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer fake-api-key'
                },
                params={
                    'teamId': 'fake-team-id',
                    'slug': 'my-team'
                }
            ),
            call(
                method='POST',
                url='https://api.vercel.com/v1/teams/team-id/members',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer fake-api-key'
                },
                params={
                    'teamId': 'fake-team-id'
                },
                json={
                    'email': 'test@email.com',
                    'role': 'MEMBER'
                }
            )
        ] == mock_request.mock_calls

    @patch('requests.request')
    def test_update_user_v1(self, mock_request):
        mock_v1_get = Path('tests/fixtures/responses/teams/v1/get.json')
        mock_v1_update_user = Path('tests/fixtures/responses/teams/v1/update_user.json')
        mock_request.side_effect = [
            MockResponse(response=json.loads(mock_v1_get.open().read())),
            MockResponse(response=json.loads(mock_v1_update_user.open().read()))
        ]

        team = vercel.Team.get('my-team')
        team.update_user(
            user_id='user-id',
            role='MEMBER'
        )
        
        assert [
            call(
                method='GET',
                url='https://api.vercel.com/v1/teams',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer fake-api-key'
                },
                params={
                    'teamId': 'fake-team-id',
                    'slug': 'my-team'
                }
            ),
            call(
                method='PATCH',
                url='https://api.vercel.com/v1/teams/team-id/members/user-id',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer fake-api-key'
                },
                params={
                    'teamId': 'fake-team-id'
                },
                json={
                    'role': 'MEMBER'
                }
            )
        ] == mock_request.mock_calls

    @patch('requests.request')
    def test_request_to_join_v1(self, mock_request):
        mock_v1_get = Path('tests/fixtures/responses/teams/v1/get.json')
        mock_v1_request_to_join = Path('tests/fixtures/responses/teams/v1/request_to_join.json')
        mock_request.side_effect = [
            MockResponse(response=json.loads(mock_v1_get.open().read())),
            MockResponse(response=json.loads(mock_v1_request_to_join.open().read()))
        ]

        team = vercel.Team.get('my-team')
        team.request_to_join(
            origin='import'
        )
        
        assert [
            call(
                method='GET',
                url='https://api.vercel.com/v1/teams',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer fake-api-key'
                },
                params={
                    'teamId': 'fake-team-id',
                    'slug': 'my-team'
                }
            ),
            call(
                method='POST',
                url='https://api.vercel.com/v1/teams/team-id/request',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer fake-api-key'
                },
                params={
                    'teamId': 'fake-team-id'
                },
                json={
                    'origin': 'import'
                }
            )
        ] == mock_request.mock_calls

    @patch('requests.request')
    def test_remove_user_v1(self, mock_request):
        mock_v1_get = Path('tests/fixtures/responses/teams/v1/get.json')
        mock_v1_remove_user = Path('tests/fixtures/responses/teams/v1/remove_user.json')
        mock_request.side_effect = [
            MockResponse(response=json.loads(mock_v1_get.open().read())),
            MockResponse(response=json.loads(mock_v1_remove_user.open().read()))
        ]

        team = vercel.Team.get('my-team')
        team.remove_user('user-id')
        
        assert [
            call(
                method='GET',
                url='https://api.vercel.com/v1/teams',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer fake-api-key'
                },
                params={
                    'teamId': 'fake-team-id',
                    'slug': 'my-team'
                }
            ),
            call(
                method='DELETE',
                url='https://api.vercel.com/v1/teams/team-id/members/user-id',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer fake-api-key'
                },
                params={
                    'teamId': 'fake-team-id'
                }
            )
        ] == mock_request.mock_calls