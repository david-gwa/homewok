import logging 
import os 

class log(object):
    def __init__(self, logger_name):
        self.log = logging.getLogger(logger_name)
        self.log.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        self.log.addHandler(console_handler)
    
    def set_output_file(self, filename):
        file_handler = logging.FileHandler(filename)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.log.addHandler(file_handler)

def main():
    test = log('scenario-mm')
    file_name = "record.log" 
    dir_name = "/c/gwa/python_test/ott"
    try:
        os.makedirs(dir_name)
    except OSError:
        pass 
    file_path =  os.path.join(dir_name, file_name)
    test.set_output_file(file_path)
    test.log.debug("debug in episode 1...")
    test.log.info("info ...")
    test.log.warning("warn ...")
    test2 = log("zjjj")
    test2.set_output_file('record.log')
    test2.log.info("test2 info")
    test2.log.warning("test2 warn")



if __name__ == "__main__":
    main()


