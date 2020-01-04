from django.shortcuts import render


def converter(request):
    """
    View to the converter page.
    """
    context = {}
    return render(request, "converter.html", context)
