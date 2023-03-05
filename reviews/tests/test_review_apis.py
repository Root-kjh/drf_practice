from test_plus.test import APITestCase

from ..models import Item, Category, Review

class ReviewApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(name='test category')
        self.user = self.make_user()
        self.item = Item.objects.create(name='test item', category=self.category, description='test description')
        self.review = Review.objects.create(item=self.item, user=self.user, context='test context')
        self.review2 = Review.objects.create(item=self.item, user=self.user, context='test context 2')

    def test_get_reviews(self):
        response = self.get('/reviews/reviews/')
        self.assert_http_200_ok(response)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['context'], self.review.context)
        self.assertEqual(response.data[1]['context'], self.review2.context)

    def test_get_review(self):
        response = self.get(f'/reviews/reviews/{self.review.id}/')
        self.assert_http_200_ok(response)
        self.assertEqual(response.data['context'], self.review.context)

    def test_create_review(self):
        with self.login(username=self.user.username):
            data = {'context': 'test review 3', 'item': self.item.id, 'user': self.user.id}
            response = self.post('/reviews/reviews/', data=data)
            self.assert_http_201_created(response)
            self.assertEqual(response.data['context'], data['context'])
            self.assertEqual(Review.objects.count(), 3)
            self.assertEqual(Review.objects.last().context, data['context'])

    def test_update_review(self):
        with self.login(username=self.user.username):
            data = {'context': 'test review 3', 'item': self.item.id, 'user': self.user.id}
            response = self.put(f'/reviews/reviews/{self.review.id}/', data=data)
            self.assert_http_200_ok(response)
            self.assertEqual(response.data['context'], data['context'])
            self.assertFalse(Review.objects.filter(context=self.review.context).exists())

    def test_delete_review(self):
        with self.login(username=self.user.username):
            response = self.delete(f'/reviews/reviews/{self.review.id}/')
            self.assert_http_204_no_content(response)
            self.assertFalse(Review.objects.filter(context=self.review.context).exists())
            self.assertEqual(Review.objects.count(), 1)