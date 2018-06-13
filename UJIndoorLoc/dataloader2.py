#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/6/13 9:41
@author: Pete
@email: yuwp_1985@163.com
@file: dataloader2.py
@software: PyCharm Community Edition
"""
import numpy as np
import pandas as pd

part_heading_list = ['LONGITUDE','LATITUDE','FLOOR','BUILDINGID','SPACEID','RELATIVEPOSITION','USERID','PHONEID','TIMESTAMP']

def get_wap_heading():
    ap_heading_list = []
    for index in range(1,520 + 1):
        ap_id_str = "WAP%03d" % (index)
        ap_heading_list.append(ap_id_str)
    return ap_heading_list

def load_wifi_data(raw_wifi_file):
    ap_heading_list = get_wap_heading()
    heading_list = []
    heading_list.extend(ap_heading_list)
    heading_list.extend(part_heading_list)
    wifi_df = pd.read_csv(raw_wifi_file)
    wifi_dict = {} # {build_id: [features_array, labels_array, [coordinate1, coordinate2]]}
    for wifi_record in wifi_df.ix[:, heading_list].values:
        build_id = wifi_record[len(ap_heading_list) - 1 + 4]
        floor_id = wifi_record[len(ap_heading_list) - 1 + 3]
        space_id = wifi_record[len(ap_heading_list) - 1 + 5]
        wifi_info = wifi_record[0:len(ap_heading_list)].astype(float)
        space_label = int((build_id + 1) * 10000 + (floor_id + 1) * 1000 + space_id)
        coord_meter = (wifi_record[len(ap_heading_list) - 1 + 1], wifi_record[len(ap_heading_list) - 1 + 2])
        if wifi_dict.has_key(build_id):
            tempList = wifi_dict[build_id]
            tempList[0].append(wifi_info)
            tempList[1].append(space_label)
            tempList[2].append(coord_meter)
        else:
            wifi_dict[build_id] = [[wifi_info], [space_label], [coord_meter]]
    return wifi_dict


if __name__ == "__main__":
    train_wifi_dict = load_wifi_data("trainingData.csv")
    build_list = train_wifi_dict.keys()
    print build_list
    # Show the first wifi infomation for each building
    for build_id in build_list:
        wifi_info = train_wifi_dict.get(build_id)
        wifi_info_array = np.array(wifi_info[0])
        print len(wifi_info_array[0])
    print("Done.")