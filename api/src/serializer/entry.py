# coding: utf-8

from rest_framework import serializers

from ..models import Entry


class EntryAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'


class EntryCreateAndUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = (
            'entry_id',
            'hatena_entry_id',
            'title',
            'summary',
            'content_md',
            'content_html',
            'draft',
            'updated_at',
            'edited_at',
        )
