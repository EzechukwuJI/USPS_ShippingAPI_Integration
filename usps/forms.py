from django import forms
from django.contrib.auth.models import User
from .models import *




class ShippingEstimateForm(forms.ModelForm):
	# girth  =  forms.CharField(widget= forms.TextInput())

	class Meta:
		model = ShippingEstimate
		fields = ('item_description','value_of_content','mail_type','destination_country',
			'originZipCode','width','length','height','weight','item_container', 'size')



class TrackingForm(forms.ModelForm):

	class Meta:
		model    =   TrackingInfo
		fields   =   ('trackingID',)



# class AddressVerificationForm(forms.ModelForm):
# 	class Meta:
# 		model = AddressInfo
# 		fields = ('')