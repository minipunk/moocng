# -*- coding: utf-8 -*-

# Copyright 2013 Rooter Analysis S.L.
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

from cgi import escape
import logging

from django.core.exceptions import ValidationError
from tastypie.validation import Validation

from moocng.courses.models import Question, Option

logger = logging.getLogger(__name__)


class AnswerValidation(Validation):

    def _gen_message(self, username, reply, should_be):
        return 'Reply from user %s for option %s is should be %s but is %s' % (
            username, reply['option'], should_be,
            escape(unicode(type(reply['value']))))

    def is_valid(self, bundle, request=None):
        questionID = None
        if 'question' in bundle.data:
            questionID = bundle.data['question'].split('/')[-2]

        if (questionID is not None) and (len(bundle.data['replyList']) > 0):
            try:
                question = Question.objects.get(id=questionID)
                for reply in bundle.data['replyList']:
                    option = question.option_set.get(id=reply['option'])
                    msg = None

                    if (option.optiontype == 't') and (not isinstance(reply['value'], basestring)):
                        msg = self._gen_message(request.user.username, reply, 'text')
                    elif (option.optiontype in ['c', 'r']) and (not isinstance(reply['value'], bool)):
                        msg = self._gen_message(request.user.username, reply, 'boolean')

                    if msg is not None:
                        logger.error(msg)
                        raise ValidationError(msg)
            except Question.DoesNotExist:
                msg = 'Question %s does not exist' % questionID
                logger.error(msg)
                raise ValidationError(msg)
            except Option.DoesNotExist:
                msg = 'Option %s does not exist' % reply['option']
                logger.error(msg)
                raise ValidationError(msg)

        return {}
