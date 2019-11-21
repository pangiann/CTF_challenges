sekrutBuffer = "2906164f2b35301e511b5b144b085d2b56475750164d51515d"

message = "You have now entered the Duck Web, and you're in for a honkin' good time.\nCan you figure out my trick?"

flag = ''
j = 0
for i in range(0, len(sekrutBuffer), 2):

    flag += chr(int(sekrutBuffer[i] +  sekrutBuffer[i+1], 16) ^ ord(message[j]))
    j += 1

print flag
