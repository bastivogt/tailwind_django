from django.db import models

from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.utils import html

User = get_user_model()


# Mixins

class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        abstract = True 


class BaseUserMixin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))    
    class Meta:
        abstract = True



# Models

class ImageCategory(TimeStampMixin):
    name = models.CharField(max_length=255, verbose_name=_("Name"))


    class Meta:
        verbose_name = _("Image Category")
        verbose_name_plural = _("Image Categories")
        ordering = ["name"]

    def __str__(self):
        return self.name


class ImageTag(TimeStampMixin):
    name = models.CharField(max_length=255, verbose_name=_("Name"))


    class Meta:
        verbose_name = _("Image Tag")
        verbose_name_plural = _("Image Tags")
        ordering = ["name"]

    def __str__(self):
        return self.name



class Image(TimeStampMixin):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    image = models.ImageField(upload_to="images/", verbose_name=_("Image"))
    category = models.ForeignKey(ImageCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Category"))
    tags = models.ManyToManyField(ImageTag, blank=True, verbose_name=_("Tags"))

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        # Delete the image file from storage when the Image object is deleted
        self.image.delete(save=False)
        super().delete(*args, **kwargs)


    def get_image_tag(self):
        if self.image:
            return html.format_html('<img src="{}" style="width: 80px; height: 80px; object-fit: cover;" />', self.image.url)
        return ""
    get_image_tag.short_description = _("Image Preview")
    get_image_tag.allow_tags = True  


    def get_image_tag_link(self):
        if self.image:
            return html.format_html('<a href="{}" target="_blank">{}</a>', self.image.url, self.get_image_tag())
        return ""   
    get_image_tag_link.short_description = _("Image Preview")
    get_image_tag_link.allow_tags = True 


    def get_image_url(self):
        if self.image:
            return self.image.url
        return ""

    def get_tags_as_string(self):
        return ", ".join([tag.name for tag in self.tags.all()]) 
    get_tags_as_string.short_description = _("Tags")
