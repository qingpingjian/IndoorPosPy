#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/6/27 10:19
@author: Pete
@email: yuwp_1985@163.com
@file: freelocation.py
@software: PyCharm Community Edition
"""
import math
import numpy as np

from collections import Counter
from  dataloader2 import load_wifi_data

class FreeLoc(object):

    def __init__(self, delta_value = 10, w = 5, dist_threshold = 1.5, nNeighbours = 3):
        """
        Parameters for FreeLoc algorithm
        :param delta_value:  delta value to separete KEY from Value Vector
        :param w:  average of top w frequency values
        :param dist_threshold: the threshold of combining fingerprints
        """
        self.update_para(delta_value, w, dist_threshold, nNeighbours)
        return

    def update_para(self, delta_value, w, dist_threshold, nNeighbours):
        self.delta_value = delta_value
        self.w = w
        self.dist_threshold = dist_threshold
        self.nNeighbours = nNeighbours

    def is_same_location(self, coord1, coord2):
        euler_dist = math.sqrt((coord1[0]-coord2[0])**2 + (coord1[1]-coord2[1])**2)
        return euler_dist <= self.dist_threshold

    def prepocess(self, build_wifi_dict, combine_same=True):
        """
        Re-organize the Wi-Fi scan to one array for each location
        {build_id: [features_array, labels_array, [coordinate1, coordinate2, ...], phoneID_array]}
        {build_id: [labels_array, phoneID_array, [coordinate1, coordinate2, ...], [[feathers_array, ...], [feathers_array, ...]]]}
        :param build_wifi_dict: wifi scaned results in the above format
        :return: target format
        """
        wifi_fp_feature_array_dict = {}
        for build_id in build_wifi_dict.keys():
            wifi_info = build_wifi_dict.get(build_id)
            # Using the first wifi record to initialize the wifi_fp_info
            # label, phoneID, coordinate, rss values
            wifi_fp_info = [[wifi_info[1][0]], [wifi_info[3][0]], [wifi_info[2][0]], [ [wifi_info[0][0]] ] ]
            for i in range(1, len(wifi_info[0])):
                first_label = wifi_info[1][i]
                first_phone = wifi_info[3][i]
                first_coord = wifi_info[2][i]
                first_feature = wifi_info[0][i]
                combined_flag = False
                if combine_same:
                    for j in range(len(wifi_fp_info[0])):
                        second_label = wifi_fp_info[0][j]
                        second_phone = wifi_fp_info[1][j]
                        second_coord = wifi_fp_info[2][j]
                        # existing same location fp
                        if first_label == second_label and first_phone == second_phone and \
                                self.is_same_location(first_coord, second_coord):
                            wifi_fp_info[3][j].append(first_feature)
                            combined_flag = True
                            break
                if not combined_flag:
                    wifi_fp_info[0].append(first_label)
                    wifi_fp_info[1].append(first_phone)
                    wifi_fp_info[2].append(first_coord)
                    wifi_fp_info[3].append([ first_feature ])
            wifi_fp_feature_array_dict[build_id] = wifi_fp_info
        return wifi_fp_feature_array_dict

    def free_loc_process(self, fp_feature_array):
        # Peak Frequency Algorithm
        # array to dict
        fp_feature_dict = {}
        for wifi_rss_list in fp_feature_array:
            index = 0
            for wifi_rss in wifi_rss_list:
                index += 1
                if wifi_rss < 0:
                    ap_id_str = "WAP%03d" % (index)
                    if fp_feature_dict.has_key(ap_id_str):
                        fp_feature_dict[ap_id_str].append(wifi_rss)
                    else:
                        fp_feature_dict[ap_id_str] = [wifi_rss]
        #  frequency statistics
        # if the number of rss values is less than 5, then using the mean value
        # else using the mean values of top w frequency
        wifi_freq_dict = {}
        for ap_id, rss_list in fp_feature_dict.items():
            if len(rss_list) < 5:
                wifi_freq_dict[ap_id] = float(sum(rss_list)) / len(rss_list)
            else:
                rss_freq_list = Counter(rss_list).most_common(self.w)
                wifi_freq_dict[ap_id] = float(sum([rf[0] for rf in rss_freq_list])) / len(rss_freq_list)
        # Key AP and AP Value Vector (core algorithm)
        # Wi-Fi RSS sequence based on frequency descending order
        wifi_rss_list_based_freq = sorted(wifi_freq_dict.items(), key=lambda x:x[1], reverse=True)
        wifi_free_loc_dict = {}
        for i in range(len(wifi_rss_list_based_freq)):
            ap_mac = wifi_rss_list_based_freq[i][0]
            ap_rss = wifi_rss_list_based_freq[i][1]
            threshold_rss = ap_rss - self.delta_value
            tmp_mac_list = []
            for j in range(i+1, len(wifi_rss_list_based_freq)):
                if wifi_rss_list_based_freq[j][1] > threshold_rss:
                    continue
                tmp_mac_list.append(wifi_rss_list_based_freq[j][0])
            wifi_free_loc_dict[ap_mac] = set(tmp_mac_list)
        return wifi_free_loc_dict

    def free_loc_score(self, train_free_loc_dict, test_free_loc_dict):
        score = 0
        for test_ap_mac in test_free_loc_dict.keys():
            if train_free_loc_dict.has_key(test_ap_mac):
                train_value_set = train_free_loc_dict.get(test_ap_mac)
                test_value_set = test_free_loc_dict.get(test_ap_mac)
                score += len(train_value_set & test_value_set)
        return score

    def free_loc_alg(self, train_fp_info, test_fp_info):
        estimateList = []
        # fingerprint format:
        # [labels_array, phoneID_array, [coordinate1, coordinate2, ...], [[feathers_array, ...], [feathers_array, ...]]]
        for i in range(len(test_fp_info[0])):
            test_coord = test_fp_info[2][i]
            test_fp_feature_array = test_fp_info[3][i]
            test_free_loc_dict = self.free_loc_process(test_fp_feature_array)
            free_loc_score_list = []
            for j in range(len(train_fp_info[0])):
                train_coord = train_fp_info[2][j]
                train_fp_feature_array = train_fp_info[3][j]
                train_free_loc_dict = self.free_loc_process(train_fp_feature_array)
                free_loc_score_list.append((train_coord, self.free_loc_score(train_free_loc_dict, test_free_loc_dict)))
            free_loc_score_list.sort(key=lambda x:x[1], reverse=True)
            neigh_coord = [free_loc[0] for free_loc in free_loc_score_list[0:self.nNeighbours]]
            estimate_coord = np.mean(neigh_coord, axis=0)
            estimateList.append((test_coord[0], test_coord[1], estimate_coord[0], estimate_coord[1]))
        return estimateList

    def estimation(self, train_wifi_array_dict, test_wifi_array_dict):
        estimate_coord_list = []
        for build_id in test_wifi_array_dict.keys():
            train_fp_info = train_wifi_array_dict.get(build_id)
            test_fp_info = test_wifi_array_dict.get(build_id)
            estimate_coord_list.extend(self.free_loc_alg(train_fp_info, test_fp_info))
        return estimate_coord_list


if __name__ == "__main__":
    control_flag_array = (True, False)
    if control_flag_array[0]:
        user_fp_dict = {"13":[
            [[-50, -55, -67, -72, -88, -90, 100],
             [-65, -68, -74, -52, -91, -87, 100],
             [-65, -51, -53, -66, -82, -85, 100],
             [-92, -80, -67, -75, -58, -54, 100]],
            ["101", "101", "101", "102"],
            [(1,1), (1,1.5), (1.5,1), (3,3)],
            [1, 1, 1, 1]
        ]}
        usera_fp = [[-50, -55, -67, -72, -88, -90, 100]]
        userb_fp = [[-65, -68, -74, -52, -91, -87, 100]]
        userc_fp = [[-65, -51, -53, -66, -82, -85, 100]]
        userd_fp = [[-92, -80, -67, -75, -58, -54, 100]]
        first_free_loc = FreeLoc(delta_value=10)
        print first_free_loc.prepocess(user_fp_dict, combine_same=False)
        pass
    elif control_flag_array[1]:
        train_wifi_dict = load_wifi_data("trainingData.csv")
        test_wifi_dict = load_wifi_data("validationData.csv")
        second_free_loc = FreeLoc(delta_value=10, w=2, dist_threshold = 1.5, nNeighbours = 3)
        train_wifi_array_dict = second_free_loc.prepocess(train_wifi_dict,combine_same=True)
        test_wifi_array_dict = second_free_loc.prepocess(test_wifi_dict, combine_same=False)
        estimate_coord_list = second_free_loc.estimation(train_wifi_array_dict, test_wifi_array_dict)

        free_loc_error_list = [round(math.sqrt((coords[0] - coords[2]) ** 2 + (coords[1] - coords[3]) ** 2) * 1000) / 1000
                        for coords in estimate_coord_list]
        print np.mean(free_loc_error_list, axis=0)
    else:
        pass
    print("Done.")