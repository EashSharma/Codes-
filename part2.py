import sys 
import random
# device structure 
class device:
	dev_id = 0 # current device id
	rec_time = 0 # time at which device received the chunk
	chunk_rec = 0 # check for whether device has the chunk or not
	chunk_rec_from = 0 # device id from which the device received the chunk
	dev_list = [] # list of devices which receives the chunk from this device
	degree = 0 # degree of the device 
	neighbours = {} #neighbours of the device 
	is_super = 0


# function for sorting
def takerec(device_):
	return device_.rec_time


# taking input
f = open(sys.argv[1],'r')
s_id = int(sys.argv[2])
per_s = float(sys.argv[3])
per_l = float(sys.argv[4])
# dictionary for maping device id with devices 
diction_struct={}
count =0
# for finding the degree of the device 
for readline in f:
	count+=1
	sv_list = readline.split(';');
	v_list = []
	if len(sv_list) == 3:
		for i in sv_list:
			v_list.append(int(i))
		dev_id1 = v_list[1]
		dev_id2 = v_list[2]

		if diction_struct.has_key(dev_id1) == 0:
			temp = device()
			temp.dev_id = dev_id1
			temp.neighbours = {}
			temp.rec_time = 0 
			temp.chunk_rec = 0 
			temp.chunk_rec_from = 0 
			temp.dev_list = []  
			temp.degree = 0 
			temp.is_super = 0
			diction_struct[dev_id1] = temp

		if diction_struct.has_key(dev_id2) == 0:
			temp = device()
			temp.dev_id = dev_id2
			temp.neighbours = {}
			temp.rec_time = 0 
			temp.chunk_rec = 0 
			temp.chunk_rec_from = 0 
			temp.dev_list = []  
			temp.degree = 0 
			temp.is_super = 0
			diction_struct[dev_id2] = temp
		
		
		if (diction_struct[dev_id1].neighbours.has_key(dev_id2) == 0) and (diction_struct[dev_id2].neighbours.has_key(dev_id1) == 0):
			diction_struct[dev_id1].degree+=1
			diction_struct[dev_id2].degree+=1			
			diction_struct[dev_id1].neighbours[dev_id2] = diction_struct[dev_id2]
			diction_struct[dev_id2].neighbours[dev_id1] = diction_struct[dev_id1]			
#reporting the output of the file for degree count 
degree_output = open("degreeoutput.csv",'w')
degree_output.write("device id, degree of the device\n")
for key,value in diction_struct.iteritems():
	degree_output.write(str(key)+","+str(value.degree)+"\n")

f.close()
degree_output.close()

# dictionary for device id and degree mapping 
degree_device = {}
for key,value in diction_struct.iteritems():
	degree_device[key]=value.degree

# sorting the dictionary accoring to degree 
temp_count = 0

num_super = 0
num_normal = 0
num_least = 0

for key,value in sorted(degree_device.iteritems(), key= lambda (k,v): (v,k)):
	temp_count+=1
	if temp_count <= (len(degree_device)*(per_l/100)):
		diction_struct[key].is_super=1
	else:
		break 
num_least = temp_count 
temp_count = 0		
for key,value in sorted(degree_device.iteritems(), key= lambda (k,v): (v,k), reverse = True):
	temp_count+=1
	if temp_count <= (len(degree_device)*(per_s/100)):
		diction_struct[key].is_super=2
	else:
		break
num_super = temp_count 
num_normal = len(degree_device)-num_super-num_least
# factors for the calculations 

total_super = 0
total_normal = 0
total_least = 0

# output file 
result = open("result.csv",'w')
result.write("trans. prob. to super nodes, time to reach 90 percent of devices, percent of devices reached,copies of chunk made, average transmissions made by super nodes, average transmissions made by normal nodes, average transmissions made by least nodes, gini coefficient for super nodes ,gini coefficient for ordinary nodes\n")
# probability of transmission for normal nodes
prob_n = 99

