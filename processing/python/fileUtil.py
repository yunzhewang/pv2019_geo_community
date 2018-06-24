# a list of commonly used file-processing related functions
import csv
import json

class fileUtil:
	"""  initialize by giving the file name  """
	def __init__(self, filename):
		self.filename = filename


	###################        Load    Data     #######################

	"""  if the file is txt, or other format  """
	"""  return data in lines  """
	@classmethod
	def txt_load(cls, filename):
		file = open(filename, 'rb') 
		lines = file.readlines()
		return lines

		#############    customize    ###########
		# revisions = []
		# for i in range(0, 187386946):       # 187386946 is number of all lines: by 'wc -l'
		# 	line = file.readline()
		# 	isRevision = 'REVISION' in line
		# 	print ("line: ", i)

		# 	if isRevision:
		# 		revisions.append(line)

		# print('the number of revisions: ', len(revisions))
		# return revisions
		#############    customize    ###########




	"""  if the file is CSV format (with header)  """
	"""  return data in list  """
	@classmethod
	def csv_load(cls, filename):
		with open(filename, 'r') as fr:
			print('Loading data...')
			reader = csv.reader(fr)
			reader.next()
			data = list(reader)
			return data



	###################        Load    Data     #######################




	###################        Write    Data     #######################
	"""  line_list:   each element is a line (in string)     """
	@classmethod
	def txt_write(cls, line_list, filename):
		with open(filename, 'a') as out_file:
			for line in line_list:
				out_file.write(line)

	"""  header:   list, i.e., ['src', 'tar', 'value']    """
	@classmethod
	def csv_write(cls, list_data, header, filename):
		with open(filename, 'w') as fw:
			writer = csv.writer(fw)
			writer.writerow(header)
			for item in list_data:
				writer.writerow(item)


	@classmethod
	def json_write(cls, json_data, filename):
		with open(filename, 'w') as fw:
			json.dump(json_data, fw)

	###################        Write    Data     #######################
			
		