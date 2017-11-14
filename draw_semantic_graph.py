import sys


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
		if line != '\n':
			cid = list[0]
			if cid not in adjacent_matrix:
				adjacent_matrix[cid] = {}

			for adjacent in list[1:]:
				if adjacent == '\n':
					continue
				adj_cid, weight = adjacent.split(':')
				adjacent_matrix[cid][adj_cid] = int(weight)

		line = file.readline()

	file.close()

	return adjacent_matrix


def draw_semantic_graph(adjacent_matrix, filename):
	file = open(filename, "w")
	file.write("graph G {\n")

	links = {}
	output = []

	for cid in adjacent_matrix:
		file.write(str(cid) + ' '  + '[label= "' + str(cid) + '"];\n')
		adjacents = adjacent_matrix[cid]
		
		for adjacent in adjacents:
			link1 = str(cid) + ':' + str(adjacent)
			link2 = str(adjacent) + ':' + str(cid)
			if not (link1 in links) and not (link2 in links):
				output.append(str(cid) + ' -- ' + str(adjacent) + 
					' [label="' + str(adjacents[adjacent]) +'" color="blue"];\n')
				links[str(cid) + ':' + str(adjacent)] = 0


	for link in output:
		file.write(str(link))

	file.write('}')
	file.close()
	return


if __name__=="__main__":
	if len(sys.argv) != 3:
		print "Error in input parameters"
		print "type %s <adjacent_matrix_filename> <output.dot>" % sys.argv[0]
		exit()

	filename = sys.argv[1]
	output = sys.argv[2]

	adjacent_matrix = read_adjacent_matrix(filename)
	print adjacent_matrix
	draw_semantic_graph(adjacent_matrix, output)
