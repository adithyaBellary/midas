import asyncio

def periodic_helper():
  print('i am in the helper')

async def periodic():
  while True:
    periodic_helper()
    await asyncio.sleep(3)

async def new_periodic():
  while True:
    print('new periodic')
    await asyncio.sleep(5)

async def n():
  while True:
    print('we are in the added function')
    await asyncio.sleep(1)

def add_new_periodic():
  loop = asyncio.get_event_loop()
  loop.run_until_complete(asyncio.gather(
    n()
  ))

def main():
  print('in main()')
  loop = asyncio.get_event_loop()
  loop.run_until_complete(asyncio.gather(
    periodic(),
    new_periodic(),
    add_new_periodic()
  ))

if __name__ == '__main__':
  main()