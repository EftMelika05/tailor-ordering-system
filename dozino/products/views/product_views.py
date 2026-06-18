from django.http import JsonResponse


def product_list(request):

    return JsonResponse({
        "message": "products app works"
    })