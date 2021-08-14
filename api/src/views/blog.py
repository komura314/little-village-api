# coding: utf-8

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
        res = 'test'
        return Response(res)
