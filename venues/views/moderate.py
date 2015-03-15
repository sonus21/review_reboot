from account.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from venues.models import Restaurant
from venues.models import Review
from venues.models.report import Report


@login_required
@user_passes_test(lambda u: u.is_venue_moderator())
def index(request):
    # approved items paginator
    list = Restaurant.objects.order_by("approved", "name")
    paginatorApproved = Paginator(list, 10)
    page = request.GET.get("page")
    try:
        restaurants = paginatorApproved.page(page)
    except PageNotAnInteger:
        restaurants = paginatorApproved.page(1)
    except EmptyPage:
        restaurants = paginatorApproved.page(paginatorApproved.num_pages)

    # updated restaurants
    list = Restaurant.objects.order_by("-modified_on")
    paginatorApproved = Paginator(list, 10)
    page = request.GET.get("pageUpdated")
    try:
        recently_update_restaurants = paginatorApproved.page(page)
    except PageNotAnInteger:
        recently_update_restaurants = paginatorApproved.page(1)
    except EmptyPage:
        recently_update_restaurants = paginatorApproved.page(paginatorApproved.num_pages)

    # checking for restaurant changed fields
    # which can be accessed via changed_fields property
    for rest in recently_update_restaurants.object_list:
        items = rest.history_link.filter(id=rest.id).order_by("-history_date")
        changed_fields = []
        if items.count() > 1:
            previous = items[1]
            if previous:
                for field in rest._meta.get_all_field_names():
                    if field not in ['cuisines', 'modified_by', 'created_by', 'modified_by_id', 'created_by_id',
                                     'modified_on', 'slug'] and getattr(rest, field) != getattr(previous, field):
                        changed_fields.append(field)
        else:
            changed_fields.append("created")
        rest.changed_fields = changed_fields

    # added reviews
    list = Review.objects.order_by("-approved", "-modified_on")
    paginatorApproved = Paginator(list, 10)
    page = request.GET.get("pageReview")
    try:
        recently_added_reviews = paginatorApproved.page(page)
    except PageNotAnInteger:
        recently_added_reviews = paginatorApproved.page(1)
    except EmptyPage:
        recently_added_reviews = paginatorApproved.page(paginatorApproved.num_pages)

    context = {
        'restaurants': restaurants,
        'recently_update_restaurants': recently_update_restaurants,
        'recently_added_reviews': recently_added_reviews,
    }
    return render(request, "moderate/index.html", context)


@login_required
@user_passes_test(lambda u: u.is_venue_moderator())
def reports(request):
    reports = Report.objects.all()
    paginatorReports = Paginator(reports, 10)
    page = request.GET.get("page")
    try:
        reports = paginatorReports.page(page)
    except PageNotAnInteger:
        reports = paginatorReports.page(1)
    except EmptyPage:
        reports = paginatorReports.page(paginatorReports.num_pages)

    return render(request, "moderate/reports.html", {
        'reports': reports
    })


@login_required
@user_passes_test(lambda u: u.is_venue_moderator())
def approve_restaurant(request, rest_pk):
    restaurant = get_object_or_404(Restaurant, pk=rest_pk)
    restaurant.approved = request.POST['approved'].lower() == u'true'
    restaurant.save()

    if request.is_ajax():
        return HttpResponse()
    else:
        if "HTTP_REFERER" in request:
            return redirect(request.META['HTTP_REFERER'])
        return redirect(reverse("venues.views.venuess.index"))


@login_required
@user_passes_test(lambda u: u.is_venue_moderator())
def approve_review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    review.approved = True
    review.save()

    if request.is_ajax():
        return HttpResponse()
    else:
        if "HTTP_REFERER" in request:
            return redirect(request.META['HTTP_REFERER'])
        return redirect(reverse("venues.views.venuess.index"))


@login_required
@user_passes_test(lambda u: u.is_venue_moderator())
def resolve_report(request, id):
    report = get_object_or_404(Report, pk=id)

    if request.method == "POST":
        if 'moderator_note' in request.POST:
            report.moderator_note = request.POST['moderator_note']

    report.closed_by = request.user
    report.resolved = True
    report.save()

    if request.is_ajax():
        return HttpResponse()
    else:
        if "HTTP_REFERER" in request:
            return redirect(request.META['HTTP_REFERER'])
        return redirect(reverse("venues.views.venuess.index"))


