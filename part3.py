import sys 
import random
import math

# device structure 
class device:
	dev_id = 0  # current device id
	rec_time = 0 # time at which device received the chunk
	chunk_rec = 0 # check for whether device has the chunk or not
	chunk_rec_from = 0 # device id from which the device received the chunk
	dev_list = [] # list of devices which receives the chunk from this device
	mclass = -1 
# function for sorting
def takerec(device_):
	return device_.rec_time

# array of devices which received the chunk 
device_array=[]

# dictionary for maping device id with devices 
diction_struct={}


# modularity class input 
g = open(sys.argv[2],'r')
for readline in g:
	sv_list = readline.split(';');
	v_list = []
	for i in sv_list:
		v_list.append(int(i))

	dev_id1 = v_list[0] 
	if diction_struct.has_key(dev_id1) == 0:
		temp = device()
		temp.dev_id = dev_id1  
		temp.rec_time = 0 
		temp.chunk_rec = 0 
		temp.chunk_rec_from = 0 
		temp.dev_list = []
		temp.mclass = v_list[1]
		diction_struct[dev_id1] = temp

# taking input
f = open(sys.argv[1],'r')
s_id = 26

# total device recieved
num_dev_rec = 0

# current time 
current_time = 0

# output file 
result = open("result.csv",'a+')

# giving chunk to the starting device

diction_struct[s_id].chunk_rec =1 
device_array.append(temp)
num_dev_rec=1

#probability change 
y = int(sys.argv[3])
x = 100-y 

# started reading the file 
for readline in f:
	sv_list = readline.split(';');
	v_list = []
	if len(sv_list) == 3:
		
		for i in sv_list:
			v_list.append(int(i))
		# updating time 
		current_time = v_list[0]
		dev_id1 = v_list[1]
		dev_id2 = v_list[2]


		q = random.randint(0,100)
		# chunck exchange between devices 
		if (diction_struct[dev_id1].chunk_rec == 1) and (diction_struct[dev_id2].chunk_rec == 0):
			if diction_struct[dev_id1].mclass == diction_struct[dev_id2].mclass :
				if q <= x :		
					diction_struct[dev_id1].dev_list.append(dev_id2)
					diction_struct[dev_id2].chunk_rec = 1
					diction_struct[dev_id2].chunk_rec_from = dev_id1
					diction_struct[dev_id2].rec_time = current_time 
					device_array.append(diction_struct[dev_id2])
					num_dev_rec+=1
			else:
				if q <= y :
					diction_struct[dev_id1].dev_list.append(dev_id2)
					diction_struct[dev_id2].chunk_rec = 1
					diction_struct[dev_id2].chunk_rec_from = dev_id1
					diction_struct[dev_id2].rec_time = current_time 
					device_array.append(diction_struct[dev_id2])
					num_dev_rec+=1
		elif (diction_struct[dev_id2].chunk_rec == 1) and (diction_struct[dev_id1].chunk_rec==0):
			if diction_struct[dev_id1].mclass == diction_struct[dev_id2].mclass : 
				if q <= x :		
					diction_struct[dev_id2].dev_list.append(dev_id1)
					diction_struct[dev_id1].chunk_rec = 1
					diction_struct[dev_id1].chunk_rec_from = dev_id2
					diction_struct[dev_id1].rec_time = current_time 
					device_array.append(diction_struct[dev_id1])
					num_dev_rec+=1
			else:
				if q <= y :
					diction_struct[dev_id2].dev_list.append(dev_id1)
					diction_struct[dev_id1].chunk_rec = 1
					diction_struct[dev_id1].chunk_rec_from = dev_id2
					diction_struct[dev_id1].rec_time = current_time 
					device_array.append(diction_struct[dev_id1])
					num_dev_rec+=1


# sorting the list of devices who received the chunk
device_array.sort( key = takerec)

#time at which 90 percent of devices gets the chunk
time_rec_count = -100
temp_c = 0


# finding time at which 90 percent of devices receives chunk
for temp in device_array:
	temp_c+=1
	if temp_c >= len(diction_struct)*0.9 :
		time_rec_count = temp.rec_time 
		break

summ=0

for xi,vi in diction_struct.iteritems():
	for xj,vj in diction_struct.iteritems():
		summ += abs(len(vi.dev_list)-len(vj.dev_list))
s= 0
for xi,vi in diction_struct.iteritems():
	s+=len(vi.dev_list)
s= (2*len(diction_struct)*s)

gini = (summ*1.0)/s	

#total percent of devices which receives the chunk
percent_dev_rec = (len(device_array)*100.0)/len(diction_struct)
number_devices_reached = len(device_array)
result.write(str(y)+","+str(x)+","+str(time_rec_count)+","+str(percent_dev_rec)+","+str(number_devices_reached-1)+","+str(gini)+"\n")
result.close()
f.close()
