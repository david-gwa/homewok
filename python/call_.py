def tick_():
	print("tick ..")


def run(callback=None):
	if callback:
		callback()
	print("run ...")


def main():
	run(tick_)

if __name__ == "__main__":
	main()
