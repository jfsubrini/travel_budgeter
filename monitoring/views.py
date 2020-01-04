from django.shortcuts import render


def monitoring(request):
    """
    View to the monitoring page.
    """
    context = {}
    return render(request, "monitoring.html", context)
