import sys
import numpy as np
from draw_semantic_graph import read_adjacent_matrix, draw_semantic_graph
from create_adjacent_matrix import *

EPSILON_1 = 0.00001
EPSILON_2 = 0.000000001
DAMPING_FACTOR = 0.85
ITERATION_LIMIT = 100


def create_prob_matrix_from_adjacent_matrix(adjacent_matrix):
	keys = adjacent_matrix.keys()
	cids = {keys[i] : i  for i in range(len(keys))}

	matrix_size = len(cids)
	init_matrix = np.zeros((matrix_size, matrix_size))
	matrix = np.matrix(init_matrix)


	for cid in cids:
		pos = cids[cid]
		adjacents = adjacent_matrix[cid]
		if len(adjacents) == 0:
			continue

		sum_weight = reduce(lambda x, y: x + y, adjacents.values())
		for adjacent in adjacents:
			weight = adjacents[adjacent]
			adj_pos = cids[adjacent]
			matrix[pos, adj_pos] = float(weight) / sum_weight



	for i in range(matrix_size):
		matrix[i, i] = EPSILON_1

	return matrix, cids

def page_rank(prob_matrix):
	nodes_count = int(prob_matrix.size ** 0.5)
	print "Page rank. Nodes count ->", nodes_count
	prob_vector = np.matrix([1.0 / nodes_count for i in range(nodes_count)])
	
	delta = np.dot(prob_vector.tolist()[0], prob_vector.tolist()[0]) 
	identity_row = np.matrix([1.0  for i in range(nodes_count)])
	print delta
	print prob_vector

	while (delta >= EPSILON_2):
		v2 = DAMPING_FACTOR * (prob_vector * prob_matrix) + identity_row * ((1.0 - DAMPING_FACTOR) / nodes_count)
		v3 = (prob_vector - v2).tolist()[0]
		delta = np.dot(v3 ,v3) 
		prob_vector = v2
		print delta
		print prob_vector

	return prob_vector
	

def write_results(results, cids, result_file):
	file = open(result_file, "w")

	for cid in cids:
		file.write(str(cid) + ' ' + str(results[cids[cid]]) + '\n')

	file.close()

# Page rank with creation adjacent matrix
if __name__=="__main__":
	if len(sys.argv) != 7:
		print "Error in input parameters"
		print "type %s <cids_file> <cid_aid1_file> <aid1_aid2_file> \
				<features_file> <cms_file> <result_file>" % sys.argv[0]
		exit()


	cids_file = sys.argv[1]
	cid_aid1_file = sys.argv[2]
	aid1_aid2_file = sys.argv[3]
	features_file = sys.argv[4]
	cms_file = sys.argv[5]
	result_file = str(sys.argv[6])

	cids = read_cids(cids_file)
	print len(cids)

	aid1_cid = get_aid1_cid(cid_aid1_file, cids)
	print len(aid1_cid)

	aid2_cid = get_cid_aid2(aid1_aid2_file, aid1_cid)
	print len(aid2_cid)

	features = read_features(features_file)
	features = {
		"GENRES" : 0,
		# "COUNTRY": 0,
		# "CALLSIGN": 0,
		# "KEYWORDS": 0,
		# "TAGS": 0,
		# "TYPE": 0,
		# "SUMMARY": 0,
		# "YEAR": 0,
		# "PREMIERE_DATE": 0
	}
	print len(features)

	adjacent_matrix = get_adjacent_matrix(aid2_cid, features, cms_file)
	prob_matrix, cids = create_prob_matrix_from_adjacent_matrix(adjacent_matrix)
	results = page_rank(prob_matrix)
	results = results.tolist()[0]
	write_results(results, cids, result_file)



# Page rank with reading adjacent matrix from file
# if __name__=="__main__":
# 	if len(sys.argv) != 4:
# 		print "Error in input parameters"
# 		print "type %s <adjacent_matrix_file> <output.dot> <result_file>" % sys.argv[0]
# 		exit()

# 	adjacent_matrix_file = str(sys.argv[1])
# 	output = str(sys.argv[2])
# 	result_file = str(sys.argv[3])
	
# 	adjacent_matrix = read_adjacent_matrix(adjacent_matrix_file)
# 	draw_semantic_graph(adjacent_matrix, output)

# 	prob_matrix, cids = create_prob_matrix_from_adjacent_matrix(adjacent_matrix)


# 	results = page_rank(prob_matrix)

# 	results = results.tolist()[0]

# 	write_results(results, cids, result_file)
