from test_plus.test import APITestCase
from ..models import Category

class CategoryApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = self.make_user(perms=['reviews.add_category', 'reviews.change_category', 'reviews.delete_category'])
        self.category = Category.objects.create(name='test category')
        self.category2 = Category.objects.create(name='test category 2')

    def test_get_categories(self):
        response = self.get('/reviews/categories/')
        self.assert_http_200_ok(response)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], self.category.name)
        self.assertEqual(response.data[1]['name'], self.category2.name)

    def test_get_category(self):
        response = self.get(f'/reviews/categories/{self.category.id}/')
        self.assert_http_200_ok(response)
        self.assertEqual(response.data['name'], self.category.name)

    def test_create_category(self):
        with self.login(username=self.user.username):
            data = {'name': 'test category 3'}
            response = self.post('/reviews/categories/', data=data)
            self.assert_http_201_created(response)
            self.assertEqual(response.data['name'], data['name'])
            self.assertEqual(Category.objects.count(), 3)
            self.assertEqual(Category.objects.last().name, data['name'])

    def test_update_category(self):
        with self.login(username=self.user.username):
            data = {'name': 'test category 3'}
            response = self.put(f'/reviews/categories/{self.category.id}/', data=data)
            self.assert_http_200_ok(response)
            self.assertEqual(response.data['name'], data['name'])
            self.assertTrue(Category.objects.filter(name=data['name']).exists())
            self.assertFalse(Category.objects.filter(name=self.category.name).exists())

    def test_delete_category(self):
        with self.login(username=self.user.username):
            response = self.delete(f'/reviews/categories/{self.category.id}/')
            self.assert_http_204_no_content(response)
            self.assertFalse(Category.objects.filter(name=self.category.name).exists())
            self.assertEqual(Category.objects.count(), 1)
