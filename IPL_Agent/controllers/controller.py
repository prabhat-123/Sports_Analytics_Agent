import csv

def read_csv_file(file_path: str):
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            ## removing empty attributes from each row
            row = {key:val for key, val in row.items() if val!=''}
            data.append(row)
        return data

