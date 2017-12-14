#!/usr/bin/env python

import logging
from kombu import Exchange, Queue
from celery_connectors.utils import ev
from celery_connectors.build_ssl_options import build_ssl_options
from celery_connectors.log.setup_logging import setup_logging
from celery_connectors.run_jtoc_relay import run_jtoc_relay


# Credits and inspirations from these great sources:
#
# https://github.com/celery/kombu/blob/master/examples/rpc-tut6/rpc_server.py
# https://gist.github.com/oubiwann/3843016
# https://gist.github.com/eavictor/ee7856581619ac60643b57987b7ed580#file-mq_kombu_rpc_server-py
# https://github.com/Skablam/kombu-examples
# https://gist.github.com/mlavin/6671079

setup_logging()
name = ev("APP_NAME", "jtoc_relay")
log = logging.getLogger(name)


broker_url = ev("BROKER_URL", "pyamqp://rabbitmq:rabbitmq@localhost:5672//")
exchange_name = ev("EXCHANGE_NAME", "ecomm.api")
exchange_type = ev("EXCHANGE_TYPE", "topic")
queue_name = ev("QUEUE_NAME", "ecomm.api.west")
routing_key = ev("ROUTING_KEY", "ecomm.api.west")
prefetch_count = int(ev("PREFETCH_COUNT", "1"))
priority_routing = {"high": "ecomm.api.west",
                    "low": "ecomm.api.east"}
use_exchange = Exchange(exchange_name, type=exchange_type)
use_queue = Queue(queue_name, exchange=use_exchange, routing_key=routing_key)
task_queues = [
    use_queue
]
ssl_options = build_ssl_options()

relay_broker_url = ev("RELAY_BROKER_URL", "pyamqp://rabbitmq:rabbitmq@localhost:5672//")
relay_backend_url = ev("RELAY_BROKER_URL", "redis://localhost:6379/10")
relay_exchange_name = ev("RELAY_EXCHANGE_NAME", "")
relay_exchange_type = ev("RELAY_EXCHANGE_TYPE", "direct")
relay_routing_key = ev("RELAY_ROUTING_KEY", "reporting.payments")
relay_exchange = Exchange(relay_exchange_name, type=relay_exchange_type)

transport_options = {}

log.info(("Consuming queues={}")
         .format(len(task_queues)))

run_jtoc_relay(broker_url=broker_url,
               ssl_options=ssl_options,
               transport_options=transport_options,
               task_queues=task_queues,
               prefetch_count=prefetch_count,
               relay_broker_url=relay_broker_url,
               relay_backend_url=relay_backend_url,
               relay_exchange=relay_exchange,
               relay_exchange_type=relay_exchange_type,
               relay_routing_key=relay_routing_key)

log.info("Done")
