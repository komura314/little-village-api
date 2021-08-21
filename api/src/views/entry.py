# coding: utf-8
import time
import os
import requests
import xmltodict

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Entry
from ..serializer import EntryAllSerializer, EntryCreateAndUpdateSerializer


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntryAllSerializer

    @action(detail=False, methods=['post'])
    def capture(self, request):
        url = self.getHatenaApiUrl('entry')
        auth = self.getHatenaApiAuth()

        while url != '':
            # 連続で呼び出すの怖いので0.5秒間間を空ける
            time.sleep(0.5)
            hatena_list = requests.get(url, auth=auth)
            dict_data = xmltodict.parse(hatena_list.text, encoding='utf-8')
            entries = []
            if 'feed' in dict_data:
                if 'entry' in dict_data['feed']:
                    entries = dict_data['feed']['entry']
            for entry in entries:
                if not isinstance(entry, dict):
                    continue

                # hatena_entry_id取得
                hatena_entry_id = entry['id'][
                    entry['id'].rfind('-') + 1:] if 'id' in entry else ''

                # category取得
                if 'category' in entry:
                    if isinstance(entry['category'], list):
                        category = entry['category'][0]['@term']
                    else:
                        category = entry['category']['@term']
                else:
                    category = ''

                # title取得
                title = entry['title'] if 'title' in entry else ''

                # summary取得
                summary = entry['summary']['#text'] if 'summary' in entry else ''

                # content_md取得
                content_md = entry['content']['#text'] if 'content' in entry else ''

                # content_html取得
                content_html = entry['hatena:formatted-content']['#text'] if 'hatena:formatted-content' in entry else ''

                # draft取得
                draft = entry['app:control']['app:draft'] if 'app:control' in entry else ''

                # updated_at取得
                updated_at = entry['updated'] if 'updated' in entry else None

                # edited_at取得
                edited_at = entry['app:edited'] if 'app:edited' in entry else None

                # 更新用パラメータ
                param = {
                    'hatena_entry_id': hatena_entry_id,
                    'category': category,
                    'title': title,
                    'summary': summary,
                    'content_md': content_md,
                    'content_html': content_html,
                    'draft': draft,
                    'updated_at': updated_at,
                    'edited_at': edited_at,
                }

                entry = Entry.objects.filter(
                    hatena_entry_id=hatena_entry_id).first()

                if not entry:
                    # 新規作成
                    serializer = EntryCreateAndUpdateSerializer(data=param)
                else:
                    # 更新
                    serializer = EntryCreateAndUpdateSerializer(
                        entry, data=param)

                if serializer.is_valid():
                    serializer.save()
                    print('valid-OK')
                else:
                    print('valid-NG')

            # 次のURLを取得
            url = ''
            if 'link' in dict_data['feed']:
                if isinstance(dict_data['feed']['link'], list):
                    for link in dict_data['feed']['link']:
                        if isinstance(link, dict):
                            if '@rel' in link:
                                if link['@rel'] == 'next':
                                    url = link['@href']

        return Response(entries)

    def getHatenaApiUrl(self, action):
        HATENA_API_URL_HEADER = 'https://blog.hatena.ne.jp'
        HATENA_API_USER = os.environ.get('HATENA_API_USER')
        HATENA_API_BLOG = os.environ.get('HATENA_API_BLOG')
        HATENA_API_URL_FUTTER = 'atom'

        url = [
            HATENA_API_URL_HEADER,
            HATENA_API_USER,
            HATENA_API_BLOG,
            HATENA_API_URL_FUTTER,
            action
        ]
        return os.path.join(*url)

    def getHatenaApiAuth(self):
        HATENA_API_USER = os.environ.get('HATENA_API_USER')
        HATENA_API_KEY = os.environ.get('HATENA_API_KEY')

        return (HATENA_API_USER, HATENA_API_KEY)
