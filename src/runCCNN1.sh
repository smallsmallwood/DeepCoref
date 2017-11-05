#!/bin/bash
cd /home/christanner/researchcode/DeepCoref/src/
numLayers=(2) # 1 3
numEpochs=(15) # 5 10 20
windowSize=(0) # 1 2 3
numNeg=(7) # 5 10 15
batchSize=(256) # 64 128
shuffle=(f) # t                                                                                            
embSize=(400) # 50                                                                                    
dropout=(0.4) # 0.0 0.1 .2 .3 .5
hddcrp="predict"
clusterMethod=("avgavg") # "min" "avg" 
source ~/researchcode/DeepCoref/venv/bin/activate
# source ~/researchcode/DeepCoref/oldcpu/bin/activate
# source /data/people/christanner/tfcpu/bin/activate

# CPU runs	 
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
									# qsub -pe smp 8 -l vlong -o cpuGOLD_nl${nl}_ne${ne}_ws${ws}_neg${neg}_bs${bs}_s${s}_e${emb}_dr${dr}_cm${cm}.out runCCNN2.sh FULL cpu ${nl} ${ne} ${ws} ${neg} ${bs} ${s} ${emb} ${hddcrp} ${dr} ${cm}
									a=1
								done
							done
						done
					done
				done
			done
		done
	done
done

# GPU runs
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
									qsub -l gpus=1 -o gpuGOLD_nl${nl}_ne${ne}_ws${ws}_neg${neg}_bs${bs}_s${s}_e${emb}_dr${dr}_cm${cm}.out runCCNN2.sh FULL gpu ${nl} ${ne} ${ws} ${neg} ${bs} ${s} ${emb} ${hddcrp} ${dr} ${cm}
								done
							done
						done
					done
				done
			done
		done
	done
done
