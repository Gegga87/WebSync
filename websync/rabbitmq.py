#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='130.240.110.14'))

channel = connection.channel()

channel.exchange_declare(exchange='logs',
                             type='fanout')

def emit_log(txt):
    channel.basic_publish(exchange='logs',
                          routing_key='',
                          body=txt)
    print " [x] Sent %r" % (txt,)
    connection.close()

def receive_logs():
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='logs',
                       queue=queue_name)

    print ' [*] Waiting for logs. To exit press CTRL+C'

    def callback(ch, method, properties, body):
        print " [x] %r" % (body,)

    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)

    channel.start_consuming()    