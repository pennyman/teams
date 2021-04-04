# -*- coding: utf-8 -*-

from __future__ import print_function

import boto3
import json
import logging

from base64 import b64decode
from urllib2 import Request, urlopen, URLError, HTTPError

TEAMS_CHANNEL = 'prod-aws'  # Enter the Slack channel to send a message to

HOOK_URL = "https://outlook.office.com/webhook/xxxxxx/IncomingWebhook/d5c3166cdfb64b04ae5138a4d908e3c2/20738ef7-fe46-4ce7-87d7-a53176474834"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info("Event: " + str(event))
    message = json.loads(event['Records'][0]['Sns']['Message'])
    logger.info("Message: " + str(message))

    alarm_name = message['AlarmName']
    new_state = message['NewStateValue']
    reason = message['NewStateReason']

    notification_message = {
        'title': " % s" % (alarm_name),
        'text': " % s : % s" % (new_state, reason)
    }

    req = Request(HOOK_URL, json.dumps(notification_message))

    try:
        response = urlopen(req)
        response.read()
        # logger.info("Message posted to %s", notification_message['channel'])
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)
