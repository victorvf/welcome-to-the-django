from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core import mail
from django.template.loader import render_to_string
from django.contrib import messages

from .forms import SubscriptionForm


def subscribe(request):
    if request.method == "POST":
        form = SubscriptionForm(request.POST)

        if form.is_valid():
            body = render_to_string(
                "subscriptions/subscription_email.txt",
                form.cleaned_data,
            )

            mail.send_mail(
                "Confirmação de incrição",
                body,
                "victor@mail.com",
                [form.cleaned_data["email"], "fulano@mail.com"],
            )
            messages.success(request, "Inscrição realizada com sucesso!")

            return HttpResponseRedirect("/inscricao/")
        else:
            return render(
                request,
                "subscriptions/subscription_form.html",
                {"form": form},
            )
    else:
        return render(
            request,
            "subscriptions/subscription_form.html",
            {"form": SubscriptionForm()},
        )
