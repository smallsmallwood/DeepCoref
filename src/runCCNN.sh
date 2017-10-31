#!/bin/bash
cd /home/christanner/researchcode/DeepCoref/src/
numLayers=(1) # 2 3) 
numEpochs=(2) # 3 10 20)
windowSize=(1) # 2 3 5)
numNeg=(1) # 3 5 10)
batchSize=(64) # 128 256)
shuffle=(f) # t)
embSize=(400) # 50
dropout=(0.0) # 0.2 0.3 0.4)
hddcrp="predict"
clusterMethod=("min") # "avg" "avgavg")
source ~/researchcode/DeepCoref/venv/bin/activate
# source ~/researchcode/DeepCoref/oldcpu/bin/activate
# source /data/people/christanner/tfcpu/bin/activate

			    # qsub -pe smp 32 -l vlong -o cpu32b_nl${nl}_ne${ne}_ws${ws}_neg${neg}_bs${bs}_s${s}.out runCoref.sh cpu ${nl} ${ne} ${ws} ${neg} ${bs} ${s} ${emb}
for nl in "${numLayers[@]}"
do
	for ne in "${numEpochs[@]}"
	do
		for ws in "${windowSize[@]}"
		do
			for neg in "${numNeg[@]}"
			do
				for bs in "${batchSize[@]}"
				do
					for s in "${shuffle[@]}"
					do
						for emb in "${embSize[@]}"
						do
							for dr in "${dropout[@]}"
							do
								for cm in "${clusterMethod[@]}"
								do
									qsub -pe smp 8 -l vlong -o cpuGOLD_nl${nl}_ne${ne}_ws${ws}_neg${neg}_bs${bs}_s${s}_e${emb}_dr${dr}_cm${cm}.out runCoref.sh FULL gpu ${nl} ${ne} ${ws} ${neg} ${bs} ${s} ${emb} ${hddcrp} ${dr} ${cm}
								done
							done
						done
					done
				done
			done
		done
	done
done
# exit 1
# GPU
for nl in "${numLayers[@]}"
do
	for ne in "${numEpochs[@]}"
	do
		for ws in "${windowSize[@]}"
		do
			for neg in "${numNeg[@]}"
			do
				for bs in "${batchSize[@]}"
				do
					for s in "${shuffle[@]}"
					do
						for emb in "${embSize[@]}"
						do
							for dr in "${dropout[@]}"
							do
								for cm in "${clusterMethod[@]}"
								do
									qsub -l gpus=1 -o gpuGOLD_nl${nl}_ne${ne}_ws${ws}_neg${neg}_bs${bs}_s${s}_e${emb}_dr${dr}_cm${cm}.out runCoref.sh FULL gpu ${nl} ${ne} ${ws} ${neg} ${bs} ${s} ${emb} ${hddcrp} ${dr} ${cm}
								done
							done
						done
					done
				done
			done
		done
	done
done

