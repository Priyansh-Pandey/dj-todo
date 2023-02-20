from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage 

from . import models
from myadmin import models as myadmin_models
import time

MEDIA_URL=settings.MEDIA_URL

#middleware to check session for user routes
def sessioncheckuser_middleware(get_response):
	def middleware(request):
		if request.path=='/user/' or request.path=='/user/searchproduct/' or request.path=='/user/searchsubcat/' :
			if request.session['sunm']==None or request.session['srole']!="user":
				response = redirect('/login/')
			else:
				response = get_response(request)
		else:
			response = get_response(request)		
		return response	
	return middleware


# Create your views here.

def funds(request):
	paypalURL="https://www.sandbox.paypal.com/cgi-bin/webscr"
	paypalID="sb-a43fyl25078745@business.example.com"
	amt=100
	return render(request,"funds.html",{"sunm":request.session["sunm"],"paypalURL":paypalURL,"paypalID":paypalID,"amt":amt})

def payment(request):
 uid=request.GET.get("uid")
 amt=request.GET.get("amt")  
 p=models.Funds(uid=uid,amt=int(amt),info=time.asctime())
 p.save()
 return redirect("/user/success/")

def success(request):
 return render(request,"success.html",{"sunm":request.session["sunm"]})

def cancel(request):
 return render(request,"cancel.html",{"sunm":request.session["sunm"]})

def userhome(request):
    return render(request,"userhome.html",{"sunm":request.session["sunm"]})

def searchproduct(request):
    clist=myadmin_models.Category.objects.all()
    return render(request,"searchproduct.html",{"clist":clist,"MEDIA_URL":MEDIA_URL,"sunm":request.session["sunm"]})    

def searchsubcat(request):
    cnm=request.GET.get("cnm")
    clist=myadmin_models.Category.objects.all()
    sclist=myadmin_models.SubCategory.objects.filter(catname=cnm)
    return render(request,"searchsubcat.html",{"cnm":cnm,"clist":clist,"sclist":sclist,"MEDIA_URL":MEDIA_URL,"sunm":request.session["sunm"]})        

def addproduct(request):
	clist=myadmin_models.Category.objects.all()	
	if request.method=="GET":
		return render(request,"addproduct.html",{"clist":clist,"sunm":request.session["sunm"],"output":""})
	else:
		title=request.POST.get("title")
		catname=request.POST.get("catname")
		subcatname=request.POST.get("subcatname")
		description=request.POST.get("description")
		price=request.POST.get("price")
		info=time.asctime()

		filename=""
		file_list=request.FILES.getlist('picon')

		for row in file_list:
			fs = FileSystemStorage()
			s = fs.save(row.name,row)
			filename+=(s+",")

		p=models.Product(title=title,catname=catname,subcatname=subcatname,description=description,price=price,piconname=filename,info=info)
		p.save()
		return render(request,"addproduct.html",{"clist":clist,"sunm":request.session["sunm"],"output":"Product Added Successfully...."})
		
def fetchSubCategoryAJAX(request):
	cnm=request.GET.get("c")
	sclist=myadmin_models.SubCategory.objects.filter(catname=cnm)
	option_str="<option>Select Sub Category</option>"
	for row in sclist:
		option_str+=("<option>"+row.subcatname+"</option>")
	return HttpResponse(option_str);

def productlist(request):
	cnm=request.GET.get("cnm")
	scnm=request.GET.get("scnm")
	sclist=myadmin_models.SubCategory.objects.filter(catname=cnm)
	plist=models.Product.objects.filter(subcatname=scnm)
	return render(request,"productlist.html",{"cnm":cnm,"scnm":scnm,"plist":plist,"sclist":sclist,"MEDIA_URL":MEDIA_URL,"sunm":request.session["sunm"]})	 