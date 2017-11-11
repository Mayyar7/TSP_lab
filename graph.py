import csv
import numpy as np
from math import sin, cos, sqrt, atan2, radians

points = []
d = {}
count = 0

with open('isd-history.csv') as csvfile:
    read_csv = csv.reader(csvfile, delimiter=',')
    for p in read_csv :
    	if (p[3] == "IN"):
    		if(p[6]=="" and p[7] == "") : 
    			continue
    		else :
    			temp = [int(p[0]),float(p[6]),float(p[7])]
    			points.append(temp)
    			d[count] = []
    			d[count].append(temp)
    			count=count+1

points = np.matrix(points)

def dist(p1,p2):
	R = 6373.0


	lat1 = radians(p1[0,1])
	lon1 = radians(p1[0,2])
	lat2 = radians(p2[0,1])	
	lon2 = radians(p2[0,2])

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = R * c
	return distance


def ajc_mat (points):
	distance_matrix = np.asmatrix(np.zeros((points.shape[0], points.shape[0])))
	
	for i in range(0,len(points)):
		for j in range(0,len(points)):
			if (j<i):
				distance_matrix[i,j]= distance_matrix[j,i]
			else:
				distance_matrix[i,j]= dist(points[i],points[j])
	return distance_matrix
		

def knn (distance_matrix,k):
	neighbour = []
	for j,i in enumerate(distance_matrix):
		index = np.argpartition(i,k+1)
		index = list(np.transpose(index))
		temp = [x for x in index[:k+1] if x!=j]
		temp = np.transpose(temp)
		temp = temp[0][0]
		print(temp)
		neighbour.append(temp)

	return neighbour

def construct_adj_mat(neighbour):
	length = len(neighbour)
	adj_matrix = np.array(np.zeros((length,length)))
	for i in range(length):
		adj_matrix[i,neighbour[i]]=1
		# print(adj_matrix)
		# break
	print(adj_matrix)



f = ajc_mat(points)
# print(f)
neighbour=knn(f,3)
neighbour = construct_adj_mat(neighbour)

