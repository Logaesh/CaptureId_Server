import socket
import timeit
import time
import datetime
import threading

Raw_image_path = "/home/pi/Project_ocr/IMAGE SERVER FILES/images/fisheye"

def RetrFile(name,s):
	#while(1):
	
		#host = '169.254.25.148'
		#port = 5000

	    	#s = socket.socket()
    		#s.connect((host, port))
	#while(1):
    		ackResponse = s.recv(1024)
		print (ackResponse)
    		if ackResponse == "1":
			print("capture id connected...")
			s.send("1")
			filesize=int(s.recv(1024))
			#filename=str(s.recv(1024))
			ts=time.time()
			st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
			id="id"
			st = id+st
			ext = ".jpg"
			filename = st+ext
			f = open(filename, 'wb')
			packets=0;
                	data = s.recv(1024)
                	totalRecv = len(data)
                	f.write(data)
                	while totalRecv < filesize:
                    		data = s.recv(1024)
                    		totalRecv += len(data)
                   		f.write(data)
				packets=packets+1
                    		#print "{0:.2f}".format((totalRecv/float(filesize))*100)+ "% Done"
                	print "Download Completed with "+str(packets+1)+" packets !"
                	f.close()
			print (filename)
	
    	
			
    



def Main():
    host = '169.254.25.148'
    port = 5000


    s = socket.socket()
    s.bind((host,port))

    s.listen(5)
    
    os.chdir(Raw_image_path)
    print "Server Started."
    while True:
	#if (GPIO.input(INPUT_PIN)==False):
		c, addr = s.accept()
	        print "client connedted ip:<" + str(addr) + ">"
	        t = threading.Thread(target=RetrFile, args=("RetrThread", c))
        	t.start()
    s.close()

if __name__ == '__main__':
    Main()