from notifier.extensions import celery
import time


@celery.task(rate_limit="50/m")
def get_sms_api(notification_id, phone, text):
    time.sleep(2)
    # Integration with SMS provider goes here.
    # If everything is ok, return True
    return {"status": True}


@celery.task(rate_limit="60/m")
def get_push_api(notification_id, registration_id, text):
    time.sleep(2)
    # Integration with push notification provider goes here.
    # If everything is ok, return True
    return {"status": True}
