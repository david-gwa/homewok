import threading

class myThread(threading.Thread):

	def __init__(self, *args, **kwargs):
		super(myThread, self).__init__(*args, **kwargs)

	def run(self):
		print("run ... from start()")


if __name__ == "__main__":
	demo = myThread()
	demo.start()
	demo.join()
