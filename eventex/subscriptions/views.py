from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, resolve_url as r
from django.core import mail
from django.template.loader import render_to_string
from django.conf import settings

from .forms import SubscriptionForm
from .models import Subscription


def new(request):
    if request.method == "POST":
        return create(request)

    return empty_form(request)


def create(request):
    form = SubscriptionForm(request.POST)

    if not form.is_valid():
        return render(
            request,
            "subscriptions/subscription_form.html",
            {"form": form},
        )

    subscription = form.save()

    _send_mail(
        "Confirmação de inscrição",
        "subscriptions/subscription_email.txt",
        settings.DEFAULT_FROM_EMAIL,
        subscription.email,
        {"subscription": subscription},
    )

    return HttpResponseRedirect(r("subscriptions:detail", subscription.pk))


def empty_form(request):
    return render(
        request,
        "subscriptions/subscription_form.html",
        {"form": SubscriptionForm()},
    )


def detail(request, pk):
    # get_object_or_404()
    try:
        subscription = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        raise Http404()

    return render(
        request,
        "subscriptions/subscription_detail.html",
        {"subscription": subscription}
    )


def _send_mail(subject, template_name, from_, to, context):
    body = render_to_string(template_name, context)

    mail.send_mail(subject, body, from_, [from_, to])