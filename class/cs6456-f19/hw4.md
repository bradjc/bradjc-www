---
permalink: "/class/cs6456-f19/hw4.html"
layout: single
title:  "CS6456 - HW4"
sidebar:
  nav: "cs6456hw4"
---

<style>
.masthead {
  display: none;
}
</style>



# HW4: Kernels Leveraging Machine Learning

Operating systems are complex pieces of software that must correctly manage many
resources, while supporting and effectively isolating other processes running on
the hardware, and ultimately provide a useful environment for users of the
system. With machine learning demonstrating impressive results for difficult
pattern-recognition tasks, it is useful to wonder if data-driven ML techniques
will be integrated into future operating system kernels. The paper ["Learned
Operating Systems"](https://cseweb.ucsd.edu/~yiying/LearnedOS-OSR19.pdf)
overviews several OS functions that might benefit from ML techniques in the
future.

In this homework we will look at one particular task a kernel may employ machine
learning for: detecting malicious software based on the system calls the
software uses. This level of insight, a per-process ordered list of syscalls, is
very straightforward for the kernel to obtain since it is involved in every
syscall. With the history of system calls, the kernel can then try to classify
each process as malicious or benign, and handle it accordingly.

## General Approach

For this homework we will use a labeled dataset containing numerous syscall
traces of both benign software and malware. Your job will be to train a
classifier with most of the traces from the dataset, and then test that
classifier on the remaining data. You should be able to predict if the process
that created the trace was malware or not with "better than guessing" accuracy.

## Dataset

The dataset is here: [api_calls_2019-11-04.zip](hw/api_calls_2019-11-04.zip).

The description of the dataset from the
[paper](https://www.techrxiv.org/articles/Behavioral_Malware_Detection_Using_Deep_Graph_Convolutional_Neural_Networks/10043099/1):

> We introduced a new public domain dataset of 42,797 malware API call sequences
> and 1,079 goodware API call sequences each [30]. Our motivation was twofold.
> On the one hand, we were motivated by the lack of public domain PE dynamic
> malware analysis dataset for training and evaluating our models. On the other
> hand, we were motivated by the desire to provide an open dataset that the
> research community could further utilize and extend. Malware samples were
> collected from VirusShare [31], and goodware samples were collected from both
> portablepps.com [32] and a 32-bit Windows 7 Ultimate directory. Both online
> download and local goodware were included to increase the variability of the
> dataset and decrease its imbalance. In order to gather the API call sequences
> from each sample, we chose Cuckoo Sandbox, which is a largely used,
> open-source automated malware analysis system capable of monitoring processes
> behavior while running in an isolated environment. Once the data was
> collected, three additional post-processing steps were performed. 1) Similar
> to [13], it was considered the first 100 non-consecutive repeated API calls to
> avoid tracking loops. 2) Since in malware detection tasks, it is prominent to
> recognize malicious patterns as early as possible, the sequences were
> extracted from the parent process only. 3) We built the list of unique API
> calls, considering all the samples, and then converted each API call name into
> a unique integer identifier equal to the index of the API call name in the
> list. As a result, 307 distinct API calls were identified. We produced a
> dataset where the first column contains the MD5 hash of the sample. The next
> 100 columns contain ordinal categorical values between 0 and 306, representing
> the API call sequence of the sample. The last column contains the label of the
> sample, 0 for goodware, and 1 for malware.

## Implementation

You are free to implement a classifier any way you see fit. A reasonable choice
would be to load the dataset in to TensorFlow and use TensorFlow's built-in
utilities to train and then execute a model. You do not need to create any new
ML techniques (but you can if you want!).

When you submit your solution you should specify some way to run your code. An
easy way to do this would be to include a `run.sh` bash script that just has a
single command that executes your code.

## Output

Your solution should create two text files:

1. `classification.txt`: This file should contain one line per test in the
   testing set. Each line should contain the hash value of the tested executable
   (from the dataset), then whitespace, then your estimated classification (1 if
   malware, 0 if benign), then whitespace, then the ground truth classification.
   For example:

	    4263f5e24054d855a1ddbc4c466e9389	1	1
		db475a7574aafc82fa8ca0bd5574e97d	1	1
		d6ce1725dafbed5408b9bcde0bf0bdc6	1	1
		342193744dd5786ae3f8e4643b6b70bb	1	1
		8f1fb93eaa4fe360a64c3ab7e1d0c06c	0	1

2. `results.txt`: This file should contain certain high-level results from your
solution, including: F1 score, precision, recall, and accuracy. For example:

        F1 score     .73
        Precision    .85
        Recall       .82
        Accuracy     .88

	This
	[document](https://towardsdatascience.com/accuracy-precision-recall-or-f1-331fb37c5cb9)
	contains a good overview of the metrics.

## Submission

You should zip or tar your code and copies of the two output files and then
upload it on collab.
