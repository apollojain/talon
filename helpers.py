
def get_directory(): 
    with open('directory_path.txt', 'r') as f:
        first_line = f.readline()
        return first_line

def formatted_index_dict_list(dictionary):
    def individual_helper(value, i):
        return value[i][1].encode("utf-8")
    formatted_list = []
    file_dict = dictionary['Files']
    for key in file_dict: 
        value = file_dict[key]
        json = {}
        json['key'] = key
        for i in range(5):
            j = i + 1
            json['label' + str(i + 1)] = individual_helper(value, i)
        formatted_list.append(json)
    return formatted_list

