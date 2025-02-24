#!/bin/bash
/home/ubuntu/miniforge3/condabin/conda activate videorag
#rm -rf videorag-workdir
#mkdir -p videorag-workdir
#python -u insert.py > videorag-workdir/insert.log
#python -u query.py > videorag-workdir/query.log

#python insert_param.py "Elderly-Fall.mp4"
#python insert_param.py "Multi-Ojbect.mp4"
python insert_param.py "LongStay.mp4"
python insert_param.py "SmashingCar.mp4"
python insert_param.py "StealChicken.mp4"

#python query.py "Elderly-Fall.mp4" "Please list all actions in the video along with their timestamps and descriptions."
#python query.py "Multi-Ojbect.mp4" "Please list all actions in the video along with their timestamps and descriptions."
python query.py "LongStay.mp4" "Please list all actions in the video along with their timestamps and descriptions."
python query.py "SmashingCar.mp4" "Please list all actions in the video along with their timestamps and descriptions."
python query.py "StealChicken.mp4" "Please list all actions in the video along with their timestamps and descriptions."