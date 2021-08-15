# coding: utf-8
import os
import requests
import xmltodict

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import User
from ..serializer import UserSerializer


class BlogViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def capture(self, request, pk=None):
        url = self.getHatenaApiUrl('entry')
        auth = self.getHatenaApiAuth()
        res = requests.get(url, auth=auth)
        dictData = xmltodict.parse(res.text, encoding='utf-8')
        print(dictData)
        return Response(dictData)

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
