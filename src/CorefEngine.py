import sys  
import params
import os.path
from ECBParser import *
from ECBHelper import *
from HDDCRPParser import *
from StanParser import *
from CCNN import *
from get_coref_metrics import *

# parses the corpus and runs Coref Resoultion on the mentions
class CorefEngine:
	if __name__ == "__main__":

		# handles passed-in args
		args = params.setCorefEngineParams()

		# figures out which mentions (HMentions) HDDCRP thinks exist
		hddcrp_parsed = HDDCRPParser(args.hddcrpFile) # loads HDDCRP's pred or gold mentions file

		# parses the real, actual corpus (ECB's XML files)
		corpus = ECBParser(args)
		helper = ECBHelper(args, corpus)

		# loads stanford's parsed version of our corpus and aligns it w/
		# our representation -- so we can use their features
		stan = StanParser(args, corpus) 
		helper.addStanfordAnnotations(stan)

		# trains and tests the pairwise-predictions via Conjoined-CNN
		corefEngine = CCNN(args, corpus, helper, hddcrp_parsed)
		(pairs, predictions) = corefEngine.run()

		# performs agg. clustering on our predicted, testset of HMentions
		stoppingPoints = [0.49] #[0.49,0.501,0.51,0.52,0.53,0.54,0.55,0.56,0.57,0.58,0.59,0.601]
		for sp in stoppingPoints:
			predictedClusters = corefEngine.clusterHPredictions(pairs, predictions, sp)
			print("* using a agg. threshold cutoff of",str(sp),",we returned # clusters:",str(len(predictedClusters.keys())))
			corefEngine.writeCoNLLFile(predictedClusters, sp)
		print("* done writing all CoNLL file(s); now run ./scorer.pl to evaluate our predictions")






