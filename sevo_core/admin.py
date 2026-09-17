from django.contrib import admin

from sevo_core import models

# Mxins
class BaseUserAdmin(admin.ModelAdmin):
    """Admin base class for models with a user owner.

    - Hide the user field from non-superusers.
    - Automatically assign the logged-in user on creation.
    - Allow superusers to view and change the user field.
    """
    user_field_name = "user"

    def get_form(self, request, obj=None, **kwargs):
        # if not request.user.is_superuser:
        #     exclude = list(kwargs.get("exclude", []))
        #     if self.user_field_name not in exclude:
        #         exclude.append(self.user_field_name)
        #     kwargs["exclude"] = exclude


        # print("get_form: ", kwargs["fields"])
        # if not request.user.is_superuser:
        #     print("user is not superuser, removing user field from form")
        #     fields = kwargs.get("fields")
        #     if fields and self.user_field_name in fields:
        #         kwargs["fields"] = [field for field in fields if field != self.user_field_name] 
        # print("modified fields: ", kwargs["fields"])
        print("kwargs in get_form: ", kwargs)
        return super().get_form(request, obj, **kwargs)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not request.user.is_superuser:
            return [field for field in fields if field != self.user_field_name]
        return fields

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if request.user.is_superuser:
            return fieldsets

        sanitized_fieldsets = []
        for name, data in fieldsets:
            fields = data.get("fields")
            if fields is None:
                sanitized_fieldsets.append((name, data))
                continue

            if isinstance(fields, dict):
                sanitized_fields = {
                    key: [field for field in value if field != self.user_field_name]
                    for key, value in fields.items()
                }
            else:
                sanitized_fields = [field for field in fields if field != self.user_field_name]

            sanitized_data = {**data, "fields": sanitized_fields}
            sanitized_fieldsets.append((name, sanitized_data))

        return sanitized_fieldsets

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(**{self.user_field_name: request.user})

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser or obj is None:
            return super().has_view_permission(request, obj=obj)
        if getattr(obj, self.user_field_name, None) == request.user:
            return super().has_view_permission(request, obj=obj)
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or obj is None:
            return super().has_change_permission(request, obj=obj)
        if getattr(obj, self.user_field_name, None) == request.user:
            return super().has_change_permission(request, obj=obj)
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or obj is None:
            return super().has_delete_permission(request, obj=obj)
        if getattr(obj, self.user_field_name, None) == request.user:
            return super().has_delete_permission(request, obj=obj)
        return False

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and getattr(obj, self.user_field_name, None) is None:
            setattr(obj, self.user_field_name, request.user)
        super().save_model(request, obj, form, change)



# Models
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

    readonly_fields = [
        "get_image_tag"
    ]


admin.site.register(models.Image, ImageAdmin)
admin.site.register(models.ImageCategory, ImageCategoryAdmin)
admin.site.register(models.ImageTag, ImageTagAdmin)