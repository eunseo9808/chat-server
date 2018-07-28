from .tests import AuthedTestCase


class TestChatter(AuthedTestCase):

    def test_01_post(self):
        post_request = {
            'username': "test12345",
            'password': "test12345",
            'nickname': "test12345",
            'fcm_reg_id': 'test'
        }
        post_response = self.client.post('/api/chatters', post_request)

        self.assertEqual(post_response.status_code, 201)
        self.assertEqual(post_response.data['username'], 'test12345')
        self.assertEqual(post_response.data['nickname'], 'test12345')
        self.assertEqual(post_response.data['fcm_reg_id'], 'test')

    def test_02_get(self):
        get_response = self.client.get('/api/chatters')

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual('test1234', get_response.data[0]['username'])
        self.assertEqual('test1234', get_response.data[0]['nickname'])
        self.assertEqual('test', get_response.data[0]['fcm_reg_id'])

    def test_03_put(self):
        put_request = {
            'nickname': "Mr.Hyper",
            'fcm_reg_id': "ABCD"
        }
        put_response = self.client.put('/api/chatters', data=put_request)

        self.assertEqual(put_response.status_code, 200)
        self.assertEqual('test1234', put_response.data['username'])
        self.assertEqual('Mr.Hyper', put_response.data['nickname'])
        self.assertEqual('ABCD', put_response.data['fcm_reg_id'])

    def test_04_delete(self):
        delete_response = self.client.delete('/api/chatters')

        self.assertEqual(delete_response.status_code, 200)
        self.assertIn('message', delete_response.data)

    def test_05_get_id(self):
        get_response = self.client.get('/api/chatters/'+str(self.user_id))

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual('test1234', get_response.data['username'])
        self.assertEqual('test1234', get_response.data['nickname'])
        self.assertEqual('test', get_response.data['fcm_reg_id'])
