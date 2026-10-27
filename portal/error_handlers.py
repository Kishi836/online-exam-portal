from django.shortcuts import render


def bad_request(request, exception):
    return render(request, "errors/error.html", status=400)


def permission_denied(request, exception):
    return render(request, "errors/error.html", status=403)


def page_not_found(request, exception):
    return render(request, "errors/error.html", status=404)


def server_error(request):
    return render(request, "errors/error.html", status=500)
