from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from mydjapp import models as mydjapp_models
from . import models 

#middleware to check session for admin routes
def sessioncheckmyadmin_middleware(get_response):
	def middleware(request):
		if request.path=='/myadmin/' or request.path=='/myadmin/manageusers/' or request.path=='/myadmin/manageuserstatus/' or request.path=='/myadmin/addcategory/' or request.path=='/myadmin/addsubcategory/' or request.path=='/myadmin/cpadmin/' or request.path=='/myadmin/epadmin/' :
			if request.session['sunm']==None or request.session['srole']!="admin":
				response = redirect('/login/')
			else:
				response = get_response(request)
		else:
			response = get_response(request)		
		return response	
	return middleware

# Create your views here.


def adminhome(request):
    return render(request,"adminhome.html",{"sunm":request.session["sunm"]})

def manageusers(request):
    userDetails=mydjapp_models.Register.objects.filter(role="user")
    return render(request,"manageusers.html",{"userDetails":userDetails,"sunm":request.session["sunm"]})     

def manageuserstatus(request):
    regid=int(request.GET.get("regid"))
    s=request.GET.get("s")    
    
    if s=="block":
        mydjapp_models.Register.objects.filter(regid=regid).update(status=0)
    elif s=="verify":
        mydjapp_models.Register.objects.filter(regid=regid).update(status=1)        
    else:
        mydjapp_models.Register.objects.filter(regid=regid).delete()

    return redirect("/myadmin/manageusers/")             

def addcategory(request):
    if request.method=="GET":
        return render(request,"addcategory.html",{"output":"","sunm":request.session["sunm"]})
    else:
        catname=request.POST.get("catname")
        caticon=request.FILES["caticon"]
        fs = FileSystemStorage()
        filename = fs.save(caticon.name,caticon)
        p=models.Category(catname=catname,caticonname=filename)
        p.save()    
        return render(request,"addcategory.html",{"output":"Category added successfully....","sunm":request.session["sunm"]})

def addsubcategory(request):
    clist=models.Category.objects.all()
    if request.method=="GET":
        return render(request,"addsubcategory.html",{"clist":clist,"output":"","sunm":request.session["sunm"]})
    else:
        catname=request.POST.get("catname")
        subcatname=request.POST.get("subcatname")
        caticon=request.FILES["caticon"]
        fs = FileSystemStorage()
        filename = fs.save(caticon.name,caticon)
        p=models.SubCategory(catname=catname,subcatname=subcatname,subcaticonname=filename)
        p.save()    
        return render(request,"addsubcategory.html",{"clist":clist,"output":"SubCategory added successfully....","sunm":request.session["sunm"]})                

def cpadmin(request):
    sunm=request.session["sunm"]
    if request.method=="GET":       
        return render(request,"cpadmin.html",{"sunm":sunm,"output":""})
    else:
        opass=request.POST.get("opass")
        npass=request.POST.get("npass")    
        cnpass=request.POST.get("cnpass")

        userDetails=mydjapp_models.Register.objects.filter(email=sunm,password=opass)
        if len(userDetails)>0:
            if npass==cnpass:
                mydjapp_models.Register.objects.filter(email=sunm).update(password=cnpass)
                msg="Password changes successfully , please login"
            else:    
                msg="New & Confirm new password mismatch"                
        else:    
            msg="Invalid old password , please try again"
        return render(request,"cpadmin.html",{"sunm":sunm,"output":msg})            

def epadmin(request):
    sunm=request.session["sunm"]
    if request.method=="GET":
        userDetails=mydjapp_models.Register.objects.filter(email=sunm)    
        m,f="",""
        if userDetails[0].gender=="male":
            m="checked"
        else:
            f="checked"    
        return render(request,"epadmin.html",{"userDetails":userDetails[0],"sunm":sunm,"output":"","m":m,"f":f})
    else:
        name=request.POST.get('name')
        email=request.POST.get('email')
        mobile=request.POST.get('mobile')
        address=request.POST.get('address')
        city=request.POST.get('city')
        gender=request.POST.get('gender')
        mydjapp_models.Register.objects.filter(email=email).update(name=name,mobile=mobile,address=address,city=city,gender=gender)        
        return redirect("/myadmin/epadmin/")                



