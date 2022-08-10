from django.core.exceptions import ValidationError
from django.test import TestCase
from ..models import Item, List


class ItemModelTest(TestCase):
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_str_repr(self):
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')


class ListModelTest(TestCase):
    def test_get_absolute_url(self):
        lst = List.objects.create()
        self.assertEqual(lst.get_absolute_url(), f'/lists/{lst.id}/')


class ListAndItemModelTest(TestCase):
    def test_item_is_related_to_list(self):
        lst = List.objects.create()
        item = Item()
        item.list = lst
        item.save()
        self.assertIn(item, lst.item_set.all())

    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='item 2')
        item3 = Item.objects.create(list=list1, text='3')
        self.assertEqual(list(Item.objects.all()), [item1, item2, item3])

    def test_cant_save_empty_list_items(self):
        lst = List.objects.create()
        item = Item(list=lst, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        lst = List.objects.create()
        Item.objects.create(list=lst, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=lst, text='bla')
            item.full_clean()

    def test_CAN_save_same_item_to_diff_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean()  # shouldnt raise
