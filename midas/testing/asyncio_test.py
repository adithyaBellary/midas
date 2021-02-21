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

# async def n():
#   while True:
#     print('we are in the added function')
#     await asyncio.sleep(1)

# def add_new_periodic():
#   loop = asyncio.get_event_loop()
#   loop.run_until_complete(asyncio.gather(
#     n()
#   ))

async def coro():
  while True:
    await asyncio.sleep(3)
    print('in the coro, slept for 3')

# async def coro_wrapper():
#   await coro()

async def main():
  print('in main()')
  loop = asyncio.get_event_loop()
  task = asyncio.ensure_future(coro())
  # loop.run_until_complete(asyncio.gather(
  #   task()
  # ))
  # await task
  print('done w the task')
  # loop.run_until_complete(asyncio.gather(
  #   periodic(),
  #   new_periodic()
  # ))


if __name__ == '__main__':
  # main()
  asyncio.run(main())