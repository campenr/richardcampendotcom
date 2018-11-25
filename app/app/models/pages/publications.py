from django.db import models
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.api import APIField

from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page


class ArticleLinkBlock(blocks.StructBlock):

    url = blocks.URLBlock()
    label = blocks.CharBlock()


class AuthorBlock(blocks.StructBlock):

    first_name = blocks.CharBlock()
    last_name = blocks.CharBlock()


class PublicationBlock(blocks.StructBlock):

    authors = blocks.ListBlock(AuthorBlock())
    title = blocks.CharBlock()

    date = blocks.DateBlock()

    journal = blocks.CharBlock()

    links = blocks.ListBlock(ArticleLinkBlock())


class PublicationsPage(Page):

    publications = StreamField([
        ('publication', PublicationBlock())
    ])

    api_fields = [
        APIField('publications')
    ]

    content_panels = Page.content_panels + [
        StreamFieldPanel('publications')
    ]
