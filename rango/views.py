from django.http import HttpResponse

def about(request):
  return HttpResponse("Rango says here is the about page. <br/>" +
                      "<a href='/rango'>Main</a>")

def index(request):
  return HttpResponse("Rango says hello world! <br/>" +
                      "<a href='/rango/about'>About</a>")