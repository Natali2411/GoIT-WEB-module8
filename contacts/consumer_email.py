import json
from datetime import datetime

from contacts.contact import Contact
from db_connect import connect_mongo_db
from contacts.rabbit_connect import make_channel
from logger import logger

QUEUE_NAME = "email_queue"
channel, connection = make_channel()
channel.queue_declare(queue=QUEUE_NAME, durable=True)
logger.info(" [*] Waiting for messages. To exit press CTRL+C")


def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    logger.info(f" [x] Received {message}")
    logger.info(f"Sending a letter to the email address {message['email']}")
    logger.info(
        f"Change the status of the sent letter in DB for the contact '"
        f"{message['fullname']}' to True"
    )
    connect_mongo_db()
    contact = Contact.objects(email=message["email"]).first()
    if contact:
        contact.update(is_sent_msg=True)
        logger.info(f" [x] Time {datetime.now()} Done: the status has been changed")
    else:
        logger.warning(
            f"The contact with email '{message['email']}' doesn't exist " f"in the DB"
        )
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)


if __name__ == "__main__":
    channel.start_consuming()
    connection.close()
