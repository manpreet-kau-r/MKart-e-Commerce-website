from django.shortcuts import render
from django.http import HttpResponse
from . models import Product,Contact,Orders,OrderUpdate
from math import ceil
import json

def index(request):

	'''
	products = Product.objects.all()

	n=len(products)
	nSlides = n//4 + ceil( (n/4) - (n//4) )

	allprods = [ [products,range(1,nSlides),nSlides] , [products,range(1,nSlides),nSlides] ] 
	'''

	allprods=[]

	catProds = Product.objects.values('category','id')
	
	cats = { item['category'] for item in catProds }

	for cat in cats:
		prod = Product.objects.filter(category=cat)

		n=len(prod)
		nSlides = n//4 + ceil( (n/4) - (n//4) )

		allprods.append( [ prod,range(1,nSlides),nSlides ] )

	params={'allProds':allprods}
	
	return render(request,'shop/index.html',params)

def about(request):
	return render(request,'shop/about.html')

def contact(request):

	thank = False

	if(request.method=="POST"):

		name=request.POST.get('name','')
		email=request.POST.get('email','')
		phone=request.POST.get('phone','')
		desc=request.POST.get('desc','')
		
		contact=Contact(name=name,email=email,phone=phone,desc=desc)
		contact.save()

		thank = True

	return render(request,'shop/contact.html',{'thank':thank})

def tracker(request):

	if(request.method=="POST"):

		order_id=request.POST.get('orderId','')
		email=request.POST.get('email','')

		try:
			order=Orders.objects.filter(order_id=order_id,email=email)

			if len(order)>0:

				update = OrderUpdate.objects.filter(order_id=order_id)

				updates=[]

				for item in update:     
					updates.append({'text':item.update_desc, 'time': item.timestamp})
					response = json.dumps([updates,order[0].items_json],default=str)
                    
				return HttpResponse(response)
               	
			else:
				return HttpResponse('{}')
   		                     	
		except Exception as e:
			return HttpResponse('{}')

	return render(request,'shop/tracker.html')

def search(request):
	return render(request,'shop/search.html')

def productview(request,myid):
	# Fetch product using id
	product = Product.objects.filter(id=myid)

	return render(request,'shop/productview.html',{'product':product[0]})

def checkout(request):

	if(request.method=="POST"):

		items_json=request.POST.get('itemsJson','')
		name=request.POST.get('name','')
		email=request.POST.get('email','')
		address=request.POST.get('address1', '') + " " + request.POST.get('address2', '')
		city=request.POST.get('city','')
		state=request.POST.get('state','')
		zip_code=request.POST.get('zip_code','')
		phone=request.POST.get('phone','')

		order = Orders(items_json=items_json,name=name,email=email,address=address,city=city,state=state,zip_code=zip_code,phone=phone)
		order.save()

		thank=True
		id=order.order_id

		update = OrderUpdate(order_id=order.order_id,update_desc='This order has been placed.')
		update.save();

		return render(request,'shop/checkout.html',{'thank':thank,'id':id})
	    
	return render(request,'shop/checkout.html')
