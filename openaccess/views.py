
import json
import time
import hmac
from hashlib import sha1

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView

from openaccess.models import UserProfile

class IndexView(TemplateView):
    template_name = 'openaccess/index.html'


# Taken from django docs
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class AnalysisView(LoginRequiredMixin, TemplateView):
    template_name = 'openaccess/analysis.html'

    def get_context_data(self, **kwargs):
        context = super(AnalysisView, self).get_context_data(**kwargs)
        try:        
            profile = self.request.user.userprofile
        except UserProfile.DoesNotExist: 
            profile = UserProfile(user=self.request.user)
            profile.setup_user()
            profile.save() 
        secret = settings.OPENACCESS_GATEONE_SECRET
        auth_obj = {
            'api_key': settings.OPENACCESS_GATEONE_KEY,
            'upn': profile.username,
            'timestamp': str(int(time.time() * 1000)),
            'signature_method': 'HMAC-SHA1',
            'api_version': '1.0',
        }
        hash = hmac.new(secret, digestmod=sha1)
        hash.update(auth_obj['api_key'] + auth_obj['upn'] + auth_obj['timestamp'])
        auth_obj['signature'] = hash.hexdigest()
        context['gateone_auth_obj'] = json.dumps(auth_obj)
        context['gateone_connect_url'] = 'ssh://%s@172.16.18.16' % profile.username
        context['gateone_url'] = settings.OPENACCESS_GATEONE_URL
        return context
