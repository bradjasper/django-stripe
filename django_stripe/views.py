from django.http import Http404, HttpResponse
from django.utils import simplejson as json
from django.views.decorators.csrf import csrf_exempt

from .signals import *

EVENT_SIGNAL_MAP = {
    'recurring_payment_failed': recurring_payment_failed,
    'invoice_ready': invoice_ready,
    'recurring_payment_succeeded': recurring_payment_succeeded,
    'subscription_trial_ending': subscription_trial_ending,
    'subscription_final_payment_attempt_failed': subscription_final_payment_attempt_failed,
    'ping': ping,
}

@csrf_exempt
def webhook_to_signal(request):
    if 'json' not in request.POST:
        raise Http404

    message = json.loads(request.POST.get('json'))
    event = message.get('event')

    if event not in EVENT_SIGNAL_MAP:
        raise Http404

    signal = EVENT_SIGNAL_MAP.get(event)
    signal.send(sender=webhook_to_signal, **message)

    return HttpResponse()
