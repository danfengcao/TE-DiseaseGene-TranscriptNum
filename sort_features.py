#!/usr/bin/python 
##-------------------------------------------------------------------------
## Description:sort features.
## firstly written by dfcao ## 2014/12/15 ##
##--------------------------------------------------------------------------

import os
import sys
import re

def substitute_space(f_name):
    print "substitute space into \\t..."
    f_in = open(f_name, "r")
    f_out = open(os.path.split(f_name)[1] + ".tmp", "w")
    
    re_ensembl_item = re.compile('^chr(?P<chr>\w+)\s+(?P<start>\d+)\s+(?P<end>\d+)\s+(?P<suffix>.*)')
    while True:
        l_now = f_in.readline()
        if len(l_now) == 0:
            break;
        m = re_ensembl_item.match(l_now)
        if m == None:
            continue
    
        chrom = m.group("chr")
        start = m.group("start")
        end = m.group("end")
        suffix = m.group("suffix")
        l_out = 'chr%s\t%s\t%s\t%s\n' % (chrom, start, end, suffix)
        f_out.write(l_out)

    f_out.close
    f_in.close
    
#----------------------------------------------------------------
# sort a gtf or bed format file by its first two feartures
# chromosome and start codon in this script
# f_name: input file to be processed
# nonsex_chrs: the number of nonsex chromosomes
def sort_features(f_name, nonsex_chrs, which_column):
    
    #substitute_space(f_name)
    
    print "sort annotation..."
    f_in = f_name
    f_out = os.path.split(f_name)[1] + ".sort"

    parts = ""
    chr_list = range(1, nonsex_chrs+1)
    chr_list.append('X')
    chr_list.append('Y')
    for i in chr_list:
        print "sorting chr%s..." % i
        tmp_file = "file" + str(hash(f_in + str(i)))
        os.system("grep -P 'chr%s\t' %s | sort -n -k %d  >%s" % (str(i), f_in, which_column, tmp_file))
        parts += (tmp_file + " ")
        
    os.system("cat " + parts + ">" + f_out)

    for i in chr_list:
        tmp_file = "file" + str(hash(f_in + str(i)))
        os.system("rm " + tmp_file)

    #os.system("rm " + f_in)
#---------------------------------------------------------------
# test
# if (len(sys.argv) < 2):
#     print "para error! need to use:\npython %s ensembl.gtf.tranNum\n" % sys.argv[0]
#     sys.exit()

# sort_features(sys.argv[1], 22, 2)
