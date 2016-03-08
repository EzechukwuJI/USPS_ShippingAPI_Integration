from __future__ import unicode_literals

from django.db import models


CONTAINER = (('RECTANGULAR', 'RECTANGULAR'),
			 # ('NONRECTANGULAR', 'NONRECTANGULAR'),
	)


SIZE = (('REGULAR', 'REGULAR'),
		('LARGE', 'LARGE'),
	)

MAILTYPE = (('LETTER', 'LETTER'),
		('PACKAGE', 'PACKAGE'),
	)

SERVICETYPE = (('LETTER', 'LETTER'),
		('PACKAGE', 'PACKAGE'),
	)


class  ShippingEstimate(models.Model):
	item_description     =   models.CharField(max_length = 150)
	originZipCode        =   models.IntegerField("sender's zip code", default = 0)
	value_of_content     =   models.FloatField(default = 0.0)
	mail_type            =   models.CharField(max_length = 15, choices=MAILTYPE, default = "PACKAGE")
	# service_type         =   models.CharField(max_length = 15, choices=MAILTYPE, default = "PACKAGE")
	destination_country  =   models.CharField(max_length = 75)
	width                =   models.FloatField(default = 0.0)
	length               =   models.FloatField(default = 0.0)
	height               =   models.FloatField(default = 0.0)
	weight               =   models.FloatField(default = 0.0)
	item_container       =   models.CharField(max_length= 15, choices=CONTAINER, default ="RECTANGULAR")
	# girth                =   models.FloatField(default = 0.0)
	size                 =   models.CharField(max_length = 15, choices=SIZE, default="LARGE")
	shipping_estimate    =   models.FloatField(default = 0.0)

	def __unicode__(self):
		return '%s  %s' %(self.item_description, self.shipping_estimate)









class TrackingInfo(models.Model):
	trackingID       =  models.CharField(max_length = 30)
	trackingInfo     =  models.CharField(max_length = 225)

	def __unicode__(self):
		return '%s  %s' %(self.trackingID, self.trackingInfo)










