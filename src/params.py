import argparse

def setWriteSentencesToFileParams():
	parser = argparse.ArgumentParser()
	parser.add_argument("--corpusPath", help="the corpus dir")
	parser.add_argument("--replacementsFile", help="we replace all instances of these tokens which appear in our corpus -- this is to help standardize the format, useful for creating embeddings and running stanfordCoreNLP")
	parser.add_argument("--outputFile", help="where we will output the file of corpus' tokens")
	parser.add_argument("--stitchMentions", help="treat multi-token mentions as 1 word token", type=str2bool, nargs='?', default="f")
	parser.add_argument("--verbose", help="print a lot of debugging info", type=str2bool, nargs='?', default="f")
	return parser.parse_args()

def setAlignWithStanfordParams():
	parser = argparse.ArgumentParser()
	parser.add_argument("--corpusPath", help="the corpus dir")
	parser.add_argument("--replacementsFile", help="we replace all instances of these tokens which appear in our corpus -- this is to help standardize the format, useful for creating embeddings and running stanfordCoreNLP")
	parser.add_argument("--stanfordFile", help="the file that stanfordCoreNLP output'ed")
	parser.add_argument("--stitchMentions", help="treat multi-token mentions as 1 word token", type=str2bool, nargs='?', default="f")
	parser.add_argument("--verbose", help="print a lot of debugging info", type=str2bool, nargs='?', default="f")
	return parser.parse_args()	

# allows for handling boolean params
def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')