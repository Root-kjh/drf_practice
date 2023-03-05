from test_plus.test import APITestCase

from ..models import Object, Category

class ObjectApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(name='test category')
        self.object = Object.objects.create(name='test object', category=self.category, description='test description')
        self.object2 = Object.objects.create(name='test object 2', category=self.category, description='test description 2')

    def test_get_objects(self):
        response = self.get('/reviews/objects/')
        self.assert_http_200_ok(response)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], self.object.name)
        self.assertEqual(response.data[1]['name'], self.object2.name)

    def test_get_object(self):
        response = self.get(f'/reviews/objects/{self.object.id}/')
        self.assert_http_200_ok(response)
        self.assertEqual(response.data['name'], self.object.name)

    def test_create_object(self):
        data = {'name': 'test object 3', 'category': self.category.id, 'description': 'test description 3'}
        response = self.post('/reviews/objects/', data=data)
        self.assert_http_201_created(response)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(Object.objects.count(), 3)
        self.assertEqual(Object.objects.last().name, data['name'])

    def test_update_object(self):
        data = {'name': 'test object 3', 'category': self.category.id, 'description': 'test description 3'}
        response = self.put(f'/reviews/objects/{self.object.id}/', data=data)
        self.assert_http_200_ok(response)
        self.assertEqual(response.data['name'], data['name'])
        self.assertTrue(Object.objects.filter(name=data['name']).exists())
        self.assertFalse(Object.objects.filter(name=self.object.name).exists())

    def test_delete_object(self):
        response = self.delete(f'/reviews/objects/{self.object.id}/')
        self.assert_http_204_no_content(response)
        self.assertFalse(Object.objects.filter(name=self.object.name).exists())
        self.assertEqual(Object.objects.count(), 1)