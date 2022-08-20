import json

from django.http import HttpResponse
from rest_framework import routers, serializers, viewsets
from rest_framework.validators import UniqueTogetherValidator

from .forms import ExistingListItemForm, EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR
from .models import List, Item


class ItemSerializer(serializers.ModelSerializer):
    text = serializers.CharField(
        allow_blank=False, error_messages={'blank': EMPTY_ITEM_ERROR}
    )

    class Meta:
        model = Item
        fields = ('id', 'list', 'text')
        validators = [
            UniqueTogetherValidator(
                queryset=Item.objects.all(),
                fields=('list', 'text'),
                message=DUPLICATE_ITEM_ERROR
            )
        ]


class ListSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, source='item_set')

    class Meta:
        model = List
        fields = ('id', 'items',)


class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


router = routers.SimpleRouter()
router.register(r'lists', ListViewSet)
router.register(r'items', ItemViewSet)


def list(request, pk):
    lst = List.objects.get(id=pk)

    if request.method == 'GET':
        item_dicts = [
            {'id': item.id, 'text': item.text}
            for item in lst.item_set.all()
        ]
        return HttpResponse(json.dumps(item_dicts), content_type='application/json')

    if request.method == 'POST':
        form = ExistingListItemForm(for_list=lst, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=201)

        return HttpResponse(
            json.dumps({'error': form.errors['text'][0]}),
            status=400
        )
