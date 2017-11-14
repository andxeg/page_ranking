import sys
import json


'''
    cids_file - each line is a cid, cid from requests to only one pid
    cid_aid1_file - mapping from cid to aid2. It is 1_content_info.txt
    aid1_aid2_file - mapping from aid1 to aid2. It is 4_T_CMS_CONT_ACCE.txt
    features_file - each line is a feature from 6_T_CMS_CONTENT_EXT.txt
    cms_file - it is a 6_T_CMS_CONTENT_EXT.txt
    output - out-file for result adjacent matrix

    For more information See Table Description.txt and features_from_6_T_CMS.txt

    aid1 has '2'
    aid2 has '1'

'''


def read_cids(cids_file):
    file = open(cids_file, "r")
    cids = {}
    line = file.readline()

    while line != "":
        list = line.split()
        if len(list) >= 1:
            cid = str(list[0])
            cids[cid] = 0
        line = file.readline()

    file.close()
    return cids


def get_aid1_cid(cid_aid1_file, cids):
    file = open(cid_aid1_file, "r")
    aid1_cid = {}
    line = file.readline()
    while line != "":
        list = line.split('|')
        if len(list) >= 2:
            cid = str(list[0])
            aid1 = str(list[1].split('_')[0])
            if cid in cids:
                aid1_cid[aid1] = cid

        line = file.readline()

    file.close()
    return aid1_cid



def get_cid_aid2(aid1_aid2_file, aid1_cid):
    file = open(aid1_aid2_file, "r")
    aid2_cid = {}
    line = file.readline()
    while line != "":
        list = line.split('|')
        if len(list) >= 2:
            list = list[0].split('-')
            if len(list) >= 2:
                aid2 = str(list[0])
                aid1 = str(list[1])
                if aid1 in aid1_cid:
                    aid2_cid[aid2] = aid1_cid[aid1]

        line = file.readline()
        

    file.close()
    return aid2_cid



def read_features(features_file):
    file = open(features_file, "r")
    line = file.readline()
    features = {}
    while line != "":
        list = line.split()
        if len(list) >= 1:
            feature = str(list[0])
            features[feature] = 0
        line = file.readline()

    file.close()
    return features


def get_adjacent_matrix(aid2_cid, features, cms_file):
    file = open(cms_file, "r")
    # feature value
    fvalue_cids = {}
    line = file.readline()
    while line != "":
        list = line.split('|')
        if len(list) == 4:
            aid2 = list[0]
            feature = list[2]
            list = list[3].split()
            if len(list) >= 1:
                fvalue = list[0]
                if fvalue != "" and feature in features and aid2 in aid2_cid:
                    cid = aid2_cid[aid2]
                    if fvalue not in fvalue_cids:
                        fvalue_cids[fvalue] = []
                    fvalue_cids[fvalue].append(cid)
        line = file.readline()

    # print json.dumps(fvalue_cids, indent=4, sort_keys=True)

    # create adjacent matrix. convert fvalue_cids to adjacent matrix

    print "creating adjacent matrix"
    adjacent_matrix = {}

    # fvalue_cids = {
    #       "0": [
    #           "271316802", 
    #           "271540439", 
    #           "271529473", 
    #           "271440464", 
    #           "271520490", 
    #           "271323742", 
    #           "271082434", 
    #           "271297682", 
    #           "271488786", 
    #           "271293773", 
    #           "271501577", 
    #           "269206082"
    #       ], 
    #       "1": [
    #           "271288952", 
    #           "271259851", 
    #           "271192207", 
    #           "271265011", 
    #           "271251239", 
    #           "271224818", 
    #           "271251251", 
    #           "271223774", 
    #           "271155846", 
    #           "271155858"
    #       ]
    # }

    items = fvalue_cids.items()
    print len(items)

    sizes = [len(fvalue_cids[fvalue]) for fvalue in fvalue_cids]
    sizes.sort()
    print sizes


    count = 0

    for item in items:
        cids = item[1]
        for cid in cids:
            if cid not in adjacent_matrix:
                adjacent_matrix[cid] = {}
            for adj in cids:
                if adj == cid:
                    continue
                if adj not in adjacent_matrix[cid]:
                    adjacent_matrix[cid][adj] = 0
                adjacent_matrix[cid][adj] += 1

                count += 1
                if count % 100 == 0:
                    print "Process " , count

    return adjacent_matrix


def write_adjacent_matrix(adjacent_matrix, output):
    file = open(output, "w")

    for cid in adjacent_matrix:
        adjacents = adjacent_matrix[cid]
        file.write(str(cid))
        for adjacent in adjacents:
            file.write(' ' + str(adjacent) + ':' + str(adjacents[adjacent]))
        file.write('\n')

    file.close()


if __name__=="__main__":
    if (len(sys.argv) != 7):
        print "Error in input parameters"
        print "type %s <cids_file> <cid_aid1_file> <aid1_aid2_file> <features_file> <cms_file> <output>" % sys.argv[0]
        print "See example in get_matrix.sh"
        exit()

    cids_file = sys.argv[1]
    cid_aid1_file = sys.argv[2]
    aid1_aid2_file = sys.argv[3]
    features_file = sys.argv[4]
    cms_file = sys.argv[5]
    output = sys.argv[6]

    cids = read_cids(cids_file)
    # print json.dumps(cids, indent=4, sort_keys=True)
    print len(cids)

    aid1_cid = get_aid1_cid(cid_aid1_file, cids)
    # print json.dumps(aid1_cid, indent=4, sort_keys=True)
    print len(aid1_cid)

    aid2_cid = get_cid_aid2(aid1_aid2_file, aid1_cid)
    # print json.dumps(aid2_cid, indent=4, sort_keys=True)
    print len(aid2_cid)

    features = read_features(features_file)
    features = {
        # "GENRES" : 0,
        "COUNTRY": 0,
        # "CALLSIGN": 0,
        # "KEYWORDS": 0,
        # "TAGS": 0,
        # "TYPE": 0,
        # "SUMMARY": 0,
        # "YEAR": 0,
        # "PREMIERE_DATE": 0
    }
    # print json.dumps(features, indent=4, sort_keys=True)
    print len(features)

    adjacent_matrix = get_adjacent_matrix(aid2_cid, features, cms_file)

    write_adjacent_matrix(adjacent_matrix, output)
