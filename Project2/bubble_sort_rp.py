# Python program for implementation of Bubble Sort
import sys
def bubbleSort(list_data):
    n = len(list_data)

    for i in range(0,n):
        for j in range(0, n-i-1):
            if int(list_data[j]) > int(list_data[j+1]) :
                list_data[j], list_data[j+1] = list_data[j+1], list_data[j]
 
# Driver code to test above
f_r = open(sys.argv[1],'r')
content = f_r.readlines()
f_r.close()

bubbleSort(content)
 
f_w = open(sys.argv[2],'w')
for i in range(0, len(content)):
    f_w.write(content[i])
f_w.close()
