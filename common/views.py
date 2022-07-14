from django.shortcuts import redirect

def root_redirect(request):
    response = redirect('https://miamiscaffoldrental.com')
    return response