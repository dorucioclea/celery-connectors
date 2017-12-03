#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
import logging
from celery import Celery
from celery_connectors.utils import ev

from celery_connectors.logging.setup_logging import setup_logging
from celery_connectors.subscriber import Subscriber

setup_logging()

name = "run-redis-subscriber"

log = logging.getLogger(name)

log.info("Start - {}".format(name))


def handle_message(body, message):
    log.info("recv msg props={} body={}".format(message, body))
    recv_msgs.append(body)
    message.ack()
# end of handle_message


# You can also pass in already-initialized Celery applications too:
app = Celery()
sub = Subscriber("redis-subscriber", ev("BROKER_URL", "redis://localhost:6379/0"), app)

recv_msgs = []


# Now send:
msg = {"account_id": 123}
dst_queue = "reporting.accounts"
sub.consume(callback=handle_message,
            dst_queue_name=dst_queue,
            dst_ex_name=None,
            routing_key=None)

log.info("End - {}".format(name))
