from django.http import JsonResponse, Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .utilities import convert_files_to_refts


@csrf_exempt  # Temporary fix, change later.
def ajax_refts_convert_files(request):
    return_obj = {
        'success': False,
        'message': None,
        'results': {}
    }
    if request.is_ajax() and request.method == 'POST':
        convert_files_to_refts(request.FILES.getlist('file'))
    return JsonResponse(return_obj)


@csrf_exempt  # Temporary fix, change later.
def ajax_refts_download_files(request):
    return_obj = {
        'success': False,
        'message': None,
        'results': {}
    }
    return JsonResponse(return_obj)


@csrf_exempt  # Temporary fix, change later.
def ajax_refts_clear_files(request):
    return_obj = {
        'success': False,
        'message': None,
        'results': {}
    }
    return JsonResponse(return_obj)
