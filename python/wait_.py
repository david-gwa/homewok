
import asyncio


async def cor1(name):
	print("executing: ", name)
	await asyncio.sleep(1)
	print("executed: ", name)

loop = asyncio.get_event_loop()
tasks = [cor1("zj_" + str(i)) for i in range(3)]
wait_cor = asyncio.wait(tasks)
loop.run_until_complete(wait_cor)
loop.close()
