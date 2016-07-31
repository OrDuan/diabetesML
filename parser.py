import csv
from datetime import datetime

from os.path import isfile, join

import os

DATE_INDEX = 0
TIME_INDEX = 1
ACTIVITY_INDEX = 2
GLUCOSE_INDEX = 3


def parse_file(file_name):
    data_dict = {
        'name': file_name,
        'data': [],
    }
    with open('datasets/' + file_name, 'r') as fp:
        for line in fp.readlines():
            file_data = line.split()
            date = '{} {}'.format(file_data[DATE_INDEX], file_data[TIME_INDEX])
            date = datetime.strptime(date, '%m-%d-%Y %H:%M')
            activity = file_data[ACTIVITY_INDEX]
            try:
                glucose = file_data[GLUCOSE_INDEX]
            except:
                pass
            data_dict['data'].append({
                'date': date,
                'activity': activity,
                'glucose': glucose,
            })
    return data_dict


def save_all_to_csv(data_list):
    for data_dict in data_list:
        save_to_csv(data_dict)


def save_to_csv(data_dict):
    with open('datasets/parsed/' + data_dict['name'] + '.csv', 'w+') as fp:
        writer = csv.DictWriter(fp, ['date', 'activity', 'glucose'])
        writer.writeheader()
        for data in data_dict['data']:
            writer.writerow(data)


def parse_all():
    files = os.listdir('datasets/')
    data_list = []
    for f in files:
        if not isfile(join('datasets/', f)):
            continue
        data_list.append(parse_file(f))

    save_all_to_csv(data_list)

if __name__ == '__main__':
    parse_all()
