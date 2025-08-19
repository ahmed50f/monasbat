from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .utils import generate_stripe_url
import stripe

@api_view(["GET"])
@permission_classes((AllowAny,))
def stripe_initialize(request, unit_amount=30000, cart_id=1, success_url=None, cancel_url=None):
    success_url = "https://shawarma.cyparta.com/success"
    cancel_url = "https://shawarma.cyparta.com/failed"
    url = generate_stripe_url(unit_amount, cart_id, success_url, cancel_url)
    return redirect(url)

@api_view(["POST"])
@csrf_exempt
@permission_classes((AllowAny,))
def stripe_webhook(request):
    payload = request.body
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    event = None
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    
    # Correct Event to Handle Business Logic:
    # For Basic Payment Completion: The most reliable event to handle payment confirmation and perform your business logic (e.g., updating order status, fulfilling the order) is checkout.
    # session.completed. This event is triggered when the customer successfully completes the checkout process and the payment is confirmed.
    
    # checkout.session.completed: This event occurs when the checkout session completes, indicating that the customer has gone through the Stripe Checkout page successfully.
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        payment_intent_id = session.get("payment_intent")

        if payment_intent_id:
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            print(payment_intent['metadata'])
            cart_id = payment_intent["metadata"]["cart_id"]
            print("completed", cart_id)

    # payment_intent.created: This is triggered when a PaymentIntent is created, which happens when the customer begins the payment process.
    if event["type"] == "payment_intent.created":
        session = event["data"]["object"]
        print(session['metadata'])
        cart_id = session["metadata"]["cart_id"]
        print("created", cart_id)

    # payment_intent.succeeded: This is triggered when the payment is successfully completed.
    if event["type"] == "payment_intent.succeeded":
        session = event["data"]["object"]
        print(session['metadata'])
        cart_id = session["metadata"]["cart_id"]
        print("succeeded", cart_id)

    # charge.succeeded: Triggered when a charge has been successfully completed. This event can be useful for confirming the transaction was fully processed.
    if event["type"] == "charge.succeeded":
        session = event["data"]["object"]
        print(session['metadata'])
        cart_id = session["metadata"]["cart_id"]
        print("succeeded1", cart_id)
    
    # charge.updated: This is triggered if there are any updates to the charge after it was created (for example, if there was an authorization issue or the charge was disputed).
    if event["type"] == "charge.updated":
        session = event["data"]["object"]
        print(session['metadata'])
        cart_id = session["metadata"]["cart_id"]
        print("updated", cart_id)

    return HttpResponse(status=200)