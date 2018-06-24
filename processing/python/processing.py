from fileUtil import fileUtil


# Input: original csv of routes
# Output: csv containing [src, tar, src_pos, tar_pos]
# Note

def filterRoute(origin_route_csv, filter_route_csv, airport_csv):
	route_data = fileUtil.csv_load(origin_route_csv)
	airport_data = fileUtil.csv_load(airport_csv)

	position_dict = {}            # airport_code: [lat, lng]
	route_list = []
	route_dict = {}      		  # (src+','+tar): weight
	data = []                     # result data: a list, [src, tar, src_pos, tar_pos, weight]

	for airport in airport_data:
		code = airport[4]
		lat = float(airport[6])
		lng = float(airport[7])
		position_dict[code] = [lat, lng]

	for route in route_data:
		src = route[16]
		tar = route[17]
		
		if ( (src+','+tar) in route_list ):
			route_dict[src+','+tar] += 1
		elif( (tar+','+src) in route_list ):
			route_dict[tar+','+src] += 1
		else:
			route_list.append(src+','+tar)
			route_dict[src+','+tar] = 1
		
	for r in route_dict:
		src = r.split(',')[0]
		tar = r.split(',')[1]
		try:
			src_pos = position_dict[src]
			tar_pos = position_dict[tar]
			data.append([src, tar, src_pos, tar_pos, route_dict[r]])
		except:
			print("ERROR: ", src, tar)
			continue

	# write data 
	fileUtil.csv_write(data, ['src', 'tar', 'src_pos', 'tar_pos', 'weight'], filter_route_csv)



# Input: airport csv file
# Output: airport geojson file
# Note:  1. normal order: [lat, lng]

def airportJSON(csv_file, json_file):
	airport_data = fileUtil.csv_load(csv_file)
	features = []
	json_data = { "type": "FeatureCollection", "features": features}

	for airport in airport_data:
		code = airport[4]
		lat = float(airport[6])
		lng = float(airport[7])

		feature = { "type": "Feature", "properties": {"code": code}, 
					"geometry": {
    			    	"type": "Point",
    					"coordinates": [lng, lat]    # order!!
  					}
				}
		features.append(feature)

	# write json
	fileUtil.json_write(json_data, json_file)



# Input:
# Output:
# Note:

def cLouvainConvert(cls, nodes_file, links_file):
	nodes = fileUtil.csv_load(nodes_file)     # list
	links = fileUtil.csv_load(links_file)     # list

	# node index mapping
	nodes_data = []           # [[node, index], [...], ...]
	nodes_index = {}          # {'node':index, ...}
	index = 0                 # index starts from 0
	for node in nodes: 
		nodes_index[node[0]] = index      # node[0]: because of how we write csv in fileUtil!!
		nodes_data.append([node[0], index])
		index += 1

	# link index mapping
	links_data = []        # [ [src_index, tar_index, value], [..],...]
	for link in links:
		value = int(link[2])    
		tmp_link = [nodes_index[link[0]], nodes_index[link[1]], value]
		links_data.append(tmp_link)

	# write to new file
	name = 'dblp_super'
	nodes_index_file = '../data/c_louvain/nodes/'+name+'.csv'
	links_index_file = '../data/c_louvain/links/'+name+'.csv'
	fileUtil.csv_write(nodes_data, ['id', 'index'], nodes_index_file)
	fileUtil.csv_write(links_data, ['source', 'target', 'value'], links_index_file)



# reformat the result of c++ Louvain method & conver node index back to 'node id'
# from 'node com_id' to {'0':[node0, node1, ...], '2':[...], ...}
def communityConvert(cls, communities_file, node_index_file):
	node_communities = fileUtil.txt_load(communities_file)    # node_index & community pairs
	node_indices = fileUtil.csv_load(node_index_file)     # node_id  &  node_index pairs

	communities = {}
	index_dict = {}      # {index: 'node_id'}

	for item in node_indices:
		node_id = item[0]
		index = item[1]
		index_dict[index] = node_id

	for item in node_communities:
		node_index = item.strip('\n').split(' ')[0]
		node_id = index_dict[node_index]
		com_id = item.strip('\n').split(' ')[1]
		if(com_id not in communities):
			communities[com_id] = [node_id]
		else:
			communities[com_id].append(node_id)

	return communities



if __name__ == '__main__':
	origin_route_csv = '/Users/WANGYunzhe/Documents/Data/Flight/origin/routes_2008.csv'
	filter_route_csv = '/Users/WANGYunzhe/Documents/Data/Flight/csv/routes2008.csv'

	csv_file = '/Users/WANGYunzhe/Documents/Data/Flight/csv/airports.csv'
	json_file = '/Users/WANGYunzhe/Documents/Data/Flight/geojson/airports.geojson'
	filterRoute(origin_route_csv, filter_route_csv, csv_file)
	# airportJSON(csv_file, json_file)
