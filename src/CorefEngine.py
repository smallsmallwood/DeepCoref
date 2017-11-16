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
		hddcrp_parsed = HDDCRPParser(args.hddcrpFullFile) # loads HDDCRP's pred or gold mentions file

		# parses the real, actual corpus (ECB's XML files)
		corpus = ECBParser(args)
		helper = ECBHelper(args, corpus)

		helper.createSemanticSpaceSimVectors(hddcrp_parsed) # just uses args and corpus

		# loads stanford's parsed version of our corpus and aligns it w/
		# our representation -- so we can use their features
		stan = StanParser(args, corpus) 
		helper.addStanfordAnnotations(stan)

		'''
		for t in corpus.corpusTokens:
			# our current 1 ECB Token possibly maps to multiple StanTokens, so let's
			# ignore the StanTokens that are ‘’ `` POS $, if possible (they may be our only ones)
			pos = ""
			posOfLongestToken = ""
			longestToken = ""
			for stanToken in t.stanTokens:
				if stanToken.pos in helper.badPOS:
					# only use the badPOS if no others have been set
					if pos == "":
					    pos = stanToken.pos
				else: # save the longest, nonBad POS tag
					if len(stanToken.text) > len(longestToken):
						longestToken = stanToken.text
						posOfLongestToken = stanToken.pos 

			if posOfLongestToken != "":
				pos = posOfLongestToken
			if pos == "":
				print("* ERROR: our POS empty!")
				exit(1)
			else:
				print(str(t),"=>",str(pos))
		exit(1)
		'''
		# trains and tests the pairwise-predictions via Conjoined-CNN
		corefEngine = CCNN(args, corpus, helper, hddcrp_parsed)
		(pairs, predictions) = corefEngine.run()

		# performs agg. clustering on our predicted, testset of HMentions
		stoppingPoints = [0.15,0.17,0.19,0.21,0.23,0.26,0.28,0.301,0.32,0.34,0.37,0.39,0.401,0.41,0.42,0.43,0.44,0.45,0.46,0.47,0.48,0.49,0.501,0.51,0.52,0.53,0.55,0.57,0.601]
		for sp in stoppingPoints:
			predictedClusters = corefEngine.clusterHPredictions(pairs, predictions, sp)
			print("* using a agg. threshold cutoff of",str(sp),",we returned # clusters:",str(len(predictedClusters.keys())))
			corefEngine.writeCoNLLFile(predictedClusters, sp)
		print("* done writing all CoNLL file(s); now run ./scorer.pl to evaluate our predictions")






