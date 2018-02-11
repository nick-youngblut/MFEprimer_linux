[![Build Status](https://travis-ci.org/nick-youngblut/MFEprimer_linux.svg?branch=master)](https://travis-ci.org/nick-youngblut/MFEprimer_linux)

# MFEprimer-2.1 linux

A fast thermodynamics-based program for checking PCR primer specificity 

> NOTE: This software has been edited in order to make it installable on Linux64 via setup.py

The original software can be found at https://github.com/quwubin/MFEprimer


## Introduction

Evaluating the specificity of PCR primers is an essential step in PCR primer design. The MFEprimer-2.1 server allows users to check primer specificity against genomic DNA and mRNA/cDNA sequence databases quickly and easily. MFEprimer-2.1 uses a k-mer index algorithm to accelerate the search process for primer binding sites and uses thermodynamics to evaluate binding stability between each primer and its DNA template. Several important characteristics such as the sequence, melting temperature and size of each amplicon, either specific or non-specific, are reported on the results page. Based on these characteristics and the user-friendly output, users can readily draw conclusions about the specificity of PCR primers. Analyses for degenerate primers and multiple PCR primers are also supported in MFEprimer-2.1. In addition, the databases supported by MFEprimer-2.1 are comprehensive, and custom databases can also be supported on request. The MFEprimer-2.1 server does not require a login and is freely available at http://biocompute.bmi.ac.cn/CZlab/MFEprimer-2.1. 


## Installation

### System requirement

  * System: Linux 
  * Python (>= 2.7) or PyPy (http://pypy.org/). 
  * psutil (>= 3.0.0): download from here (https://github.com/giampaolo/psutil)

### Installation 

  * clone the repo from GitHub
  * `python setup.py install`

### Testing

  * Get to the test directory 
    * `cd MFEprimer/test/`
  *  Index the database, it will create three files with suffix: .2bit .uni and .sqlite3.db.
    * `../IndexDb.sh test.rna`
  *  Run MFEprimer and you will get the results if not errors found.
    *  `../MFEprimer.py -i p.fa -d test.rna`   
  * Done. Good Luck.



## More about "index"
   
Unlike MFEprimer 1.x versions, which use BLAST for primer binding sites search, MFEprimer-2.1 uses the k-mer index algorithm to speed up the primer binding sites search process. This is the speed problem I have to solve, while, the other question force me **MUST** to replace the BLAST. It's the "ACCURACY" problem. As we know that, BLAST is a famous program to find the homology sequence from a database by sequence similarity. However, the annealing process of primer and its target sequence is thermodynamics. They bind to each other just because they are stable in thermodynamics, not because they are matched in base pairs. For example, the mismatch "G-G" contributes as much as the Gibbs free energy of -2.2 kcal/mol to the duplex stability _[SantaLucia 2.14]_. So the first step we have to do is to find all the possible binding sites with the k-mer index algorithm], and then to evaluate the binding stability using the Nearest-Neighbor model. 

Someone may think that what if let BLAST do the first step (find all the possible binding sites)? Actually, MFEprimer 1.x version uses this strategy. But we found that BLAST may lose many less significant hits. The reasons are 1)BLAST only reports the significant hits in statistically; 2) the BLAST output was controlled by "-E" and other options. Even we carefully handled these options, we still found many less significant hits were missed.

So, what is the "k-mer index algorithm"? And why this algorithm can't miss possible binding sites? Because MFEprimer-2.1 pre-stored all the positions of all k-mers. I will explain in details.

First of all, I have to explain the "k-mer". A “k-mer" is defined as a short DNA sequence with a length of k nucleotides. For example, "AAATTTCCC" is a mer with k=9.

The “index process” is to store all the positions of all k-mers which appears in all the sequences from a FASTA format database. We use the following Python-like seudo-code and Fig. 2 to illustrate the index process. For advanced users, they may look at our [Python code](https://github.com/quwubin/MFEprimer/blob/master/chilli/mfe_index_db.py) for details.

```
mer_pos_hash = {}
k = 9
for seq in fasta_db:
    mer_pos_hash[seq.id] = {}
    for i in range(seq.length - k):
        mer = seq[ i : i+k ]
        pos = i + k
        if mer not in mer_pos_hash[seq.id]:
            mer_pos_hash[seq.id][mer] = []

        mer_pos_hash[seq.id][mer].append( pos)
```

![Index algorithm](https://github.com/quwubin/image/raw/master/MFEprimer/IndexAlgorithm.png)
> Fig. 2 The k-mer index process in MFEprimer-2.1. Here k = 9 and the green lines show the mers.

We store the positions in SQLite3 database. The database schema is very simple. There are three fields:
  1. mer_id [Integer, Primary key]: the mer id. We don’t store the raw mer string into the database. Instead, we convert the mer string into a unique integers and store this unique integer as the mer_id.
  2. plus [text]: seq_id_1:pos_1,pos_2,pos_3,…,pos_n;seq_id_2:pos_1,pos_2…
  3. minus [text]: Same like plus but the sequence is the reverse complement sequence of the plus strand.

According to these explanations, we expect the users know why the k-mer index algorithm is more accurate than BLAST.

## MFEprimer 1.x vs. MFEprimer-2.1 (Running speed comparison)

We did a benchmark test to compare the running speed of MFEprimer 1.x and MFEprimer-2.1.

### Parameters

Here are the machine parameters:

  * System: Linux 2.6.18-194.el5xen #1 SMP x86_64 GNU/Linux
  * CPU: Intel(R) Xeon(R) CPU E5430  @ 2.66GHz  # For all the experiments, only one CPU or one processor was used
  * Memory: 16 GB

Here are the program running parameters:

  * MFEprimer 1.x: -W 9, -e 10000, -B 2.10, -b 1000 -s 0.3
  * MFEprimer-2.1: -k 9, --size_stop=2.10, --size_start=100, --ppc=30

### Datasets

Here are the data sets with size:

  * _C. elegans_: mRNA (24377 sequences, 37 M), Genome (7 sequences, 97 M bases)
  * Chiken: mRNA (19839 sequences, 41 M bases), Genome (32 sequences, 997 M bases)
  * Human: mRNA (46150 sequences, 125 M bases), Genome (25 sequences, 3134 M bases)

The primers are obtained from [_C. elegans_ RNAi library](http://cmgm.stanford.edu/~kimlab/primers.12-22-99.html). We used the 1 pair, 2 pairs, ... 30 pairs of primers for test.

The running time (in seconds) in Table 1 was counted by Linux command "/usr/bin/time" with option "-f '%e" to count only the elapsed time by the program.

### Results

From Table 1, we can see that for mRNA databases, which have thousands of short sequences (compared with the chromosome sequences), MFEprimer-2.1 have absolutely advantages. Even for 30 pair of primers, MFEprimer-2.1 takes less 10 seconds to finish the work. While for genome databases, which have fewer but large chromosome sequences, the running time increases when the number of primer pair increases. When using 20 pair of primers, it takes about 10 minutes. But for one pair of primers, which is the most normal case, MFEprimer-2.1 can finish the job within 1 seconds. So in the "single mode", MFEprimer-2.1 can quickly (usually less than 10 seconds) return the results for the tasks of one or two pair of primers. But for batch primers with large genome database, it's better to use the "batch mode" to examine the specificity of the PCR primers. 

In general, **the size of database sequence** and the **number of primers** have significant effect on the performance of MFEprimer-2.1. 

### Discussion

Obviously, MFEprimer 1.x has to run BLAST program for searching the whole database every time, however MFEprimer-2.1 only retrieves the position data from the SQL database. So as expected, MFEprimer-2.1 wins in almost every way. It seems that MFEprimer-2.1 lost in the aspects indicated by the yellow region. However, that's because MFEprimer-1.x missed many less significantly hits as I described in the previous section. 


![Benchmark result data](https://github.com/quwubin/image/raw/master/MFEprimer/benchmark_data.png)
> Table 1 Benchmark result data. MFEprimer-2.1 wins in almost every way. It seems that MFEprimer-2.1 lost in the aspects indicated by the yellow region. However, that's because MFEprimer-1.x missed many less significantly hits as I described in the previous section. 

## Bug tracker

Have a bug? Please create an issue here on GitHub!

https://github.com/quwubin/MFEprimer/issues


## Getting help

Email to Wubin Qu (quwubin@gmail.com) or Nick Youngblut (nyoungb2@gmail.com)

## Citation

>Wubin Qu, Yang Zhou, Yanchun Zhang, Yiming Lu, Xiaolei Wang, Dongsheng Zhao, Yi Yang and Chenggang Zhang\*. MFEprimer-2.1: A fast thermodynamics-based program for checking PCR primer specificity. **_Nucleic Acids Res_**. 2012 (accepted).

>Wubin Qu, Zhiyong Shen, Dongsheng Zhao, Yi Yang and Chenggang Zhang. (2.19) 
MFEprimer: multiple factor evaluation of the specificity of PCR primers, 
**_Bioinformatics_**, 25(2), 276-278.

## Authors

**Wubin Qu**

+ http://quwubin.sinaapp.com
+ http://github.com/quwubin

**Chenggang Zhang**

+ zhangcg@bmi.ac.cn

**Nick Youngblut**

* Just updated the software for easy install in Linux via setup.py

## Copyright and license

Copyright (c) 2.08-2012. Wubin Qu (quwubin@gmail.com) and 
Chenggang Zhang (zhangcg@bmi.ac.cn, zcgweb@gmail.com), Beijing Institute of Radiation Medicine.

MFEprimer (all the versions) source and executables are freely available for academic, 
nonprofit and personal use. Commercial licensing information please contact 
Dr. Chenggang Zhang (zhangcg@bmi.ac.cn, zcgweb@gmail.com).

MFEprimer source may be downloaded from "https://github.com/quwubin/MFEprimer".
