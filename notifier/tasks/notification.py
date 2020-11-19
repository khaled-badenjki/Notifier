from notifier.extensions import celery
import time


@celery.task(rate_limit="5/m")
def get_sms_api(notification_id, phone, text):
    time.sleep(10)
    # Integration with SMS provider goes here.
    # If everything is ok, return True
    return {"status": True}
