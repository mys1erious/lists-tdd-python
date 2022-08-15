import unittest
from unittest.mock import patch, Mock

from django.test import TestCase
from ..forms import (
    ItemForm,
    NewListForm,
    ExistingListItemForm,
    EMPTY_ITEM_ERROR,
    DUPLICATE_ITEM_ERROR
)
from ..models import List, Item


class ExistingListItemFormTest(TestCase):
    def test_form_render_item_text_input(self):
        lst = List.objects.create()
        form = ExistingListItemForm(for_list=lst)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())

    def test_form_validation_for_blank_items(self):
        lst = List.objects.create()
        form = ExistingListItemForm(for_list=lst, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplicate_items(self):
        lst = List.objects.create()
        Item.objects.create(list=lst, text='no twins!')
        form = ExistingListItemForm(for_list=lst, data={'text': 'no twins!'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        lst = List.objects.create()
        form = ExistingListItemForm(for_list=lst, data={'text': 'hi'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.first())


class ItemFormTest(TestCase):
    def test_form_render_item_text_input(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])


@patch('lists.forms.List.create_new')
class NewListFormTest(unittest.TestCase):
    def test_save_creates_new_list_from_post_data_if_user_not_authenticated(self, mock_List_create_new):
        user = Mock(is_authenticated=False)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        form.save(owner=user)
        mock_List_create_new.assert_called_once_with(
            first_item_text='new item text'
        )

    def test_save_creates_new_list_from_post_data_if_user_is_authenticated(self, mock_List_create_new):
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        form.save(owner=user)
        mock_List_create_new.assert_called_once_with(
            first_item_text='new item text', owner=user
        )

    def test_save_returns_new_list_object(self, mock_List_create_new):
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        response = form.save(owner=user)
        self.assertEqual(response, response, mock_List_create_new.return_value)
