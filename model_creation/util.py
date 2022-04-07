#coding=utf-8

import csv
import datetime
import os




class util():
    def csvRead(csvPath):
        csvFile = csv.reader(open(csvPath, 'r', encoding="utf8"))
        return csvFile


    def csvReadDetail(csvPath):
        try:
            csvFile = csv.reader(open(csvPath, 'r'))
        except Exception as e:
            print("Error: %s,\t,%s" % (Exception, e))
            print("There may be some problem in %s" % csvPath)
            return ""
        dataList = []
        for csvLine in csvFile:
            dataList.append(csvLine)
        return dataList


    def csvWrite(csvPath):
        csvFile = open(csvPath, 'w', encoding='utf8', newline='')
        writer = csv.writer(csvFile)
        return writer

    def csvInit():
        csv.field_size_limit(1000000000)
        return 0

    def datetime_toString(dt):
        return dt.strftime("%Y-%m-%d-%H")

    def mkdir(path):

        isExists = os.path.exists(path)

        if not isExists:
            os.makedirs(path)

            print
            path + ' Created successfully'
            return True
        else:
            print
            path + ' directory already exists'
            return False

