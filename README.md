python_mpqueue_vs_rabbitmq
=====================

Simple test script to compare messaging performance of Python's multiprocessing.Queue and Rabbit MQ.

Results with pika.BlockingConnection

    run number 100000
    
    mpqueue received message_count 100000 exiting
    multiprocessing.Queue run time 1.04472184181 seconds, 0.00001 seconds per iteration
    
    rabbitmq_consumer starting
    rabbitmq received message_count 100000 exiting last message 1
    
    rabbitmq run time 318.613850832 seconds, 0.00319 seconds per iteration

Results with pika.SelectConnection

    run number 100000
    
    mpqueue received message_count 100000 exiting
    multiprocessing.Queue run time 1.03926706314 seconds, 0.00001 seconds per iteration
    
    rabbitmq_consumer starting
    rabbitmq run time 18.1656091213 seconds, 0.00018 seconds per iteration
