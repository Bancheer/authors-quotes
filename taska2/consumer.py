import pika
import json
from mongoengine import connect, Document, StringField, BooleanField

connect(host='mongodb+srv://<credentials>@cluster0.fshakdd.mongodb.net/?appName=mongosh+2.0.0')

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='email_queue')

class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)

def send_email(contact_id):
    contact = Contact.objects(id=contact_id).first()
    if contact:
        print(f"Надсилаємо email до {contact.email}...")
        contact.message_sent = True
        contact.save()
        print("Email надіслано.")

def callback(ch, method, properties, body):
    data = json.loads(body)
    contact_id = data['contact_id']
    send_email(contact_id)

def consume_messages():
    channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

    print("Очікування повідомлень. Для виходу натисніть Ctrl+C")
    channel.start_consuming()

if __name__ == "__main__":
    consume_messages()