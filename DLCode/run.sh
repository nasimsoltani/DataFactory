#!/bin/bash
# ----------------------------------------------------------------------------------------------------
python -u /home/nasim/DataFactory/DLCode/top.py \
--exp_name $1 \
--partition_path /home/nasim/dataset/indoor/ \
--stats_path /home/nasim/dataset/indoor/ \
--save_path /home/nasim/results/ \
--model_flag alexnet \
--contin false \
--json_path /home/nasim/results/cnn1/model_file.json \
--hdf5_path '' \
--slice_size 256 \
--num_classes 7 \
--batch_size 256 \
--id_gpu $2 \
--normalize true \
--train true \
--test true \
--epochs 100 \
--early_stopping true \
--patience 5 \
> /home/nasim/results/$1/log.out \
2> /home/nasim/results/$1/log.err
