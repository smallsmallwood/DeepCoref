#!/bin/bash

# manually set these
corpusPath="/Users/christanner/research/DeepCoref/data/ECB_SMALL/"
replacementsFile="/Users/christanner/research/DeepCoref/data/replacements.txt"
allTokens="/Users/christanner/research/DeepCoref/data/allTokens1.txt"
verbose="true"
stanfordPath="/Users/christanner/research/libraries/stanford-corenlp-full-2017-06-09"

# parses corpus and outputs a txt file, with 1 sentence per line, which is used for (1) creating embeddings; (2) stanfordCoreNLP to annotate
#python WriteSentencesToFile.py --corpusPath=${corpusPath} --replacementsFile=${replacementsFile} --outputFile=${allTokens} --verbose=${verbose}

# runs stanfordCoreNLP, which annotates our corpus
cd ${stanfordPath}
java -cp "*" -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse,dcoref -file ${allTokens} -tokenize.options untokenizable=noneKeep -parse.debug
