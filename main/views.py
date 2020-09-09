import os
import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from .forms import FileForm
from .models import Upload, Document


def fetch(request, hash):

    if not re.match(r'[0-9a-f]{16,32}', hash):
        raise Http404()

    upld = None
    sec_upld = None
    if request.method == 'POST':
        if 'password' in request.POST:
            try:
                upld = Upload.objects.get(hash_secure=hash, password=request.POST['password'])
            except Upload.DoesNotExist:
                return HttpResponseForbidden()
        else:
            raise HttpResponseNotAllowed()
    else:
        try:
            upld = Upload.objects.get(hash=hash)
        except Upload.DoesNotExist:
            try:
                sec_upld = Upload.objects.get(hash_secure=hash)
            except Upload.DoesNotExist:
                raise Http404()
    return render(request, 'main/download.html', locals())


class UploadView(FormView):
    form_class = FileForm
    template_name = 'main/upload.html'
    success_url = '/'
    files = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UploadView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid() and len(files):
            key = os.urandom(16).hex()
            obj = Upload(user=request.user, timestamp=timezone.now(), hash=key)
            if 'password' in form.cleaned_data and form.cleaned_data['password']:
                obj.hash_secure = key[::-1]  # reverse it
                obj.password = form.cleaned_data['password']
            obj.save()

            for f in files:
                doc = Document(doc=f, upload=obj)
                doc.save()
            messages.success(request, 'Successfully uploaded %d files' % len(files))
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@login_required
def index(request):
    previous = Upload.objects.filter(user=request.user)
    return render(request, 'main/index.html', locals())
