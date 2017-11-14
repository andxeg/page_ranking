import sys
import time
import random
from Queue import Queue
from threading import Thread
from draw_semantic_graph import draw_semantic_graph


def read_adjacent_matrix(filename):
	'''
		Adjacent matrix description
		{
			cid: {
				cid : w,
				...
				cid : w
			}

			...

			cid: {
				cid : w,
				...
				cid : w
			}
		}
	'''

	adjacent_matrix = {}

	file = open(filename, "r")
	line = file.readline()

	while line != "":
		list = line.split()
		cid = list[0]
		if cid not in adjacent_matrix:
			adjacent_matrix[cid] = {}

		for adjacent in list[1:]:
			adj_cid, weight = adjacent.split(':')
			adjacent_matrix[cid][adj_cid] = int(weight)

		line = file.readline()

	file.close()

	return adjacent_matrix


def send_ball_in_graph(adjacent_matrix, balls_path_limit, output_queue):
	result = {str(cid) : 0 for cid in adjacent_matrix}
	current_cid = adjacent_matrix.keys()[random.randint(0, len(adjancent_matrix))]
	result[current_cid] += 1
	path_length = 0

	while path_length < balls_path_limit:
		adjacent_cids = adjacent_matrix[current_cid].keys()
		next_cid = adjacent_cids[random.randint(0, len(adjacent_cids))]
		current_cid = next_cid
		result[current_cid] += 1
		path_length += 1

	return result


def test(number, output_queue):
	time.sleep(2)
	print "input -> %d, output -> %d" % (number, number ** 2)
	output_queue.put(number**2)
	output_queue.task_done()
	return

if __name__=="__main__":
	if len(sys.argv) != 4:
		print "Error in input parameters" 
		print "type %s <filename_with_adjacent_matrix> <balls_count> <balls_path_limit>" % sys.argv[0]
		exit()
	
	filename = str(sys.argv[1])
	balls_count = int(sys.argv[2])
	balls_path_limit = int(sys.argv[3])

	adjacent_matrix = read_adjacent_matrix(filename)

	print adjacent_matrix

	draw_semantic_graph(adjacent_matrix, "output.dot")

	exit()
	#

	threads = []
	queue = Queue()

	for i in range(balls_count):
		thread = Thread(target=send_ball_in_graph, args=(adjacent_matrix, balls_path_limit, q))
		threads.append(thread)
		thread.start()

	for thread in threads:
		thread.join()

	results = {str(cid) : 0 for cid in adjacent_matrix}
	while not q.empty():
		result = q.get()
		for cid in result:
			if cid not in results:
				results[cid] = 0
			results[cid] += int(result[cid])

	print results
