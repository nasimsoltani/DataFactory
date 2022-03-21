#!/bin/bash
# ----------------------------------------------------
python -u ./sigmf_converter.py \
--sigmf_path /home/nasim/UAVDataset/UAV-Sigmf-float16/ \
--mat_path /home/nasim/UAVDataset/UAV-mat-files/ \
--conversion sigmf2mat
