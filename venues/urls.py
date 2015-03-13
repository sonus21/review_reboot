from django.conf.urls import url, patterns
from django.conf.urls.i18n import i18n_patterns

__author__ = 'm'

urlpatterns = patterns('venues.views',
    # notes editing
    url(r'notes/(?P<note_pk>[0-9]+)/remove/$', 'notes.remove_note'),
    url(r'notes/(?P<note_pk>[0-9]+)/update/$', 'notes.update_note'),

    # comments editing
    url(r'comments/(?P<comment_pk>[0-9]+)/remove/$', 'comments.remove_comment'),
    url(r'comments/(?P<comment_pk>[0-9]+)/update/$', 'comments.update_comment'),
    url(r'comments/(?P<comment_pk>[0-9]+)/approve/$', 'moderate.approve_comment'),

    # moderate
    url(r'moderate/$', 'moderate.index'),
    url(r'moderate/reports$', 'moderate.reports'),
    url(r'moderate/reports/(?P<id>[0-9]+)/close$', 'moderate.resolve_report'),

    #profile
    url(r'profile/restaurants/$', 'profile.myrestaurants'),
    url(r'profile/comments/$', 'profile.mycomments'),
    url(r'profile/notes/$', 'profile.mynotes'),
    url(r'profile/reports/$', 'profile.myreports'),

    # venues
    url(r'(?P<rest_pk>[0-9]+)/show-all-comments/$', 'comments.show_all_comments'),
    url(r'(?P<rest_pk>[0-9]+)/show-all-tips/$', 'notes.show_all_notes'),
    url(r'(?P<rest_pk>[0-9]+)/report/$', 'reports.report_restaurant'),
    url(r'(?P<rest_pk>[0-9]+)/remove', 'venuess.remove_restaurant'),
    url(r'(?P<rest_pk>[0-9]+)/update/$', 'venuess.update_restaurant'),
    url(r'(?P<rest_pk>[0-9]+)/approve/$', 'moderate.approve_restaurant'),
    url(r'(?P<rest_pk>[0-9]+)/profile$', 'venuess.restaurant'),
    url(r'(?P<rest_pk>[0-9]+)/note/new/$', 'notes.add_note'),
    url(r'(?P<rest_pk>[0-9]+)/comment/new/', 'comments.add_comment'),
    url(r'(?P<rest_pk>[0-9]+)/comment/$', 'comments.comment'),

    # common
    url(r'restaurants_lists/$', 'venuess.restaurants_lists'),
    url(r'get_category/', 'get_category', name='get_drugs'),
    url(r'new$', 'venuess.add_restaurant'),

    # restautant by slug
    url(r'(?P<slug>[\w-]+)/$', 'venuess.restaurant_by_slug'),
)