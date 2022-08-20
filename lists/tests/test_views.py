import unittest
from unittest.mock import patch, Mock

from django.http import HttpRequest
from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Item, List
from ..forms import ItemForm, EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR, ExistingListItemForm
from ..views import new_list


User = get_user_model()


class MyListsTest(TestCase):
    def test_my_lists_url_renders_my_lists_template(self):
        User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertTemplateUsed(response, 'lists/my_lists.html')

    def test_passes_correct_owner_to_template(self):
        User.objects.create(email='wrong@owner.com')
        correct_user = User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertEqual(response.context['owner'], correct_user)


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        lst = List.objects.create()
        response = self.client.get(f'/lists/{lst.id}/')
        self.assertTemplateUsed(response, 'lists/list.html')

    # def test_displays_only_items_from_1_list(self):
    #     correct_list = List.objects.create()
    #     Item.objects.create(text='itemey 1', list=correct_list)
    #     Item.objects.create(text='itemey 2', list=correct_list)
    #
    #     other_list = List.objects.create()
    #     Item.objects.create(text='other list item 1', list=other_list)
    #     Item.objects.create(text='other list item 2', list=other_list)
    #
    #     response = self.client.get(f'/lists/{correct_list.id}/')
    #
    #     self.assertContains(response, 'itemey 1')
    #     self.assertContains(response, 'itemey 2')
    #     self.assertNotContains(response, 'other list item 1')
    #     self.assertNotContains(response, 'other list item 2')

    def test_can_save_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, EMPTY_ITEM_ERROR)

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        lst = List.objects.create()
        item = Item.objects.create(list=lst, text='textey')
        response = self.client.post(
            f'/lists/{lst.id}/',
            data={'text': 'textey'}
        )

        self.assertContains(response, DUPLICATE_ITEM_ERROR)
        self.assertTemplateUsed(response, 'lists/list.html')
        self.assertEqual(Item.objects.all().count(), 1)

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def test_displays_item_form(self):
        lst = List.objects.create()
        response = self.client.get(f'/lists/{lst.id}/')
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def post_invalid_input(self):
        lst = List.objects.create()
        return self.client.post(f'/lists/{lst.id}/', data={'text': ''})


# Just for sanity check
class NewListViewIntegratedTest(TestCase):
    def test_can_save_POST_request(self):
        self.client.post('/lists/new', data={'text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_invalid_input_doesnt_save_but_shows_errors(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertContains(response, EMPTY_ITEM_ERROR)

    def test_list_owner_is_saved_if_user_is_authenticated(self):
        user = User.objects.create(email='a@b.com')
        self.client.force_login(user)
        self.client.post('/lists/new', data={'text': 'new item'})
        lst = List.objects.first()
        self.assertEqual(lst.owner, user)


@patch('lists.views.NewListForm')
class NewListViewUnitTest(unittest.TestCase):
    def setUp(self) -> None:
        self.request = HttpRequest()
        self.request.POST['text'] = 'new list item'
        self.request.user = Mock()

    def test_passes_POST_data_to_NewListForm(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        returned_object = mock_form.save.return_value
        returned_object.get_absolute_url.return_value = 'fakeurl'

        new_list(self.request)

        mockNewListForm.assert_called_once_with(data=self.request.POST)

    def test_saves_form_with_owner_if_form_valid(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True
        returned_object = mock_form.save.return_value
        returned_object.get_absolute_url.return_value = 'fakeurl'

        new_list(self.request)

        mock_form.save.assert_called_once_with(owner=self.request.user)

    @patch('lists.views.redirect')
    def test_redirects_to_form_returned_object_if_form_valid(self, mock_redirect, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True

        response = new_list(self.request)

        self.assertEqual(response, mock_redirect.return_value)
        mock_redirect.assert_called_once_with(mock_form.save.return_value)

    @patch('lists.views.render')
    def test_renders_home_template_with_form_if_form_invalid(self, mock_render, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False

        response = new_list(self.request)

        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(
            self.request, 'lists/home.html', {'form': mock_form}
        )

    def test_doesnt_save_if_form_invalid(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False

        new_list(self.request)

        self.assertFalse(mock_form.save.called)


class ShareListTest(TestCase):
    def test_POST_redirects_to_list_page(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/share'
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_POST_adds_user_to_shared_with(self):
        other_user = User.objects.create(email='other@example.com')
        other_list = List.objects.create()
        owner_user = User.objects.create(email='owner@example.com')
        correct_list = List.objects.create(owner=owner_user)

        response = self.client.post(
            f'/lists/{correct_list.id}/share',
            data={'sharee': 'other@example.com'}
        )

        self.assertIn(other_user, list(correct_list.shared_with.all()))

        self.assertRedirects(response, f'/lists/{correct_list.id}/')
