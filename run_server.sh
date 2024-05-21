lsof -i:80 | awk '{print "kill -9 " $2}' | sh -x
nohup python3 ./run.py &
