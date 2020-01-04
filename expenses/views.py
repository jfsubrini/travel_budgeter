from django.shortcuts import render


def expenses(request):
    """
    View to the expenses page.
    """
    context = {}
    return render(request, "expenses.html", context)
