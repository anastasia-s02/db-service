"""
Conncts to RabbitMQ and processes messages
"""

import dataclasses
import logging
import os
import sys

import msgpack
import pika
import rmq_interface
from dacite import from_dict

from db_service.actions.registry import ACTION_REGISTRY, ActionType
from db_service.connect import ENGINE

logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger(__name__)


@rmq_interface.consumer_function
def consume(
    payload: bytes,
    properties: pika.BasicProperties,  # pylint: disable=unused-argument # fmt: skip
) -> bytes:
    """
    Process message from queue
    """
    try:
        logger.info("Received message; unpacking...")
        data = msgpack.unpackb(payload, raw=False)

        logger.info("Unpacking succeeded; reading action...")
        action_type = ActionType(data["action"])
        action = ACTION_REGISTRY[action_type]

        logger.info(f"Action: {action.name}; processing...")

        data["payload"]["engine"] = ENGINE
        request = from_dict(data_class=action.request_schema, data=data["payload"])
        function_result = action.function(request)

        logger.info("Done processing; sending back...")
        result = msgpack.packb(
            {"data": [dataclasses.asdict(function_result)], "errors": []}
        )
    except Exception as exception:  # pylint: disable=broad-except
        logger.exception(f"Exception in processing message: {str(exception)}")
        result = msgpack.packb({"data": [], "errors": [str(exception)]})
    return result


if __name__ == "__main__":
    interface = rmq_interface.RabbitMQInterface(url_parameters=os.getenv("RMQ_CONNECT"))
    interface.listen(os.getenv("RMQ_TABLENAME"), consume)
