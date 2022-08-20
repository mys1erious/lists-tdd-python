import json
from django.test import TestCase
from django.urls import reverse

from ..models import List, Item
from ..forms import DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR


class ListAPITest(TestCase):
    base_url = '/api/lists/{}/'

    def test_get_returns_json_200(self):
        lst = List.objects.create()
        response = self.client.get(self.base_url.format(lst.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

    def test_get_returns_items_for_correct_list(self):
        other_list = List.objects.create()
        Item.objects.create(list=other_list, text='item 1')

        our_list = List.objects.create()
        item1 = Item.objects.create(list=our_list, text='item 1')
        item2 = Item.objects.create(list=our_list, text='item 2')

        response = self.client.get(self.base_url.format(our_list.id))
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {'id': our_list.id, 'items': [
                {'id': item1.id, 'list': item1.list.id, 'text': item1.text},
                {'id': item2.id, 'list': item1.list.id, 'text': item2.text},
            ]}
        )


class ItemsAPITest(TestCase):
    base_url = reverse('item-list')

    def test_POSTing_a_new_item(self):
        lst = List.objects.create()
        response = self.client.post(
            self.base_url,
            {'list': lst.id, 'text': 'new item'}
        )
        self.assertEqual(response.status_code, 201)
        new_item = lst.item_set.get()
        self.assertEqual(new_item.text, 'new item')

    def test_invalid_input_nothing_saved_to_db(self):
        self.post_empty_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_invalid_input_returns_error_code(self):
        response = self.post_empty_input()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {'text': [EMPTY_ITEM_ERROR]}
        )

    def test_duplicate_items_error(self):
        lst = List.objects.create()
        self.client.post(
            self.base_url.format(lst.id),
            data={'list': lst.id, 'text': 'thing'}
        )
        response = self.client.post(
            self.base_url.format(lst.id),
            data={'list': lst.id, 'text': 'thing'}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {'non_field_errors': [DUPLICATE_ITEM_ERROR]}
        )

    def post_empty_input(self):
        lst = List.objects.create()
        return self.client.post(
            self.base_url,
            data={'list': lst.id, 'text': ''}
        )
