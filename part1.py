import sys 

# device structure 
class device:
	dev_id = 0  # current device id
	rec_time = 0 # time at which device received the chunk
	chunk_rec = 0 # check for whether device has the chunk or not
	chunk_forwarded = 0 # count for k
	chunk_rec_from = 0 # device id from which the device received the chunk
	dev_list = [] # list of devices which receives the chunk from this device

# function for sorting
def takerec(device_):
	return device_.rec_time


# taking input
f = open(sys.argv[1],'r')
k = int(sys.argv[2])
s_id = int(sys.argv[3])


# total device recieved
num_dev_rec = 0

# current time 
current_time = 0

# output file 
result = open("result.csv",'a+')

# array of devices which received the chunk 
device_array=[]

# dictionary for maping device id with devices 
diction_struct={}

# giving chunk to the starting device
temp = device()
temp.dev_id = s_id
temp.chunk_rec = 1
temp.chunk_forwarded = k
diction_struct[s_id] = temp
device_array.append(temp)
num_dev_rec=1


count=0
# started reading the file 
for readline in f:
	count+=1
	sv_list = readline.split(';');
	v_list = []
	if len(sv_list) == 3:
		
		for i in sv_list:
			v_list.append(int(i))
		# updating time 
		current_time = v_list[0]
		dev_id1 = v_list[1]
		dev_id2 = v_list[2]
		
		# checking whether the devices is in the list or not 
		if diction_struct.has_key(dev_id1) == 0:
			temp = device()
			temp.dev_id = dev_id1
			temp.chunk_forwarded = k
			diction_struct[dev_id1] = temp

		if diction_struct.has_key(dev_id2) == 0:
			temp = device()
			temp.dev_id = dev_id2
			temp.chunk_forwarded = k
			diction_struct[dev_id2] = temp

		# chunck exchange between devices 
		if (diction_struct[dev_id1].chunk_rec == 1) and (diction_struct[dev_id1].chunk_forwarded > 0) and (diction_struct[dev_id2].chunk_rec == 0):
			diction_struct[dev_id1].chunk_forwarded-=1
			diction_struct[dev_id1].dev_list.append(dev_id2)
			diction_struct[dev_id2].chunk_rec = 1
			diction_struct[dev_id2].chunk_rec_from = dev_id1
			diction_struct[dev_id2].rec_time = current_time 
			device_array.append(diction_struct[dev_id2])
			num_dev_rec+=1
		elif (diction_struct[dev_id2].chunk_rec == 1) and (diction_struct[dev_id2].chunk_forwarded > 0) and (diction_struct[dev_id1].chunk_rec==0):
			diction_struct[dev_id2].chunk_forwarded-=1
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


#total percent of devices which receives the chunk
percent_dev_rec = (len(device_array)*100.0)/len(diction_struct)
number_devices_reached = len(device_array)
result.write(str(k)+","+str(time_rec_count)+","+str(percent_dev_rec)+","+str(number_devices_reached-1)+"\n")
result.close()
f.close()

