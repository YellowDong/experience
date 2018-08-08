#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path, include
from rest_framework import routers
from api.views import BlogListView, TagView


router = routers.DefaultRouter()
router.register(r'blog', BlogListView)
router.register(r'tag', TagView)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
