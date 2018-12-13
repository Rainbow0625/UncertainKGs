import numpy as np
import csv
import sys
import math
import re


# ConceptNet
def preConceptNet():
    file = "E:\conceptnet\conceptnet-assertions-5.6.0.csv"
    dataset = []  # store the string
    fact_list = []  # store the index
    ent_dic = {}
    rel_dic = {}
    max_p = -1
    min_p = 100
    num = 0
    with open(file, encoding='utf-8') as csv_file:
        data_raw = csv.reader(csv_file)
        # original total number = 32755210
        for row in data_raw:
            triple = ''.join(row).split('\t')  # row is a list
            if re.match(r'/c/en/[a-zA-Z0-9_/]+\Z', triple[2]) != None and\
                    re.match(r'/c/en/[a-zA-Z0-9_/]+\Z', triple[3]) != None:
                weight = "".join(re.findall(r'"weight": \d+.\d+', triple[4])).split(':')  # ['"weight"', ' 1.0']
                if( float(weight[1]) <= 3 ):
                    rel = triple[1]
                    head = triple[2]
                    tail = triple[3]
                    score = float(weight[1])

                    # statistic the score
                    if score > max_p:
                        max_p = score
                    if score < min_p:
                        min_p = score
                    num = num + score

                    # get the dataset
                    li = [head, tail, rel, score]
                    # print(li)
                    dataset.append(li)

                    # get the dataset
                    li = [head, tail, rel, score]
                    # print(li)
                    dataset.append(li)

                    # get relation, entity and fact
                    if rel not in rel_dic.keys():
                        rel_dic[rel] = len(rel_dic)
                    r = rel_dic[rel]
                    if head not in ent_dic.keys():
                        ent_dic[head] = len(ent_dic)
                    e1 = ent_dic[head]
                    if tail not in ent_dic.keys():
                        ent_dic[tail] = len(ent_dic)
                    e2 = ent_dic[tail]
                    li2 = [e1, e2, r, score]
                    print(li2)
                    fact_list.append(li2)
        total = len(dataset)
        print(total)
        # 3098816(only filter the '/c/en') from 0.1-22.891
        # 3054006(and '/c/en/[a-zA-Z0-9_/]+\Z') from 0.1-22.891
        # 3044163 and weight <= 3

        # save in the file
        f = open('./Conceptnet/relation2id.txt', 'w')
        f.write(str(len(rel_dic)) + "\n")
        for key_name in rel_dic.keys():
            f.write(str(key_name) + "\t" + str(rel_dic[key_name]) + "\n")

        f = open('./Conceptnet/entity2id.txt', 'w')
        f.write(str(len(ent_dic)) + "\n")
        for key_name in ent_dic.keys():
            f.write(str(key_name) + "\t" + str(ent_dic[key_name]) + "\n")

        f = open('./Conceptnet/Fact.txt', 'w')
        f.write(str(len(fact_list)) + "\n")
        for line in fact_list:
            f.write(str(line[0]) + " " + str(line[1]) + " " + str(line[2]) + "\n")
        f.close()

        return dataset, fact_list, rel_dic, ent_dic


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
    file = 'E:/_NELLbig/_NELL.csv'
    dataset = []  # store the string
    fact_list = []  # store the index
    ent_dic = {}
    rel_dic = {}
    max_p = -1
    min_p = 100
    num = 0
    with open(file, encoding='utf-8') as csv_file:
        data_raw = csv.reader(csv_file)
        header = "".join(next(data_raw)).split('\t')  # 读取第一行每一列的标题
        # header: ['Entity', 'Relation', 'Value', 'Iteration of Promotion', 'Probability', 'Source',
        # 'Entity literalStrings','Value literalStrings', 'Best Entity literalString', 'Best Value literalString',
        # 'Categories for Entity', 'Categories for Value', 'Candidate Source']

        for row in data_raw:
            triple = "".join(row).split('\t')

            # it will be several scores in different iteration.
            score_list = triple[4].strip('[').strip(']').split(' ')
            max_s = -1.0
            for item in score_list:
                if float(item) > max_s:
                    max_s = float(item)

            # Relation "generalizations" should be filter, because it belongs to the "Category".
            if triple[1] == 'generalizations' or math.isnan(max_s):
                continue
            else:
                rel = triple[1]
                head = triple[0]
                tail = triple[2]
                score = max_s

                # statistic the score
                if score > max_p:
                    max_p = score
                if score < min_p:
                    min_p = score
                num = num + score

                # get the dataset
                li = [head, tail, rel, score]
                # print(li)
                dataset.append(li)

                # get relation, entity and fact
                if rel not in rel_dic.keys():
                    rel_dic[rel] = len(rel_dic)
                r = rel_dic[rel]
                if head not in ent_dic.keys():
                    ent_dic[head] = len(ent_dic)
                e1 = ent_dic[head]
                if tail not in ent_dic.keys():
                    ent_dic[tail] = len(ent_dic)
                e2 = ent_dic[tail]
                li2 = [e1, e2, r, score]
                print(li2)
                fact_list.append(li2)

        total = len(dataset)
        print(total)
        # print(max_p)
        # print(min_p)
        # print(num)
        # print(num / total)
        # 644208, from 1.0 to 0.9000133499803894   avg. 0.9675292351354514

        # save in the file
        f = open('./NELL/relation2id.txt', 'w')
        f.write(str(len(rel_dic)) + "\n")
        for key_name in rel_dic.keys():
            f.write(str(key_name) + "\t" + str(rel_dic[key_name]) + "\n")

        f = open('./NELL/entity2id.txt', 'w')
        f.write(str(len(ent_dic)) + "\n")
        for key_name in ent_dic.keys():
            f.write(str(key_name) + "\t" + str(ent_dic[key_name]) + "\n")

        f = open('./NELL/Fact.txt', 'w')
        f.write(str(len(fact_list)) + "\n")
        for line in fact_list:
            f.write(str(line[0]) + " " + str(line[1]) + " " + str(line[2]) + "\n")
        f.close()

        return dataset, fact_list, rel_dic, ent_dic


def std_format(dataset):
    pass


if __name__ == "__main__":
    dataset, fact_list, rel_dic, ent_dic = preNELL()
    # dataset, fact_list, rel_dic, ent_dic = preConceptNet()