# varying probability of supernodes 
for prob_s in range(1,100):
	print str(prob_s)+"\n"
	# started reading the file
	f = open(sys.argv[1],'r')
	# total device recieved
	num_dev_rec = 0

	# current time 
	current_time = 0

	# array of devices which received the chunk 
	device_array=[]
	# giving chunk to the starting device
	for key,value in diction_struct.iteritems():
		diction_struct[key].rec_time = 0 
		diction_struct[key].chunk_rec = 0 
		diction_struct[key].chunk_rec_from = 0 
		diction_struct[key].dev_list = []

	diction_struct[s_id].chunk_rec = 1
	device_array.append(diction_struct[s_id])
	num_dev_rec=1



	total_super = 0
	total_normal = 0
	total_least = 0


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

			# chunck exchange between devices 
			x = random.randint(0,100)
			if (diction_struct[dev_id1].chunk_rec == 1) and (diction_struct[dev_id2].chunk_rec == 0):
				if diction_struct[dev_id2].is_super == 2:
					if x <= prob_s :
						diction_struct[dev_id1].dev_list.append(dev_id2)
						diction_struct[dev_id2].chunk_rec = 1
						diction_struct[dev_id2].chunk_rec_from = dev_id1
						diction_struct[dev_id2].rec_time = current_time 
						device_array.append(diction_struct[dev_id2])
						num_dev_rec+=1
						if diction_struct[dev_id1].is_super == 2:
							total_super+=1
						elif diction_struct[dev_id1].is_super == 0:
							total_normal+=1
						elif diction_struct[dev_id1].is_super == 1:	
							total_least+=1
				elif diction_struct[dev_id2].is_super == 0:
					if x <= prob_n :
						diction_struct[dev_id1].dev_list.append(dev_id2)
						diction_struct[dev_id2].chunk_rec = 1
						diction_struct[dev_id2].chunk_rec_from = dev_id1
						diction_struct[dev_id2].rec_time = current_time 
						device_array.append(diction_struct[dev_id2])
						num_dev_rec+=1
						if diction_struct[dev_id1].is_super == 2:
							total_super+=1
						elif diction_struct[dev_id1].is_super == 0:
							total_normal+=1
						elif diction_struct[dev_id1].is_super == 1:	
							total_least+=1
				elif diction_struct[dev_id2].is_super == 1:
					diction_struct[dev_id1].dev_list.append(dev_id2)
					diction_struct[dev_id2].chunk_rec = 1
					diction_struct[dev_id2].chunk_rec_from = dev_id1
					diction_struct[dev_id2].rec_time = current_time 
					device_array.append(diction_struct[dev_id2])
					num_dev_rec+=1
					if diction_struct[dev_id1].is_super == 2:
						total_super+=1
					elif diction_struct[dev_id1].is_super == 0:
						total_normal+=1
					elif diction_struct[dev_id1].is_super == 1:	
						total_least+=1
			elif (diction_struct[dev_id2].chunk_rec == 1) and (diction_struct[dev_id1].chunk_rec==0):	
				if diction_struct[dev_id1].is_super == 2:
					if x <= prob_s :
						diction_struct[dev_id2].dev_list.append(dev_id1)
						diction_struct[dev_id1].chunk_rec = 1
						diction_struct[dev_id1].chunk_rec_from = dev_id2
						diction_struct[dev_id1].rec_time = current_time 
						device_array.append(diction_struct[dev_id1])
						num_dev_rec+=1
						if diction_struct[dev_id2].is_super == 2:
							total_super+=1
						elif diction_struct[dev_id2].is_super == 0:
							total_normal+=1
						elif diction_struct[dev_id2].is_super == 1:	
							total_least+=1
				elif diction_struct[dev_id1].is_super == 0:
					if x <= prob_n :
						diction_struct[dev_id2].dev_list.append(dev_id1)
						diction_struct[dev_id1].chunk_rec = 1
						diction_struct[dev_id1].chunk_rec_from = dev_id2
						diction_struct[dev_id1].rec_time = current_time 
						device_array.append(diction_struct[dev_id1])
						num_dev_rec+=1
						if diction_struct[dev_id2].is_super == 2:
							total_super+=1
						elif diction_struct[dev_id2].is_super == 0:
							total_normal+=1
						elif diction_struct[dev_id2].is_super == 1:	
							total_least+=1
				elif diction_struct[dev_id1].is_super == 1:
					diction_struct[dev_id2].dev_list.append(dev_id1)
					diction_struct[dev_id1].chunk_rec = 1
					diction_struct[dev_id1].chunk_rec_from = dev_id2
					diction_struct[dev_id1].rec_time = current_time 
					device_array.append(diction_struct[dev_id1])
					num_dev_rec+=1
					if diction_struct[dev_id2].is_super == 2:
						total_super+=1
					elif diction_struct[dev_id2].is_super == 0:
						total_normal+=1
					elif diction_struct[dev_id2].is_super == 1:	
						total_least+=1

	# sorting the list of devices who received the chunk
	device_array.sort( key = takerec)						
	prob_n-=1						

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
	aver_s = (1.0*total_super)/num_super
	aver_n = (1.0*total_normal)/num_normal
	aver_l = (1.0*total_least)/num_least 
	summ =0

	temp_super = []
	temp_ordinary = []

	for xi,vi in diction_struct.iteritems():
		if vi.is_super == 2 :
			temp_super.append(vi)
		elif vi.is_super == 0 :
			temp_ordinary.append(vi)
	for vi in temp_super:
		for vj in temp_super:
			summ+= abs(len(vi.dev_list)-len(vj.dev_list))
	s=0
	for vi in temp_super:
		s+=len(vi.dev_list)
	s= 2*len(temp_super)*s
	gini_super = (summ*1.0)/s
	summ =0
	for vi in temp_ordinary:
		for vj in temp_ordinary:
			summ+= abs(len(vi.dev_list)-len(vj.dev_list))
	s=0
	for vi in temp_ordinary:
		s+=len(vi.dev_list)
	s= 2*len(temp_ordinary)*s
	gini_ordinary = (summ*1.0)/s
	result.write(str(prob_s)+","+str(time_rec_count)+","+str(percent_dev_rec)+","+str(number_devices_reached-1)+","+str(aver_s)+","+str(aver_n)+","+str(aver_l)+","+str(gini_super)+","+str(gini_ordinary)+"\n")
	f.close()

result.close()


