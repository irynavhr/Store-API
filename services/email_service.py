import os
import resend

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")

resend.api_key = RESEND_API_KEY


# REGISTRATION NOTIFICATION
def send_registration_email(to_email: str, bonuses_earned: int):

    resend.Emails.send({
        "from": EMAIL_FROM,
        "to": to_email,
        "subject": "Registration successful",
        "html": f"""
            <h1>Welcome!</h1>
            <p>Your account was successfully created.</p>
            <p>You earned {bonuses_earned} bonuses for the registration!</p>
            <p>Enjoy shopping with us!</p>
        """
    })


# ORDER CREATED NOTIFICATION
def send_order_created_email(
    to_email: str,
    order_id: int,
    bonuses_earned: int,
    current_bonus_balance: int
):

    resend.Emails.send({
        "from": EMAIL_FROM,
        "to": to_email,
        "subject": "Order created",
        "html": f"""
            <h1>Order #{order_id}</h1>
            <p>Your order was successfully created.</p>
            <p> Bonuses earned: {bonuses_earned}</p>
            <p> Current bonus balance: {current_bonus_balance}</p>
        """
    })


# STATUS CHANGE NOTIFICATION
def send_order_status_email(
    to_email: str,
    order_id: int,
    status: str
):

    resend.Emails.send({
        "from": EMAIL_FROM,
        "to": to_email,
        "subject": f"Order #{order_id} status updated",
        "html": f"""
            <p>Your order status changed to:
            <b>{status}</b></p>
        """
    })