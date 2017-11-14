#!/bin/bash

# launch script create_adjacent_matrix with appropriate input parameters



CIDS_FILE="/home/andrew/MEGA/ARCCN_CDN/second_stage/user_log/analyze_user_log_backup_22_08_2017/dataset2/only_cids/dataset2_pid_5_only_cid.log"
CID_AID1_FILE="/home/andrew/MEGA/ARCCN_CDN/second_stage/user_log/cms_attribute_tables/1_content_info.txt"
AID1_AID2_FILE="/home/andrew/MEGA/ARCCN_CDN/second_stage/user_log/cms_attribute_tables/4_T_CMS_CONT_ACCE.txt"
FEATURES_FILE="/home/andrew/MEGA/ARCCN_CDN/second_stage/code/page_ranking/features_short_list.txt"
CMS_FILE="/home/andrew/ARCCN_CDN/cms_attribute_tables/6_T_CMS_CONTENT_EXT.txt"
RESULT_FILE="./page_rank_results.txt" 


python an_page_rank.py $CIDS_FILE $CID_AID1_FILE $AID1_AID2_FILE $FEATURES_FILE $CMS_FILE $RESULT_FILE

