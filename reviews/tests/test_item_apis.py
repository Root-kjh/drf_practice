from test_plus.test import APITestCase

from ..models import Item, Category

class ItemApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = self.make_user(perms=['reviews.add_item', 'reviews.change_item', 'reviews.delete_item'])
        self.category = Category.objects.create(name='test category')
        self.item = Item.objects.create(name='test item', category=self.category, description='test description')
        self.item2 = Item.objects.create(name='test item 2', category=self.category, description='test description 2')

    def test_get_items(self):
        response = self.get('/reviews/items/')
        self.assert_http_200_ok(response)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], self.item.name)
        self.assertEqual(response.data[1]['name'], self.item2.name)

    def test_get_item(self):
        response = self.get(f'/reviews/items/{self.item.id}/')
        self.assert_http_200_ok(response)
        self.assertEqual(response.data['name'], self.item.name)

    def test_create_item(self):
        with self.login(username=self.user.username):
            data = {'name': 'test item 3', 'category': self.category.id, 'description': 'test description 3'}
            response = self.post('/reviews/items/', data=data)
            self.assert_http_201_created(response)
            self.assertEqual(response.data['name'], data['name'])
            self.assertEqual(Item.objects.count(), 3)
            self.assertEqual(Item.objects.last().name, data['name'])

    def test_update_item(self):
        with self.login(username=self.user.username):
            data = {'name': 'test item 3', 'category': self.category.id, 'description': 'test description 3'}
            response = self.put(f'/reviews/items/{self.item.id}/', data=data)
            self.assert_http_200_ok(response)
            self.assertEqual(response.data['name'], data['name'])
            self.assertTrue(Item.objects.filter(name=data['name']).exists())
            self.assertFalse(Item.objects.filter(name=self.item.name).exists())

    def test_delete_item(self):
        with self.login(username=self.user.username):
            response = self.delete(f'/reviews/items/{self.item.id}/')
            self.assert_http_204_no_content(response)
            self.assertFalse(Item.objects.filter(name=self.item.name).exists())
            self.assertEqual(Item.objects.count(), 1)