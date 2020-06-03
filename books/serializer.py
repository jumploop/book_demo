#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/28 18:15
# @Author  : 一叶知秋
# @File    : serializer.py
# @Software: PyCharm
from rest_framework import serializers
from books.models import Books


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'
