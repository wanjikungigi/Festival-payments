from django.http import HttpResponse, JsonResponse  

def home(request):
    return HttpResponse("Welcome to the Payments App!")  # <--- homepage

def stk_push(request):
    return JsonResponse({"status": "ok", "message": "STK push placeholder"})

def mpesa_callback(request):
    return HttpResponse("Callback received")
