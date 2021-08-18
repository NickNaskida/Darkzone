from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

def send_email(name, email, message):
	''' Function that sends email to me with data from form '''
	try:
		send_mail(
        	name, #subject
			message, #message
			email, #from email
			[settings.EMAIL_HOST_USER], #to email
			)
	except BadHeaderError:
		return HttpResponse('Invalid header found')