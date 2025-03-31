from django.shortcuts import render
# import pyrebase
#
# config = {
#     "apiKey": "AIzaSyCTgnF2AydDIUAf7y4LEA3OM-bCniOTK_U",
#     "authDomain": "gtmoviestore.firebaseapp.com",
#     "databaseURL": "https://gtmoviestore-default-rtdb.firebaseio.com",
#     "projectId": "gtmoviestore",
#     "storageBucket": "gtmoviestore.firebasestorage.app",
#     "messagingSenderId": "639276599595",
#     "appId": "1:639276599595:web:88d10490534b2749e59d6e"
# }
#
# firebase = pyrebase.initialize_app(config)
# authe = firebase.auth()
# database = firebase.database()


# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def about(request):
    return render(request, 'home/about.html')
