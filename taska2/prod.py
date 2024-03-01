import pika
import json
from faker import Faker
from mongoengine import connect, Document, StringField, BooleanField
from models import Contact

connect(host='mongodb+srv://<credentials>@cluster0.fshakdd.mongodb.net/?appName=mongosh+2.0.0')

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='email_queue')

fake = Faker()

class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)  

def generate_contacts_and_send_to_queue(num_contacts):
    for i in range(num_contacts):
        contact = Contact(
            fullname = fake.name(),
            email = fake.email()
        ).save()

        channel.basic_publish(
            exchange='',
            routing_key='email_queue',
            body=json.dumps({"contact_id": str(contact.id)})
        )

    print(f"{num_contacts} контактів надіслано до черги RabbitMQ.")

generate_contacts_and_send_to_queue(5)

connection.close()