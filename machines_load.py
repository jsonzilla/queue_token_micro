from deta import Deta
import time

# ONLY for the first deploy

deta = Deta(<deta project key>)
machines = deta.Base("machines")

m = [
{ "key": "token", "machine": "id", "user": "John Doe" },
]

# for each 25 items in the list, insert them into the db
def insert_many(list):
  for i in range(0, len(list), 25):
    step = list[i:i+25]
    promise = machines.put_many(step)
    consume_promise(promise, step)


def consume_promise(promise, step):
  if 'processed' in promise:
    print("Processed:", promise['processed'])
  else:
    print("Error:", promise['error'])
    print("Step:", step)
    exit()

  time.sleep(1)


if __name__=="__main__":
  insert_many(m)
  print("done")