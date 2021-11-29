# sumayya created this projects

from django.shortcuts import render,redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages


# Create your views here.
def home(request):
	import requests
	import json

	if request.method =='POST':
		ticker=request.POST['ticker']
		api_request=requests.get("https://cloud.iexapis.com/stable/stock/"  +  ticker  +  "/quote?token=pk_835797ad8b34457289aa597814deada1")
		try:
			api=json.loads(api_request.content)
		except Exception as e:
			api="Errors..."	
		return render(request,'home.html',{'api':api})
	
	else:
		return render(request,'home.html',{'ticker':"Enter The Ticker Symbol Above"})
			
def about(request):
	return render(request,'about.html')	

def add_stock(request):
	import requests
	import json
	if request.method =='POST':
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request,('Stock has been add success'))
			return redirect('add-stock')
		
	else:
		ticker=Stock.objects.all()
		output=[]
		for ticker_item in ticker:
			api_request=requests.get("https://cloud.iexapis.com/stable/stock/"  +  str(ticker_item)  +  "/quote?token=pk_835797ad8b34457289aa597814deada1")
			try:
				api=json.loads(api_request.content)
				output.append(api)
			except Exception as e:
				api="Errors..."	


		return render(request,'add_stock.html',{'ticker':ticker,'output':output})


def delete(request,stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request,('stock has been deleted'))
	return redirect('add-stock')


def delete_stock(request):
	ticker=Stock.objects.all()

	return render(request,'delete_stock.html',{'ticker':ticker})	

	
