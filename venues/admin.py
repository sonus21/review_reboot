from django.contrib.auth.models import User
from django.contrib.gis import admin
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.auth.admin import UserAdmin
from venues import models
from venues.models import VenueUser


class VenueUserInline(admin.StackedInline):
    model = VenueUser
    can_delete = False
    verbose_name_plural = 'venue user'


class UserAdmin(UserAdmin):
    inlines = (VenueUserInline, )
    list_display = UserAdmin.list_display + ('is_superuser', 'venue_moderator',)

    def venue_moderator(self, obj):
        user = VenueUser.objects.filter(user=obj).first()
        if user:
            return user.venue_moderator
        else:
            return obj.is_superuser
    venue_moderator.boolean = True
    # list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active')

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# VENUES

class MasjidAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'id', 'phone', 'twitter_url', 'facebook_url')


class RestaurantAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'id', 'phone', 'avg_rating')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('venue_name', 'rating', 'short_text', 'user')
    fields = (('venue_name', 'user'), 'rating', 'text')
    readonly_fields = ('venue_name',)


class NoteAdmin(admin.ModelAdmin):
    list_display = ('venue_name', 'text', 'user')
    fields = (('venue_name', 'user'), 'text')
    readonly_fields = ('venue_name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')

# Register your models here.
admin.site.register(models.Restaurant, RestaurantAdmin)
admin.site.register(models.Masjid, MasjidAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Note, NoteAdmin)
admin.site.register(models.Report, admin.ModelAdmin)