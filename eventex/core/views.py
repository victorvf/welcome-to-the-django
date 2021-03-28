from django.shortcuts import render


def home(request):
    speakers = [
        {"name": "Grace Hopper", "image_url": "http://hbn.link/hopper-pic"},
        {"name": "Alan Turing", "image_url": "http://hbn.link/turing-pic"},
    ]
    return render(request, "core/index.html", {"speakers": speakers})
