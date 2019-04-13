#!/usr/bin/env bash

corpus=${1}
corpus_train="train_${corpus}"
corpus_test="test_${corpus}"

printf "corpus:%s\n" ${corpus}
printf "train corpus:%s\n" ${corpus_train}
printf "test corpus:%s\n" ${corpus_test}

shuf ${corpus} | split -l $[ $(wc -l ${corpus} | cut -d" " -f1) * 80 / 100 ]
mv xaa ${corpus_train}
mv xab ${corpus_test}


#############################
corpus=${2}
corpus_train="train_${corpus}"
corpus_test="test_${corpus}"
printf "corpus:%s\n" ${corpus}
printf "train corpus:%s\n" ${corpus_train}
printf "test corpus:%s\n" ${corpus_test}

shuf ${corpus} | split -l $[ $(wc -l ${corpus} | cut -d" " -f1) * 80 / 100 ]
mv xaa ${corpus_train}
mv xab ${corpus_test}

wc -l *.*
