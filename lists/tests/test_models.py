from django.core.exceptions import ValidationError
from django.test import TestCase
from ..models import Item, List


class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_item(self):
        lst = List()
        lst.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = lst
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = lst
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, lst)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, lst)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, lst)

    def test_cant_save_empty_list_items(self):
        lst = List.objects.create()
        item = Item(list=lst, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
