from wagtail.core import blocks
from wagtail.core.templatetags.wagtailcore_tags import richtext
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel, TabbedInterface, ObjectList
from django.db import models

class ProjectFileBlock(blocks.StructBlock):

    title = blocks.CharBlock(required=True, help_text="Add your title")
    block_number = blocks.IntegerBlock(required=True)
    cards = blocks.ListBlock( blocks.StructBlock(
            [
                ("file", models.FileField(required=True)),
                ("title", blocks.CharBlock(required=False, max_length=60)),
            ],
    ))

    class Meta:  # noqa
        template = "project/project_files.html"
        icon = "placeholder"
        label = "Project files"


