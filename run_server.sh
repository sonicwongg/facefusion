ps aux | grep python3 | awk '{print "kill -9 " $2}' | sh -x
nohup python3 ./server.py &
