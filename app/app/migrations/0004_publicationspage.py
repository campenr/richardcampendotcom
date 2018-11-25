# Generated by Django 2.1.3 on 2018-11-24 23:02

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('app', '0003_aboutpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicationsPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('publications', wagtail.core.fields.StreamField([('publication', wagtail.core.blocks.StructBlock([('authors', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('first_name', wagtail.core.blocks.CharBlock()), ('last_name', wagtail.core.blocks.CharBlock())]))), ('title', wagtail.core.blocks.CharBlock()), ('date', wagtail.core.blocks.DateBlock()), ('journal', wagtail.core.blocks.CharBlock()), ('links', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('url', wagtail.core.blocks.URLBlock()), ('label', wagtail.core.blocks.CharBlock())])))]))])),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]