def get_directory(): 
    with open('directory_path.txt', 'r') as f:
        first_line = f.readline()
        return first_line