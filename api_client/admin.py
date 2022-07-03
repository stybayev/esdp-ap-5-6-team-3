# from django.contrib import admin
# from api_client.models import Client
#
#
# class UserAdmin(admin.ModelAdmin):
#     list_display = (
#         'full_name', 'email', 'email_verified', 'phone_verified',
#         'first_name_cyrillic',
#         'last_name_cyrillic', 'first_name_latin', 'last_name_latin')
#
#     def get_deleted_objects(self, objs, request):
#         deleted_objects, model_count, perms_needed, protected = \
#             super().get_deleted_objects(objs, request)
#         return deleted_objects, model_count, set(), protected
#
#
# admin.site.register(Client, UserAdmin)
