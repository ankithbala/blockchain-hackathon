from django.shortcuts import render
from django.views.generic.base import View

from web3 import Web3, HTTPProvider
from ownermanagement.settings import trufSettings
from web3.contract import ConciseContract
from web3 import eth
from django.contrib.auth.mixins import LoginRequiredMixin
from ownerportal.forms import SetOwnerForm, SellLandForm
from smtplib import fromaddr

web3 = Web3(HTTPProvider(trufSettings["server"]))

Bhoomi=web3.eth.contract(abi=trufSettings["abi"], address=trufSettings["address"])



class HomePageView(View):
    def get(self, request):
        return render(request, "ownerportal/homepage.html")

# Create your views here.
class SetOwnerView(LoginRequiredMixin, View):
    def get(self, request):
        context={
            "form":SetOwnerForm(),
        }
        return render(request, "ownerportal/setowner.html", context)
    
    def post(self, request):
        form=SetOwnerForm(request.POST)
        if form.is_valid():
            landno=int(form.cleaned_data["land_number"])
            owner=form.cleaned_data["owner_name"]
            aadhar=int(form.cleaned_data["aadhar_number"])
            panno=form.cleaned_data["land_number"]
            Bhoomi.transact({"from":web3.eth.coinbase}).setOwner(landno, owner, aadhar, panno)
            return render(request, "ownerportal/setown_succ.html")
        context={
            "form":form,
        }  
        return render(request, "ownerportal/setowner.html", context)

class SellLandView(LoginRequiredMixin, View):
    def get(self, request):
        context={
            "form":SellLandForm(),
        }
        return render(request, "ownerportal/setowner.html", context)
    
    def post(self, request):
        form=SellLandForm(request.POST)
        if form.is_valid():
            landno=int(form.cleaned_data["land_number"])
            fromaadahar=int(form.cleaned_data["from_aadhar"])
            owner=form.cleaned_data["owner_name"]
            aadhar=int(form.cleaned_data["aadhar_number"])
            panno=form.cleaned_data["land_number"]
            Bhoomi.transact({"from":web3.eth.coinbase}).sellLand(landno, fromaadahar, owner, aadhar, panno)
            return render(request, "ownerportal/setown_succ.html")
        context={
            "form":form,
        }  
        return render(request, "ownerportal/setowner.html", context)