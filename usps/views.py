import requests
import xmltodict, json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import helpers
import forms
from .forms import ShippingEstimateForm, TrackingForm



# Create your views here.
def index(request):
	return render(request, 'usps/index.html')





def do_api_request(request, **kwargs):
	context = {}
	context['action']  =  kwargs['action']
	if hasattr(forms, kwargs['action'] + "Form"):
		form_class = getattr(forms,  kwargs['action'] + "Form")
		context['form'] = form_class()
	else:
		return HttpResponse("<strong style='padding:25px; margin-top:25px;'>Form Does not Exist</strong><a href='/'> Back </a>")
	if request.method == "POST":
		rp = request.POST
		form_class = getattr(forms, rp['form_name'])
		form = form_class(data = request.POST)
		if form.is_valid():
			r = requests.post(helpers.get_url(request, rp['action']), headers = {'Content-Type': 'application/xml'})
			if r.status_code == 200:
				try:
					return  helpers.process_api_response(request, r.content, rp['action']) 
				except:
					# attempt error processing 
					try:
						error_msg = helpers.process_error_response(request, r.content)
					except:
						return render(request, 'usps/index.html', {'server_error_msg':r.content, 'server_error':True, 'got_response':False })
					return render(request, 'usps/index.html', {'server_error_msg':error_msg, 'server_error':True, 'got_response':False })
			else:
				return HttpResponse("Error encountered code ", r.status_code)
		else:
			return HttpResponse(form.errors)
	return render(request, 'usps/index.html', context)


















