from django.db import models
from wagtail.admin.edit_handlers import InlinePanel, FieldPanel
from wagtail.api import APIField

from wagtail.core.models import Page


class AboutPage(Page):

    bio = models.TextField(
        default='',
        blank=True,
    )

    api_fields = [
        APIField('bio'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('bio'),
    ]
