from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SalesRecord, Product, Region
from .forms import SalesRecordForm

@csrf_exempt
def index(request):
    if request.method == 'GET':
        records = list(SalesRecord.objects.all().values())
        return JsonResponse(records, safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
# def add_record(request):
#     if request.method == 'POST':
#         form = SalesRecordForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return JsonResponse({'success': True})
#         else:
#             return JsonResponse({'errors': form.errors}, status=400)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)
def add_record(request):
    if request.method == 'POST':
        form = SalesRecordForm(request.POST, request.FILES)
        if form.is_valid():
            sales_record = form.save(commit=False)
            # Update sales_amount of associated region
            sales_record.region.sales_amount += sales_record.sales_amount
            sales_record.product.sales_amount += sales_record.sales_amount
            sales_record.region.save(update_fields=['sales_amount'])
            sales_record.product.save(update_fields=['sales_amount'])
            sales_record.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
@csrf_exempt
def products(request):
    if request.method == 'GET':
        products = list(Product.objects.all().values())
        return JsonResponse(products, safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def regions(request):
    if request.method == 'GET':
        regions = list(Region.objects.all().values())
        return JsonResponse(regions, safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
