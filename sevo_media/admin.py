from django.contrib import admin

from sevo_media import models

# Images

class ImageCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name", 
        "created_at", 
        "updated_at"
        )
    search_fields = ("name",)


class ImageTagAdmin(admin.ModelAdmin):
    list_display = (
        "name", 
        "created_at", 
        "updated_at"
        )
    search_fields = ("name",)

class ImageAdmin(admin.ModelAdmin):
    fields = [
        "title",
        "image",
        "get_image_tag",
        "category",
        "tags"
    ]
    list_display = [
        "id",
        "get_image_tag",
        "title", 
        "category", 
        "get_tags_as_string",
        "created_at", 
        "updated_at"
    ]

    list_display_links = [
        "id",
        "get_image_tag",
    ]

    list_filter = [
        "category",
        "tags",
        "created_at",
        "updated_at"
    ]

    search_fields = [
        "title"
    ]

    raw_id_fields = [
        #"category",
    ]

    readonly_fields = [
        "get_image_tag"
    ]



# Files

class FileCategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name", 
        "created_at", 
        "updated_at"
    ]
    search_fields = [
        "name"
    ]   


class FileTagAdmin(admin.ModelAdmin):
    list_display = [
        "name", 
        "created_at", 
        "updated_at"
    ]
    search_fields = [
        "name"
    ]

class FileAdmin(admin.ModelAdmin):
    fields = [
        "title",
        "file",
        "category",
        "tags"
    ]
    list_display = [
        "id",
        "title", 
        "category", 
        "get_tags_as_string",
        "created_at", 
        "updated_at"
    ]

    list_display_links = [
        "id",
        "title"
    ]

    list_filter = [
        "category",
        "tags",
        "created_at",
        "updated_at"
    ]

    search_fields = [
        "title"
    ]

    raw_id_fields = [
        #"category",
    ]


admin.site.register(models.File, FileAdmin)
admin.site.register(models.FileCategory, FileCategoryAdmin)
admin.site.register(models.FileTag, FileTagAdmin)

admin.site.register(models.Image, ImageAdmin)
admin.site.register(models.ImageCategory, ImageCategoryAdmin)
admin.site.register(models.ImageTag, ImageTagAdmin)