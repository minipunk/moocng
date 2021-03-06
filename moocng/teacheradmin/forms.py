# Copyright 2012 Rooter Analysis S.L.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django import forms
from django.utils.translation import ugettext_lazy as _

from tinymce.widgets import TinyMCE

from moocng.courses.forms import AnnouncementForm as CoursesAnnouncementForm
from moocng.courses.models import Course
from moocng.forms import BootstrapMixin, BootstrapClearableFileInput, HTML5DateInput
from moocng.teacheradmin.models import MassiveEmail


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        exclude = ('slug', 'teachers', 'owner', 'students')
        widgets = {
            'start_date': HTML5DateInput(),
            'end_date': HTML5DateInput(),
            'certification_banner': BootstrapClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget

            if isinstance(widget, (forms.widgets.TextInput, forms.widgets.DateInput)):
                widget.attrs['class'] = 'input-xlarge'

            elif isinstance(widget, forms.widgets.Textarea):
                widget.mce_attrs['width'] = '780'  # bootstrap span10


class AnnouncementForm(CoursesAnnouncementForm, BootstrapMixin):

    send_email = forms.BooleanField(
        required=False,
        label=_(u'Send the announcement via email to all the students in this course'),
        initial=False,
        help_text=_(u'Please use this with caution as some courses has many students'),
    )


class MassiveEmailForm(forms.ModelForm, BootstrapMixin):

    class Meta:
        model = MassiveEmail
        exclude = ('course', )
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'input-xxlarge'}),
            'message': TinyMCE(attrs={'class': 'input-xxlarge'}),
        }
