# email.py is part of the 'TsetseCheckout' package.
# It was written by Gus Dunn and was created on 9/28/14.
#
# Please see the license info in the root folder of this package.

"""
=================================================
email.py
=================================================
Purpose:
Handles sending email to users and admins for the app.
"""
import threading
from flask import render_template, current_app, copy_current_request_context
from flask_mail import Message

from TsetseCheckout.extensions import mail
from TsetseCheckout.settings import Config as config
from TsetseCheckout.decorators import async

import pdb

__author__ = 'Gus Dunn'


def create_message(recipients, subject, template, sender=None, **kwargs):
    if not sender:
        sender = current_app.config['ROBOT_EMAIL']
    if not recipients:
        raise ValueError('Target email not defined.')
    body = render_template(template, **kwargs)
    subject = subject.encode('utf-8')
    body = body.encode('utf-8')
    return Message(subject, recipients, body, sender=sender)

 
def send(recipients, subject, template, sender=None, **kwargs):
    message = create_message(recipients, subject, template, sender, **kwargs)
    mail.send(message)


def send_async(recipients, subject, template, sender=None, **kwargs):
    message = create_message(recipients, subject, template, sender, **kwargs)

    @copy_current_request_context
    def send_message(message):
        mail.send(message)

    sender = threading.Thread(name='mail_sender', target=send_message, args=(message,))
    sender.start()

# @async
# def send_async_email(app, msg):
#     pdb.set_trace()
#     with app.app_context():
#         mail.send(msg)
#
#
# def send_email(subject, sender, recipients, text_body, html_body=None):
#     msg = Message(subject, sender=sender, recipients=recipients)
#     msg.body = text_body
#     msg.html = html_body
#     # mail.send(msg)
#     send_async_email(current_app, msg) #TODO: FINDOUT WHY THIS IS OUT OF APP CONTEXT


def notify_spreadsheet_req_confirm(user, validation_results, passed):
    """
    Sends email confirmation message to `user` upon completion of the validation steps with the results.
    :param user:
    :param validation_results:
    :param passed:
    :return:
    """

    if passed:
        pass_or_fail = "SUCCEEDED"
    else:
        pass_or_fail = "FAILED"

    main_line = "="*50
    mid_line = '-'*25

    details = ["A per line summary of your requests:\n",
               main_line]

    if passed:
        first = True
        for index, req in validation_results:
            if not first:
                details.append(mid_line)
            else:
                first = False

            line = "Line %(req_line)s: RequestNo: %(reqno)s" % {'req_line': index+1, 'reqno': req.id}
            details.append(line)

    else:
        first = True
        for index, req in validation_results:
            if not first:
                details.append(mid_line)
            else:
                first = False

            intro = "Line %(req_line)s errors:" % {'req_line': index+1}
            details.append(intro)

            if req.validation_failures is not None:
                for colname, msg in req.validation_failures.iteritems():
                    details.append("%(colname)s: %(msg)s" % {"colname": colname, "msg": msg})

    details.append(main_line)

    details = '\n'.join(details)

    send_async(recipients=[user.email],
               subject="Your TsetseSampleDB requests.",
               template="email/spreadsheet_requests_confirmation.txt",
               sender=config.MAIL_USERNAME,
               user=user.username,
               pass_or_fail=pass_or_fail,
               details=details)

    # send_email(subject="Your TsetseSampleDB requests.",
    #            sender=config.MAIL_USERNAME,
    #            recipients=[user.email],
    #            text_body=render_template("email/spreadsheet_requests_confirmation.txt",
    #                                      user=user.username,
    #                                      pass_or_fail=pass_or_fail,
    #                                      details=details),
    #            )







