# coding: utf-8
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Entry
from ..utils import HatenaApi
from ..serializer import EntryAllSerializer, EntryCreateAndUpdateSerializer


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntryAllSerializer

    @action(detail=False, methods=['post'])
    def capture(self, request):
        hatena_api = HatenaApi()
        all_entries = hatena_api.getAllEntries()
        all_entries_sort = sorted(all_entries, key=lambda x: x['edited_at'])
        response = {
            'created_count': 0,
            'updated_count': 0,
            'deleted_count': 0,
            'failed_count': 0,
            'failed_hatena_entry_ids': [],
        }
        hatena_entry_ids = []
        for param in all_entries_sort:
            print('category:')
            print(param['category'])
            hatena_entry_id = param['hatena_entry_id']
            hatena_entry_ids.append(hatena_entry_id)
            # 更新用パラメータ
            entry = Entry.objects.filter(
                hatena_entry_id=hatena_entry_id).first()

            if not entry:
                # 新規作成
                mode = 'create'
                serializer = EntryCreateAndUpdateSerializer(data=param)

            else:
                # 更新
                mode = 'update'
                serializer = EntryCreateAndUpdateSerializer(
                    entry, data=param)

            if serializer.is_valid():
                serializer.save()
                if mode == 'create':
                    response['created_count'] = response['created_count'] + 1
                else:
                    response['updated_count'] = response['updated_count'] + 1
            else:
                response['failed_count'] = response['failed_count'] + 1
                response['failed_hatena_entry_ids'].append(
                    hatena_entry_id)

        # はてなIDが存在しなければ論理削除
        response['deleted_count'] = Entry.objects.exclude(
            hatena_entry_id__in=hatena_entry_ids).delete()

        return Response(response, status.HTTP_200_OK)
