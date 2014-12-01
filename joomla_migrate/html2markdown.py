#!/usr/bin/env python
 # -*- coding: utf-8 -*-

import pypandoc
from django.core.management import setup_environ
from blavanetproject import settings
setup_environ(settings)


from blog.models import Post

for post in Post.objects.all():
    p = post
    post_html_content = p.content
    post_markdown_content = pypandoc.convert(post_html_content,
                                             'markdown', format='html')
    p.content = post_markdown_content
    p.save()
