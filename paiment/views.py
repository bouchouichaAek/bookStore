from django.shortcuts import render, redirect, get_object_or_404
from books.cart import Cart
from .forms import *
from django.contrib import messages
from django.conf import settings
from .order_info import *
from .models import *
from django.http import JsonResponse
from .services import create_invoice
import hashlib
import hmac
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST



# Create your views here.


def cart(request):

    context = {}
    return render(request, 'paiment/cart.html', context)


def checkout(request):
    cart = Cart(request)
    if len(cart) > 0:

        if request.user.is_authenticated and len(AddresShiping.objects.filter(user=request.user)):
            get_addres = AddresShiping.objects.get(
                user=request.user)
            dileveryaddress = dilevery_address(stats=get_addres.stats, first_name=get_addres.user.first_name, last_name=get_addres.user.last_name,
                                               phone_number=get_addres.phone_number, address_complete=get_addres.address_complete, postal_code=get_addres.postal_code, city=get_addres.city)
            cart.add_address(dileveryaddress)

        addres_form = AddresSipingForm(initial=cart.get_dilevery_address())
        if request.method == "POST":
            addres_form = AddresSipingForm(request.POST)
            state = request.POST.get("stats")
            firtsname = request.POST.get("firtsname")
            lastname = request.POST.get("lastname")
            phone_number = request.POST.get("phone_number")
            city = request.POST.get("city")
            postal_code = request.POST.get("postal_code")
            address_complete = request.POST.get("address_complete")
            check = request.POST.get("remember")

            if addres_form.is_valid():
                if request.user.is_authenticated and len(AddresShiping.objects.filter(user=request.user)) > 0:
                    check = True
                if check:
                    if request.user.is_authenticated:
                        try:
                            addres_form = AddresSipingForm(
                                request.POST, instance=AddresShiping.objects.get(user=request.user))

                        except AddresShiping.DoesNotExist:
                            print('An exception occurred')
                        else:
                            addres_form = AddresSipingForm(
                                request.POST, instance=AddresShiping.objects.get(user=request.user))
                        addres_form = addres_form
                        addres = addres_form.save(commit=False)
                        addres.user = request.user
                        addres.save()
                        get_addres = AddresShiping.objects.get(
                            user=request.user)
                        dileveryaddress = dilevery_address(stats=get_addres.stats, first_name=get_addres.user.first_name, last_name=get_addres.user.last_name,
                                                           phone_number=get_addres.phone_number, address_complete=get_addres.address_complete, postal_code=get_addres.postal_code, city=get_addres.city)
                        cart.add_address(dileveryaddress)
                    else:
                        messages.error(
                            request, "عليك ان تسجل الدخول لتحفظ بيانتك", extra_tags="saveAddresError")

                else:
                    dileveryaddress = dilevery_address(stats=State.objects.get(pk=state), first_name=firtsname, last_name=lastname,
                                                       phone_number=phone_number, address_complete=address_complete, postal_code=postal_code, city=city)
                    cart.add_address(dileveryaddress)

            return redirect("checkout")

    else:
        return redirect("our-books")

    address = cart.get_dilevery_address()
    payment = cart.get_payment_method()
    promo = cart.get_code_promo()
    context = {
        "title": "إنهاء الدفع",
        "address": address,
        "payment": payment,
        "promo": promo,
        "addres_form": addres_form,
    }
    return render(request, 'paiment/checkout.html', context)


def add_method_payment(request):
    cart = Cart(request)
    if request.method == "POST":
        select_payment_method = request.POST.get("select-payment-method")

        value1, value2 = select_payment_method.split('*')
        cart.add_payment(value1, value2)
        return redirect("checkout")


def add_code_promo(request):
    cart = Cart(request)
    if request.method == "POST":
        code_promo = request.POST.get("code_promo")
        if len(CodePromo.objects.filter(code=code_promo)) > 0:
            if len(CodePromo.objects.filter(code=code_promo, is_valide=True)) > 0:
                cart.add_promo(CodePromo.objects.get(code=code_promo))
            else:
                messages.error(
                    request, "كود الخصم الذي أدخلته غير صالح ", extra_tags="codePromoError")
        else:
            messages.error(
                request, "كود الخصم الذي أدخلته غير موجود", extra_tags="codePromoError")

        return redirect("checkout")


