import stripe
from django.conf import settings
import stripe.api_resources

def generate_stripe_url(unit_amount, cart_id, success_url, cancel_url):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": unit_amount,
                    "product_data": {
                        "name": f"Hello in stripe payment",
                    },
                },
                "quantity": 1,
            }
        ],
        payment_intent_data={"metadata": {"cart_id": cart_id}},
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return checkout_session.url