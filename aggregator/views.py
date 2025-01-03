# aggregator/views.py

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import IPAggregatorForm
from .utils import aggregate_ip_addresses, aggregate_ips

def index(request):
    form = IPAggregatorForm()
    result = None

    if request.method == 'POST':
        form = IPAggregatorForm(request.POST)
        if form.is_valid():
            ip_addresses = form.cleaned_data['ip_addresses']
            output_format = form.cleaned_data['output_format']
            why_blocked = form.cleaned_data['why_blocked']
            asn_code = form.cleaned_data['asn_code']
            
            result = aggregate_ip_addresses(ip_addresses, output_format, why_blocked, asn_code)
            
    
    else:
        form = IPAggregatorForm()

    return render(request, 'aggregator/index.html', {'form': form, 'result': result})



from django.http import JsonResponse
from django.utils.decorators import method_decorator

def ip_aggregator_api(request):
    if request.method == "POST":
        ip_addresses = request.POST.get("ip_addresses")
        output_format = request.POST.get("output_format", "text")

        if not ip_addresses:
            return JsonResponse({"error": "IP Address ranges are required!"}, status=400)

        try:
            # Process IP ranges
            aggregated_data = aggregate_ips(ip_addresses)
            return JsonResponse({
                "result": aggregated_data,
                "output_format": output_format,
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method. Use POST."}, status=405)