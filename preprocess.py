import numpy as np
import csv
import sys
import math
import re


# ConceptNet
def preConceptNet():
    file = "E:\conceptnet\conceptnet-assertions-5.6.0.csv"
    with open(file, encoding='utf-8') as csv_file:
        data_raw = csv.reader(csv_file)
        # total number = 32755210
        dataset = []
        for row in data_raw:
            row = ''.join(row).split('\t')  # row is a list
            if re.match(r'/c/en/[a-zA-Z0-9_/]+\Z', row[2]) != None and re.match(r'/c/en/[a-zA-Z0-9_/]+\Z', row[3]) != None:
                weight = "".join(re.findall(r'"weight": \d+.\d+', row[4])).split(':')  # ['"weight"', ' 1.0']
                if( float(weight[1]) <= 3 ):
                    li = [row[1], row[2], row[3], float(weight[1])]
                    print(li)
                    dataset.append(li)
        print(len(dataset))
        # 3098816(only filter the '/c/en') from 0.1-22.891
        # 3054006(and '/c/en/[a-zA-Z0-9_/]+\Z') from 0.1-22.891
        # 3044163 and weight <= 3
        return dataset


# NELL
def preNELL():
    # print(sys.getdefaultencoding())
    decrement = True
    maxInt = sys.maxsize
    while decrement:
        # decrease the maxInt value by factor 10
        # as long as the OverflowError occurs.
        decrement = False
        try:
            csv.field_size_limit(maxInt)
        except OverflowError:
            maxInt = int(maxInt/10)
            decrement = True
    file = 'E:\_NELL\_NELL.csv'  # from 1.0 to 0.9000133499803894   avg. 0.9675292351354514
    with open(file, encoding='utf-8') as csv_file:
        data_raw = csv.reader(csv_file)
        header = "".join(next(data_raw)).split('\t')  # 读取第一行每一列的标题
        # header: ['Entity', 'Relation', 'Value', 'Iteration of Promotion', 'Probability', 'Source',
        # 'Entity literalStrings','Value literalStrings', 'Best Entity literalString', 'Best Value literalString',
        # 'Categories for Entity', 'Categories for Value', 'Candidate Source']
        dataset = []
        max_p = -1
        min_p = 100
        num = 0
        for row in data_raw:
            triple = "".join(row).split('\t')
            # Relation "generalizations" should be filter, because it belongs to the "Category".
            if triple[1] == 'generalizations' or math.isnan(float(triple[4])):
                continue
            else:
                li = [triple[0], triple[1], triple[2], float(triple[4])]
                if float(triple[4]) > max_p:
                    max_p = float(triple[4])
                if float(triple[4]) < min_p:
                    min_p = float(triple[4])
                num = num + float(triple[4])
                print(li)
                dataset.append(li)
        total = len(dataset)
        print(total)
        print(max_p)
        print(min_p)
        print(num)
        print(num / total)
        # 644208, from 1.0 to 0.9000133499803894   avg. 0.9675292351354514
        return dataset


def std_format(dataset):
    


if __name__ == "__main__":
    dataset = preNELL()
    std_format(dataset)
