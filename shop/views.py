from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ProductForm
from django.contrib import messages
from .credentials import *
from .models import Product


def shop_home(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'product saved')
            return redirect('home')
        else:
            messages.error(request, 'product not saved')
            return redirect('shop')
    else:
        form = ProductForm()
    return render(request, 'shop/shop_home.html', {'form': form})


def delete(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    messages.success(request, 'product deleted')
    return redirect('home')


# def update_view_product(request, id):
# product = Product.objects.get(id=id)
# if request.method == 'POST':
# product_name = request.POST.get('name')
# product_qtty = request.POST.get('qtty')
# product_price = request.POST.get('price')
# product_desc = request.POST.get('desc')
# product_image = request.FILES.get('image')
# product.name = product_name
# product.qtty = product_qtty
# product.price = product_price
# product.desc = product_desc
# product.image = product_image
# product.save()
# messages.success(request, 'product updated')
# return redirect('home')

# return render(request, 'shop/updateProduct.html', {'product': product})


def pay(request, id):
    product = Product.objects.get(id=id)
    if request.method == "POST":
        phone = request.POST['phone']
        amount = product.price
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPassword.Business_short_code,
            "Password": LipanaMpesaPassword.decode_password,
            "Timestamp": LipanaMpesaPassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "PYMENT001",
            "TransactionDesc": "School fees"
        }

        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse("success")
    return render(request, 'shop/pay.html', {'product': product})
