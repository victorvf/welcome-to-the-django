from django.contrib import admin
from django.template.defaultfilters import safe

from eventex.core.models import Speaker, Contact, Talk, Course


class ContactInline(admin.TabularInline):
    model = Contact
    can_delete = False
    extra = 1


class SpeakerModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "photo_img", "website_link", "email", "phone"]
    inlines = [ContactInline]

    def website_link(self, obj):
        return safe(f'<a href="{obj.website}">{obj.website}</a>')

    website_link.short_description = "website"

    def photo_img(self, obj):
        return safe(f'<img style="width:32px;border-radius:100%;" src="{obj.photo}" />')

    photo_img.short_description = "foto"

    def email(self, obj):
        return obj.contact_set.emails().first()
    
    email.short_description = "e-mail"

    def phone(self, obj):
        return Contact.phones.filter(speaker=obj).first()
    
    phone.short_description = "telefone"


class TalkModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(course=None)


admin.site.register(Speaker, SpeakerModelAdmin)
admin.site.register(Talk, TalkModelAdmin)
admin.site.register(Course)
