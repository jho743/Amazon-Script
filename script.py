# Amazon Tool
import sys

"""
	Reads the file into list, separated by line
"""
def read_file(file_name):
	with open(file_name, 'r') as f:
		content = f.read()
		content_list = content.splitlines()
		f.close()
	return content_list

"""
	Returns a dictionary with appropriate values
"""
def parse_data(contents):
	lst = []
	for i in range(1, len(contents)):
		line = contents[i]
		if line[0] == '"':
			line = line[1:]
		if line[-1] == '"':
			line = line[:-1]
		line = line.split('","')

		d = dict()
		d['tracking_id'] = line[0]
		d['route_code'] = line[1]
		d['station_code'] = line[2]
		d['dsp_name'] = line[3]
		d['da_name'] = line[4]
		d['reason_code'] = line[5]
		d['status_code'] = line[6]
		d['route_sort_code'] = line[7]
		d['time_stamp'] = line[8]
		d['sort_zone'] = line[9]
		d['amount'] = line[10]
		d['commercial'] = line[11]

		lst.append(d)
	return lst


"""
	Given a dsp name, return the data values that contain the dsp name
"""
def data_for_dsp(data_dict, dsp_name):
	lst = []
	for data in data_dict:
		if data['dsp_name'] == dsp_name:
			lst.append(data)
	return lst

"""
	Return a dictionary with driver as key and a list of data as value
	Returns the grand total
"""
def organize_by_driver(dsp_data):
	d = dict()
	grand_total = 0
	for item in dsp_data:
		dsp_name = (item['route_code'] + " / " if item['route_code'] else "") + item['da_name'].split('/')[0]
		if dsp_name not in d:
			d[dsp_name] = [item]
		else:
			d[dsp_name].append(item)
	return d

"""
	TESTING: Display the data nicely
"""
def display_data(dsp_data, dsp_name):
	grand_total = 0
	print(f'		***  {dsp_name} Commercials ***\n\n')
	for da_name in dsp_data:
		lst = dsp_data[da_name]
		print(f'- {da_name}')
		for item in lst:
			grand_total += 1
			print(f'	- {item["tracking_id"]} / {item["sort_zone"]}' + \
				(f" / {item['route_sort_code']}" if item['route_sort_code'] else ""))
	print(f'\nGrand Total: {grand_total}')
	print('\n')

"""
	Display the data nicely
"""
def write_data(dsp_datas, dsp_names):
	f = open("output.doc", "w")
	for i in range(len(dsp_datas)):
		grand_total = 0
		f.write(f'		***  {dsp_names[i]} Commercials ***\n\n\n')
		for da_name in dsp_datas[i]:
			lst = dsp_datas[i][da_name]
			f.write(f'- {da_name}\n')
			for item in lst:
				grand_total += 1
				f.write(f'	- {item["tracking_id"]} / {item["sort_zone"]}' + \
					(f" / {item['route_sort_code']}\n" if item['route_sort_code'] else "\n"))
		f.write(f'\nGrand Total: {grand_total}\n')
		f.write('\n\n')
	print('Note: The data has been written to output.doc\n')

def main(argv):
	if len(argv) > 2:
		print('\n!!! You have given more than 1 argument to this script !!!\n')
		print('Example: python script.py data.csv\n')
		return -1
	if len(argv) < 2:
		print('\n!!! You will need to provide the file name as an argument to this script !!!\n')
		print('Example: python script.py data.csv\n')
		return -1

	file_name = argv[1]
	try:
		lines = read_file(file_name)
	except Exception as e:
		print(f'{file_name} does NOT exist in the same directory')
		return -1
	
	data_dict = parse_data(lines)

	alal = organize_by_driver(data_for_dsp(data_dict, 'ALAL'))
	noah = organize_by_driver(data_for_dsp(data_dict, 'NOAH'))
	opls = organize_by_driver(data_for_dsp(data_dict, 'OPLS'))

	display_data(alal, 'ALAL')
	display_data(noah, 'NOAH')
	display_data(opls, 'OPLS')

	write_data([alal, noah, opls], ['ALAL', 'NOAH', 'OPLS'])
	return 0

if __name__ == "__main__":
	main(sys.argv)
	
