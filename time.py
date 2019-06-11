import time
import datetime

t = time.time()
sec = int(t)

print(sec)

xz = "2018-04-10 23:59:50"
timeArray = time.strptime(xz, "%Y-%m-%d %H:%M:%S")
timeStamp = int(time.mktime(timeArray))
print(timeStamp)
