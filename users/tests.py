import jwt

from datetime      import datetime, timedelta

from django.test   import TestCase, Client
from django.conf   import settings
from unittest.mock import patch
from unittest      import mock

from users.models  import User

class KakaoSignInTest(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 1,
            kakao_id = 123456789,
            name     = 'DGK',
            email    = 'GET_DGKTEST@gmail.com'
        )
    
    def tearDown(self):
        User.objects.all().delete()
        
    @patch('users.views.requests')
    def test_kakao_signin_success_new_create_user(self, mocked_requests):
        client = Client()
        
        class MockedResponse:
            def json(self):
                return {
                    'id' : 12345678910,
                    'kakao_account' : {
                        'email' : 'CREATE_DGKTEST@gmail.com',
                        'profile' : {
                            'nickname' : 'DGK'
                        }
                    }
                }
            
        mocked_requests.get = mock.MagicMock(return_value = MockedResponse())
        headers             = {'Authorization' : 'fake_access_token'}
        response            = client.get('/users/kakao-auth', **headers)
        
        user                = User.objects.get(kakao_id=12345678910)
        access_token        = jwt.encode({'user_id' : user.id, 'exp': datetime.utcnow() + timedelta(hours=24)}, settings.SECRET_KEY, settings.ALGORITHM)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message' : 'SUCCESS', 'access_token' : access_token})    
    
    @patch('users.views.requests')
    def test_kakao_signin_success_already_existed_user(self, mocked_requests):
        client = Client()
        
        class MockedResponse:
            def json(self):
                return {
                    'id' : 123456789,
                    'kakao_account' : {
                        'email' : 'GET_DGKTEST@gmail.com',
                        'profile' : {
                            'nickname' : 'DGK'
                        }
                    }
                }
            
        mocked_requests.get = mock.MagicMock(return_value = MockedResponse())
        headers             = {'Authorization' : 'fake_access_token'}
        response            = client.get('/users/kakao-auth', **headers)
        access_token        = jwt.encode({'user_id' : 1, 'exp': datetime.utcnow() + timedelta(hours=24)}, settings.SECRET_KEY, settings.ALGORITHM)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'SUCCESS', 'access_token' : access_token})
        
    @patch('users.views.requests')
    def test_kakao_signin_fail_key_error(self, mocked_requests):
        client = Client()
        
        class MockedResponse:
            def json(self):
                return {
                    'id' : 123456789,
                    'kakao_account' : {
                        'profile' : {
                            'nickname' : 'DGK'
                        }
                    }
                }
        
        mocked_requests.get = mock.MagicMock(return_value = MockedResponse())
        headers             = {'Authorization' : 'fake_access_token'}
        response            = client.get('/users/kakao-auth', **headers)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'KEY_ERROR'})
        
    @patch('users.views.requests')
    def test_kakao_signin_fail_invalid_token(self, mocked_requests):
        client = Client()
        
        class MockedResponse:
            def json(self):
                return {
                    'code' : -401
                }
                
        mocked_requests.get = mock.MagicMock(return_value = MockedResponse())
        headers             = {'Authorization' : 'fake_access_token'}
        response            = client.get('/users/kakao-auth', **headers)
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message' : 'INVALID_TOKEN'})