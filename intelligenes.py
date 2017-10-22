# Intelli-Genes: How many intelligence alleles do you have?
# by Jun Axup, Longevi.me (http://longevi.me)
#
# Based off Sniekers, et al. Nature Genetics 49, 1107–1112 (2017)
# https://www.nature.com/ng/journal/v49/n7/full/ng.3869.html
# Genome-wide association meta-analysis of 78,308 individuals identified 336 SNPs associated with intelligence.
#
# This script takes your 23andMe raw data and compares your genotype to those found in the paper.
# To get your 23andMe data, log in and go to Tools -> Browse Raw Data -> Download
# Script requires csv and pandas libraries
# Due to size of the 23andMe file, the script can take a few moments to execute. Please be patient.

# Edit file paths:

file_23andme = 'raw_data_from_23andme.txt' # Supply your own genome file here
file_intelgenes = 'intelligenes.csv'

# No edits needed below

# Imports intelligenes and prepares data set

import csv
import pandas as pd

with open(file_intelgenes, 'r') as f:
    inteldata = [i.split(",") for i in f.read().split()]

intelsnps = []
for i in inteldata:
    intelsnps.append(i[0])

intelsnps = set(intelsnps)

# Import 23andMe data and creates dictionary of your genotype

with open(file_23andme, 'r') as f:
    reader = csv.reader(f, delimiter="\t")
    rawdata = list(reader)

mygene = {}

for i in rawdata:
    if i[0][0] != "#":
        if i[0] in intelsnps and i[3] != '--':
            mygene[i[0]] = i[3]

# Merges the data sets

mydata = []
nodata = []

for j in inteldata:
    if j[0] in mygene:
        j.extend([mygene[j[0]], mygene[j[0]].count(j[1].capitalize())])
        mydata.append(j)
    else:
        nodata.append(j[0])

# Counts number of alleles

alcount = 0

for i in mydata:
    alcount += i[4]

# Prints chart and info

print "Intelli-Genes: How many intelligence alleles do you have?"
print "by Jun Axup, Longevi.me (http://longevi.me)"
print ""
print "Based off Sniekers, et al. Nature Genetics 49, 1107–1112 (2017)."
print "https://www.nature.com/ng/journal/v49/n7/full/ng.3869.html"
print "Genome-wide association meta-analysis of 78,308 individuals identified 336 SNPs associated with intelligence."
print ""
print "This script takes your 23andMe raw data and compares your genotype to those found in the paper."
print "Note: not all SNPs are weighted equally, not all SNPs in the paper are represented (only %s percent), it does not" % (len(mygene) * 100/ len(intelsnps))
print "account for heterozygous properties, and it’s still only GWAS correlations that aren’t necessarily causation."
print ""
print "number of intelligence SNPs sequenced by 23andMe: %s" % len(mygene)
print "number of SNPs not sequenced by 23andMe: %s" % (len(intelsnps) - len(mygene))
print ""
print "your number of intelligence alleles: %s" % alcount
print "your percent of intelligent alleles: %s" % (alcount * 100 / (2 * len(mydata)))
print ""
pd.DataFrame(mydata, columns=['SNP rsID', 'Intelligence Allele', 'Alternative Allele', 'Your Genotype', 'Your Intelligence Allele Count'])
