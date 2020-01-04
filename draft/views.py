from django.shortcuts import render


def draft(request):
    """
    View to the draft page.
    """
    context = {}
    return render(request, "draft.html", context)
