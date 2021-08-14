# coding: utf-8

from rest_framework import viewsets

from ..models import Entry
from ..serializer import EntrySerializer


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