def create_payment(request):
    cart = Cart(request)

    if cart.get_payment_method()["payment"] == "الدفع أون لاين":
        if cart.get_dilevery_address()!= {}:
            if request.method == 'POST':
                amount = cart.get_total_price()
                back_url = request.build_absolute_uri(reverse('home'))

                try:
                    invoice = create_invoice(amount, back_url)
                    delivery_state = State.objects.get(state_name=cart.get_dilevery_address()["stats"])
                    customer_name = cart.get_dilevery_address()["first_name"] +" "+ cart.get_dilevery_address()["last_name"]
                    order = Order(customer=customer_name, order_fk=invoice["id"],stats=delivery_state,phone_number=cart.get_dilevery_address()["phone_number"],address_complete=cart.get_dilevery_address()["address_complete"],postal_code=cart.get_dilevery_address()["postal_code"],city=cart.get_dilevery_address()["city"],total_price=cart.get_total_price())
                    order.save()
                    for value in cart.cart.items():
                        book_item  = OrderItem(order=order,product=value[1]["book"],quantity=value[1]["quantity"],total_price=value[1]["total_price"])
                        book_item.save()
                    cart.clear()
                    return redirect(invoice['checkout_url'])
                except Exception as e:
                    return JsonResponse({'error': str(e)}, status=400)
            return JsonResponse({'error': 'Invalid request method'}, status=405)
        else:
            messages.error(
                    request, "أدخل عنوان الشحن من فضلك ", extra_tags="addressShippingDoesNotExist")
        return redirect("checkout")
    else:
        delivery_state = State.objects.get(state_name=cart.get_dilevery_address()["stats"])
        customer_name = cart.get_dilevery_address()["first_name"] +" "+ cart.get_dilevery_address()["last_name"]
        order = Order(customer=customer_name,stats=delivery_state,phone_number=cart.get_dilevery_address()["phone_number"],address_complete=cart.get_dilevery_address()["address_complete"],postal_code=cart.get_dilevery_address()["postal_code"],city=cart.get_dilevery_address()["city"],total_price=cart.get_total_price())
        order.save()
        for value in cart.cart.items():
            book_item  = OrderItem(order=order,product=value[1]["book"],quantity=value[1]["quantity"],total_price=value[1]["total_price"])
            book_item.save()
        cart.clear()
        return redirect("home")


@csrf_exempt
@require_POST
def payment_webhook(request):
    # Handle webhook data
    # This should verify the data and update the payment status in your system
    # Extracting the 'signature' header from the HTTP request
    signature = request.headers.get('signature')

    # Getting the raw payload from the request body
    payload = request.body.decode('utf-8')

    # If there is no signature, ignore the request
    if not signature:
        return HttpResponse(status=400)

    # Calculate the signature
    computed_signature = hmac.new(settings.CHARGILY_SECRET.encode('utf-8'), payload.encode('utf-8'), hashlib.sha256).hexdigest()

    # If the calculated signature doesn't match the received signature, ignore the request
    if not hmac.compare_digest(signature, computed_signature):
        return HttpResponse(status=403)

    # If the signatures match, proceed to decode the JSON payload
    event = json.loads(payload)

    # Switch based on the event type
    if event['type'] == 'checkout.paid':
        checkout = event['data']
        payment_id = Order.objects.get(order_fk=checkout['id'])
        payment_id.payment_status =  "Paid"
        payment_id.save()
        # Handle the successful payment.
    elif event['type'] == 'checkout.failed':
        checkout = event['data']
        payment_id = Order.objects.get(order_fk=checkout['id'])
        payment_id.payment_status =  "Failed"
        payment_id.save()

        # Handle the failed payment.

    # Respond with a 200 OK status code to let us know that you've received the webhook
    return JsonResponse({}, status=200)
