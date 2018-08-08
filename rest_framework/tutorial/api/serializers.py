#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import serializers
from api.models import BlogModel, TagModel


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        fields = ('name',)


class BlogSerializer(serializers.ModelSerializer):
    tag = TagSerializer()

    class Meta:
        model = BlogModel
        fields = ('title', 'body', 'tag', 'create_time')

    def create(self, validated_data):
        tag_data = validated_data.pop('tag')
        # name = BlogModel.objects.create(**validated_data)
        tag = TagModel.objects.create(**tag_data)
        blog = BlogModel.objects.create(tag=tag, **validated_data)
        return blog

    def update(self, instance, validated_data):
        # tag_data = validated_data.pop('tag')

        # tag = instance.tag

        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.tag = validated_data.get('tag', instance.tag)
        instance.save()
        # tag.has_support_contract = tag_data.get('has_support_contract',
        #                                     tag.has_support_contract)
        # tag.is_premium_member = tag_data.get('is_premium_member',
        #                                     tag.is_premium_member)
        return instance
