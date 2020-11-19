from notifier.models.customer import Customer
from notifier.translations import translations


def process_text(text, extra_params, customer_id, is_dynamic):
    """Translate text based on customer language"""
    customer = Customer.query.get(customer_id)
    language = customer.language
    text = translations[language][text]

    """Populate provided extra params, if dynamic message"""
    if not is_dynamic:
        return text
    for extra_param in extra_params:
        text = text.replace(extra_param["key"], extra_param["value"])

    """Populate personalized params, if dynamic message"""
    customer = Customer.query.get(customer_id)
    customer_params = [
        {
            "key": "@calculate_customer_name",
            "value": customer.name,
        },
        {
            "key": "@calculate_customer_email",
            "value": customer.email,
        },
        {
            "key": "@calculate_customer_phone",
            "value": customer.phone,
        },
    ]
    for customer_param in customer_params:
        text = text.replace(customer_param["key"], customer_param["value"])

    return text
