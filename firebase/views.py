from django.shortcuts import render, redirect
import pyrebase,json


# Create your views here.
 
 
config={
    "apiKey": "AIzaSyAY_qSimSG7I9qFqoAkMTrAUCI0WYKrJ-o",
    "authDomain": "krishworks-314e6.firebaseapp.com",
    "projectId": "krishworks-314e6",
    "storageBucket": "krishworks-314e6.appspot.com",
    "messagingSenderId": "333343314476",
    "appId": "1:333343314476:web:104dbf734e1d80f06bb789",
    "measurementId": "G-XDH18GF173",
    "databaseURL":"https://krishworks-314e6-default-rtdb.firebaseio.com/"
}
# Initialising database,auth and firebase for further use
firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()
 
def signIn(request):
    return render(request,"firebase/Login.html")

def home(request):
    print(request.session)
    return render(request,"firebase/Home.html")
 
def postsignIn(request):
    email=request.POST.get('email')
    pasw=request.POST.get('pass')
    try:
        # if there is no error then signin the user with given email and password
        user=authe.sign_in_with_email_and_password(email,pasw)
    except:
        message="Invalid Credentials!!Please ChecK your Data"
        return render(request,"firebase/Login.html",{"message":message})
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    return render(request,"firebase/Home.html",{"email":email})
 
def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request,"firebase/Login.html")
 
def signUp(request):
    return render(request,"firebase/Registration.html")
 
def postsignUp(request):
    email = request.POST.get('email')
    passs = request.POST.get('pass')
    name = request.POST.get('name')
    try:
        # creating a user with the given email and password
        user=authe.create_user_with_email_and_password(email,passs)
        uid = user['localId']
        print(uid)
        # return render(request,"firebase/Login.html")
        return redirect('/')
    except Exception as e:
        print(e)
        return render(request, "firebase/Registration.html", {"message":"Invalid data! Kindly retry"})

def reset(request):
    return render(request, "firebase/Reset.html")
 
def postReset(request):
    email = request.POST.get('email')
    try:
        print('here')
        authe.send_password_reset_email(email)
        message  = "A email to reset password is successfully sent. kindly visit the link to change your password."
        return render(request, "firebase/Login.html", {"msg":message})
    except:
        message  = "Something went wrong, Please check the email you provided is registered or not"
        return render(request, "firebase/Reset.html", {"msg":message})