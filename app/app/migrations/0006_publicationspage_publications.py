# Generated by Django 2.1.3 on 2018-11-24 23:07

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_publicationspage_publications'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicationspage',
            name='publications',
            field=wagtail.core.fields.StreamField([('publication', wagtail.core.blocks.StructBlock([('authors', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('first_name', wagtail.core.blocks.CharBlock()), ('last_name', wagtail.core.blocks.CharBlock())]))), ('title', wagtail.core.blocks.CharBlock()), ('date', wagtail.core.blocks.DateBlock()), ('journal', wagtail.core.blocks.CharBlock()), ('links', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('url', wagtail.core.blocks.URLBlock()), ('label', wagtail.core.blocks.CharBlock())])))]))], default=None),
            preserve_default=False,
        ),
    ]