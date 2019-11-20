import pika

channel = None


def on_connected(connection):
    """Called when we are fully connected to RabbitMQ"""
    # Open a channel
    connection.channel(on_open_callback=on_channel_open)


def on_channel_open(new_channel):
    """Called when our channel has opened"""
    global channel
    channel = new_channel
    channel.queue_declare(queue="hello", callback=on_queue_declared)


def on_queue_declared(frame):
    """Called when RabbitMQ has told us our Queue has been declared, frame is the response from RabbitMQ"""
    channel.basic_consume('hello', handle_delivery)


def handle_delivery(channel, method, header, body):
    """Called when we receive a message from RabbitMQ"""
    print(body)


credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('172.17.0.2', 5672, '/', credentials=credentials)
connection = pika.SelectConnection(parameters, on_open_callback=on_connected)

try:
    # Loop so we can communicate with RabbitMQ
    connection.ioloop.start()
except KeyboardInterrupt:
    # Gracefully close the connection
    connection.close()
    # Loop until we're fully closed, will stop on its own
    connection.ioloop.start()
