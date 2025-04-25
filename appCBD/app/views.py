from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    return render(request, 'home.html')

def load_stations(request):
    return redirect('home')

def lines_list(request):
    return redirect('home')

def line_form(request):
    return redirect('home')

def line_stations(request, pk):
    return redirect('home')

def station_form(request):
    return redirect('home')

def station_line(request, pk):
    return redirect('home')

def route_form(request):
    return redirect('home')

def route_stations(request):
    return redirect('home')