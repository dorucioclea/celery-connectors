#!/usr/bin/env python

import logging
from celery_connectors.utils import ev
from celery_connectors.log.setup_logging import setup_logging
from celery_connectors.publisher import Publisher

setup_logging()

name = "publish-user-conversion-events"

log = logging.getLogger(name)

log.info("Start - {}".format(name))

exchange_name = ev("CONVERSIONS_EXCHANGE", "user.events")
queue_name = ev("CONVERSIONS_QUEUE", "user.events.conversions")
routing_key = ev("CONVERSIONS_ROUTING_KEY", "user.events.conversions")
auth_url = ev("BROKER_URL", "amqp://rabbitmq:rabbitmq@localhost:5672//")
serializer = "json"

# import ssl
# Connection("amqp://", login_method='EXTERNAL', ssl={
#               "ca_certs": '/etc/pki/tls/certs/something.crt',
#               "keyfile": '/etc/something/system.key',
#               "certfile": '/etc/something/system.cert',
#               "cert_reqs": ssl.CERT_REQUIRED,
#          })
#
ssl_options = {}
app = Publisher("publish-uce-rabbitmq",
                auth_url,
                ssl_options)

if not app:
    log.error("Failed to connect to broker={}".format(auth_url))
else:

    log.info("Building message")

    # Now send:
    body = {"account_id": 111,
            "subscription_id": 222,
            "stripe_id": 333,
            "product_id": "DEF"}

    log.info("Sending user conversion event msg={} ex={} rk={}".format(body, exchange_name, routing_key))

    send_result = app.publish(
        body=body,
        exchange=exchange_name,
        routing_key=routing_key,
        queue=queue_name,
        serializer=serializer,
        retry=True)

    log.info("End - {}".format(name))
# end of valid or not