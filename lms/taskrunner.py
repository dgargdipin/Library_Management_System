from datetime import time
from lms.task import emailsend

from redis import Redis
import rq
queue = rq.Queue('emailsend', connection=Redis.from_url('redis://'))
email_data={'email':'dgargdipin@gmail.com','name':'Dipin','book_name':'Intro to algos'}

job = queue.enqueue(emailsend, email_data)
print(job.get_id())
print(job.result)   # => None

# Now, wait a while, until the worker is finished
time.sleep(2)
print(job.result)


