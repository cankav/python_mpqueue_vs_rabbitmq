from multiprocessing import Process, Queue
import timeit
import pika
import json
import sys 

def mpqueue_producer(run_num, q, message):
    for i in range(run_num):
        q.put(message)

def test_mpqueue(run_num, message):
    # create two processes which will communicate via multiprocessing.Queue
    q = Queue()
    p = Process(target=mpqueue_producer, args=(run_num, q, message))
    p.start()

    message_count = 0
    for i in range(run_num):
        q.get()
        message_count += 1

    p.join()
    print 'mpqueue received message_count', message_count,'exiting'




def rabbitmq_callback(ch, method, properties, body):
    global message_count
    msg = json.loads(body)
    #ch.basic_ack(delivery_tag = method.delivery_tag)

    #print 'received message:', msg
    if msg == 1:
        print 'rabbitmq received message_count', message_count,'exiting last message', msg, '\n'
        sys.exit(1)
    else:
        message_count += 1

def rabbitmq_consumer():
    global message_count
    message_count = 0
    print 'rabbitmq_consumer starting'
    conn = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@localhost:5672/%2F"))
    channel = conn.channel()
    channel.basic_consume(rabbitmq_callback, queue='hello', no_ack=True)
    channel.start_consuming()

def test_rabbitmq(run_num, message):
    p = Process(target=rabbitmq_consumer, args=())
    p.start()

    conn = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@localhost:5672/%2F"))
    channel = conn.channel()
    channel.queue_declare(queue='hello')
    for i in range(run_num):
        channel.basic_publish(exchange='', routing_key='hello', body=json.dumps(message))

    channel.basic_publish(exchange='', routing_key='hello', body='1')




def test():
    run_num = pow(10, 4)
    print 'run number ' + str(run_num) + '\n'
    message = [ 1407919673695, 'USDTRY', 1.300, 5, 1.340, 3, 1.4, 0, 1.3, 1231231, 0.03, 0.034 ]

    mpqueue_time = timeit.timeit(stmt='test_mpqueue(' + str(run_num) + ', ' + str(message) + ')', setup='from __main__ import test_mpqueue', number=1)
    print 'multiprocessing.Queue run time ' + str(mpqueue_time) + ' seconds, %.5f' % (mpqueue_time / run_num) + ' seconds per iteration\n'


    rabbitmq_time = timeit.timeit(stmt='test_rabbitmq(' + str(run_num) + ', ' + str(message) + ')', setup='from __main__ import test_rabbitmq', number=1)
    print 'rabbitmq run time ' + str(rabbitmq_time) + 'seconds, %.5f' % (rabbitmq_time / run_num) + ' seconds per iteration'

if __name__ == "__main__":
    test()

