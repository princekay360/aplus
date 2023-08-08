from django.shortcuts import render


def index(request):
    request.session["attend_attempt_log"] = {}
    return render(request, 'aplus_app/index.html')
