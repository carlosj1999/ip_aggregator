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
from django.views.decorators.csrf import csrf_exempt
from .utils import aggregate_ips  # Import your utility function

@csrf_exempt  # Disable CSRF for testing
def ip_aggregator_api(request):
    if request.method == "POST":
        ip_addresses = request.POST.get("ip_addresses")
        output_format = request.POST.get("output_format", "text")

        if not ip_addresses:
            return JsonResponse({"error": "IP Address ranges are required!"}, status=400)
        
        if output_format not in ['cidr', 'mask', 'range', 'b-n', 'hta', 'zbb']:
            return JsonResponse({"error": "Invalid output format!"}, status=400)

        try:
            # Use utility function to process IP ranges
            aggregated_data = aggregate_ips(ip_addresses, output_format)
            return JsonResponse({
                "result": aggregated_data,
                "output_format": output_format,
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # For invalid request methods
    return JsonResponse({"error": "Invalid request method. Use POST."}, status=405)

from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def login_view(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def about(request):
    return render(request, 'about.html')