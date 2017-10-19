import sys  
import params
from ECBParser import *
from ECBHelper import *
from SiameseCNN import *
from get_coref_metrics import *
# parses the corpus and runs Coref Resoultion on the mentions
class CorefEngine:
	if __name__ == "__main__":

		# handles passed-in args
		args = params.setCorefEngineParams()

		# toy example to test PYTHON approach
		'''
		g = {1:set(['a','b','c']), 2:set(['d','e','f','g'])}
		r = {1:set(['a','b']), 2:set(['d','c']), 3:set(['f','g','h','i'])}
		print(get_conll_scores(g, r))
		exit(1)
		'''

		'''
		# 
		# [A: 1 of 1] create HDDCRP .key file based on the following .response file
		hddcrpFile="/Users/christanner/research/DeepCoref/results/test_hddcrp_wd.response"
		hddcrpOut="/Users/christanner/research/DeepCoref/results/test_hddcrp_wd.keys"
		f = open(hddcrpFile, 'r')
		hddcrpDMs = set()
		f.readline()
		for line in f:
			line = line.rstrip()
			if line == "#end document (t);":
				break
			_, tmp, clusterID = line.rstrip().split()
			(doc_id,m_id) = tmp.split(";")
			dm = (doc_id,int(m_id))
			hddcrpDMs.add(dm)
		f.close()
		print("we have ",str(len(hddcrpDMs)), " DMs in HDDCRP's WD response")
		# parses corpus
		corpus = ECBParser(args)
		
		ref_id = 0
		DocREFToUniqueNum = {}
		for dm in hddcrpDMs:

			ref = corpus.dmToREF[dm]
			print("dm:",str(dm), "has ref:",str(ref))
			(doc_id,m_id) = dm
			if (doc_id,ref) not in DocREFToUniqueNum.keys():
				DocREFToUniqueNum[(doc_id,ref)] = ref_id
				ref_id += 1
			else:
				print("we already have",str(doc_id),str(ref)," in the map")
		print("the response had ", str(len(DocREFToUniqueNum.keys())), " unique REFs")

		# makes the .key file for the .response
		f = open(hddcrpFile, 'r')
		g = open(hddcrpOut, 'w')
		g.write("#begin document (t);\n")
		f.readline()
		for line in f:
			line = line.rstrip()
			if line == "#end document (t);":
				break
			_, tmp, clusterID = line.rstrip().split()
			(doc_id,m_id) = tmp.split(";")
			dm = (doc_id,int(m_id))
			ref = corpus.dmToREF[dm]
			ref_id = DocREFToUniqueNum[(doc_id,ref)]
			g.write(str(_) + "\t" + str(tmp) + "\t(" + str(ref_id) + ")\n")
		g.write("#end document (t);")
		f.close()
		g.close()
		exit(1)
		# end of A
		'''

		# [B] evaluates HDDCRP

		'''
		B1:
		corpus = ECBParser(args)
		helper = ECBHelper(corpus, args)
		
		# constructs golden clusters from entire corpus
		goldenClusters = defaultdict(set)
		goldenClusterID = 0
		goldenDMs = set()
		for dirNum in corpus.dirToDocs.keys():
			if dirNum not in helper.testingDirs:
				continue
			for doc_id in corpus.dirToDocs[dirNum]:
				for i in range(len(corpus.docToREFs[doc_id])):
					tmp = set()
					curREF = corpus.docToREFs[doc_id][i]
					for dm in corpus.docREFsToDMs[(doc_id,curREF)]:
					    tmp.add(dm)
					    goldenDMs.add(dm)
					goldenClusters[goldenClusterID] = tmp
					goldenClusterID += 1
		print("# golden clusters:",str(len(goldenClusters.keys())))

		#hddcrpFile="/home/christanner/researchcode/DeepCoref/results/test_hddcrp_wd.response"
		hddcrpFile="/Users/christanner/research/DeepCoref/results/test_hddcrp_wd.response"
		f = open(hddcrpFile, 'r')
		f.readline()
		hddcrpDMs = set()
		hddcrpClusters = defaultdict(set)

		ref_id = 0
		DocREFToUniqueNum = {}
		for line in f:
			line = line.rstrip()
			if line == "#end document (t);":
				break
			_, tmp, clusterID = line.rstrip().split()
			(doc_id,m_id) = tmp.split(";")
			dm = (doc_id,int(m_id))
			hddcrpDMs.add(dm)
			c_id = int(clusterID[1:-1])
			hddcrpClusters[c_id].add(dm)


			ref = corpus.dmToREF[dm]
			if (doc_id,ref) not in DocREFToUniqueNum.keys():
				DocREFToUniqueNum[(doc_id,ref)] = ref_id
				ref_id += 1
		f.close()

		missingFromHDDCRP = set()
		for i in goldenDMs:
			if i not in hddcrpDMs:
				missingFromHDDCRP.add(i)

		missingFromGolden = set()
		for i in hddcrpDMs:
			if i not in goldenDMs:
				missingFromGolden.add(i)
		print("# goldenDMs:",str(len(goldenDMs)))
		print("# dms in hddcrp's:", str(len(hddcrpDMs)))
		print("# missing from hddcrp:", str(len(missingFromHDDCRP)))
		print("# missing from golden:", str(len(missingFromGolden)))
		print("missing from golden:",str(missingFromGolden))
		print("missing from hddcrp:",str(missingFromHDDCRP))

		#print(DocREFToUniqueNum.keys())
		print("# dms in hddcrp's:", str(len(hddcrpDMs)))
		print("the response had ", str(len(DocREFToUniqueNum.keys())), " unique REFs")
		#print("hddcrp clusters:",str(hddcrpClusters))
		print("# hddcrp clusters:",str(len(hddcrpClusters.keys())))
		print("# golden clusters:",str(len(goldenClusters.keys())))
		print(get_conll_scores(goldenClusters, hddcrpClusters))
		'''
		
		# gets HDDCRP's DMs
		hddcrpFile="/home/christanner/researchcode/DeepCoref/results/test_hddcrp_wd.response"
		#hddcrpFile="/Users/christanner/research/DeepCoref/results/test_hddcrp_wd.response"
		f = open(hddcrpFile, 'r')
		f.readline()
		hddcrpDMs = set()
		for line in f:
			line = line.rstrip()
			if line == "#end document (t);":
				break
			_, tmp, clusterID = line.rstrip().split()
			(doc_id,m_id) = tmp.split(";")
			dm = (doc_id,int(m_id))
			hddcrpDMs.add(dm)
		print("# hddcrp dms:",str(len(hddcrpDMs)))

		# parses corpus
		corpus = ECBParser(args)

		# constructs helper class
		helper = ECBHelper(corpus, args)
		helper.setValidDMs(hddcrpDMs)
		#response = helper.constructCoNLLClustersFromFile("/Users/christanner/research/DeepCoref/results/test_hddcrp2.response")
		#print(str(len(response)))
		#helper.constructCoNLLTestFileCD("/Users/christanner/research/DeepCoref/results/test_cd.keys")
		#helper.constructCoNLLTestFileWD("/Users/christanner/research/DeepCoref/results/test_wd.keys")

		# trains and tests the pairwise-predictions
		corefEngine = SiameseCNN(args, corpus, helper)
		(pairs, predictions) = corefEngine.run()

		stoppingPoints = [0.68]
		f1s = []
		for sp in stoppingPoints:
			(predictedClusters, goldenClusters) = corefEngine.clusterPredictions(pairs, predictions, sp)
			f1s.append(get_conll_f1(goldenClusters, predictedClusters))
		print(f1s)
			'''
			goldenDMs = set()
			missingFromHDDCRP = set()
			for _ in goldenClusters.keys():
				for i in goldenClusters[_]:
					goldenDMs.add(i)
					if i not in hddcrpDMs:
						missingFromHDDCRP.add(i)

			missingFromGolden = set()
			for i in hddcrpDMs:
				if i not in goldenDMs:
					missingFromGolden.add(i)
			print("# goldenDMs:",str(len(goldenDMs)))
			print("# dms in hddcrp's:", str(len(hddcrpDMs)))
			print("# missing from hddcrp:", str(len(missingFromHDDCRP)))
			print("# missing from golden:", str(len(missingFromGolden)))
			print("hddcrp's perf:", str(get_conll_f1(goldenClusters, hddcrpClusters)))
			exit(1)
		for i in zip(stoppingPoints,f1s):
			print(i)
		'''


