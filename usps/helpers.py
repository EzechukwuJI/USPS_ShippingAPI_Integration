from xml.etree import ElementTree as ET
from django.shortcuts import render




def get_url(request, action):
	rp = request.POST
	url = "http://production.shippingapis.com/ShippingApi.dll?API="
	xml = ""
	if action == "shipping-estimate":
		ounce_weight = float(rp['weight']) * 16
		print "ounce weight :", ounce_weight
		print "pound weight: ", rp['weight']

		xml += '''IntlRateV2&XML=
		<?xml version='1.0' encoding='utf-8' standalone='yes' ?>
		<IntlRateV2Request USERID="593CIRCU5990">
		<Revision>2</Revision>
		<Package ID="0">
		<Pounds> ''' + rp['weight'] + '''</Pounds>
		<Ounces>''' + str(ounce_weight) + '''</Ounces>
		<Machinable>True</Machinable>
		<MailType>''' + rp['mail_type'] + '''</MailType>
		<ValueOfContents>''' + rp['value_of_content'] + '''</ValueOfContents>
		<Country>''' + rp['destination_country'] + '''</Country>
		<Container>''' + rp['item_container'] + '''</Container>
		<Size>''' + rp['size'] + '''</Size>
		<Width>''' + rp['width'] + '''</Width>
		<Length>''' + rp['length'] + '''</Length>
		<Height>''' + rp['height'] + '''</Height>
		<Girth>0</Girth>
		<OriginZip>''' + rp['originZipCode'] + '''</OriginZip>
		<CommercialFlag>Y</CommercialFlag>
		<ExtraServices>
		<ExtraService>1</ExtraService>
		</ExtraServices>
		</Package>
		</IntlRateV2Request> '''
		print url + xml
	elif action == "tracking":
		# print "tracking number: ", rp['trackingID'].replace(" ", "")
		xml += '''TrackV2&XML=<TrackFieldRequest USERID="593CIRCU5990"><TrackID ID='''+ rp['trackingID'].replace(" ", "") +'''></TrackID></TrackFieldRequest>'''


		
		
	elif action == "address_verification":
		xml = '''Verify&XML=<?xml version='1.0' encoding='utf-8' standalone='yes' ?>
		<AddressValidateRequest USERID="593CIRCU5990">
		<Address>
		<Address1></Address1>
		<Address2>6406 Ivy Lane</Address2>
		<City>Greenbelt</City>
		<State>MD</State>
		<Zip5></Zip5>
		<Zip4></Zip4>
		</Address>
		</AddressValidateRequest>'''
	return url + xml






def process_api_response(request, xml_response, action):
	context = {}
	context['got_response']   =   True
	context['action']         =   action
	try:
		root = ET.fromstring(xml_response)
	except:
		return HttpResponse("Could not parse XML object")
	if action == "shipping-estimate":
		context["has_express_speed"]  =   True
		context["has_normal_speed"]   =   True
		
		context['destination']          =   root.findall(".//Service[@ID='1']/Country")[0].text
		#  Normal delivery
		try:
			context['normal_postage']       =   root.findall(".//Service[@ID='2']/Postage")[0].text
			context['normal_commercial']    =   root.findall(".//Service[@ID='2']/CommercialPostage")[0].text
			context['normal_duration']      =   root.findall(".//Service[@ID='2']/SvcCommitments")[0].text
			context['normal_desc']          =   root.findall(".//Service[@ID='2']/SvcDescription")[0].text
		except:
			context["has_normal_speed"]  =  False

		# Express delivery
		try:
			context['express_postage']      =   root.findall(".//Service[@ID='1']/Postage")[0].text
			context['express_commercial']   =   root.findall(".//Service[@ID='1']/CommercialPostage")[0].text
			context['express_duration']     =   root.findall(".//Service[@ID='1']/SvcCommitments")[0].text
			context['express_desc']         =   root.findall(".//Service[@ID='1']/SvcDescription")[0].text
		except:
			context["has_express_speed"]  =  False
			
	elif action == "Tracking":
		context['testing']  = True
	return render(request, 'usps/index.html', context)



def process_error_response(request, xml_response):
	root = ET.fromstring(xml_response)
	error_msg = root.findall(".//Error/Description")[0].text
	return error_msg















