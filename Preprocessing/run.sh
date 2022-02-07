#!/bin/bash
# ----------------------------------------------------------------------------------------------------
python -u ./preprocess.py \
--sigmf_address /home/nasim/Downloads/neu_m046p309d/UAV-Sigmf-float16/ \
--mat_address /home/nasim/Downloads/neu_m046p309d/mat_files/ \
--pkl_path /home/nasim/Downloads/neu_m046p309d/pkls_new/ \
--symbolic_class_name 'uav' \
--num_classes 7 \
--distance_list '6ft,9ft,12ft,15ft' \
--symbolic_transmitter_sigmf_key 'UAV' \
