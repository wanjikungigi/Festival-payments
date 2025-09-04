from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

def home(request):
    return render(request, "index.html")

def stk_push(request):
    return JsonResponse({"status": "ok", "message": "STK push placeholder"})

def mpesa_callback(request):
    return HttpResponse("Callback received")
