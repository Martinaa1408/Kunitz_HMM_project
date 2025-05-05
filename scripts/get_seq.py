#!/usr/bin/python
import sys
def get_ids(idlist):
    f=open(idlist)
    return f.read().strip().split('\n')

def get_seq(pidlist,seqfile):
    f=open(seqfile)
    s=0
    for line in f:
        #now the fasta file looks >name and below the sequence. So i should define one way to define a sort of state variable that can be 0 or 1. If it is 0 dont do anything, anyway do something. 
        if line.startswith('>'):
            pid=line.split('|')[1] #now you have to check if the identifier, the accession number.
            s=0 #state variable
            if pid in pidlist: s=1 #so if the accession number (id) is in the fasta file i set state equal to 1
        if s==1: print(line.strip())
#before using the file we need to do some cleaning because swissprot has the full list of identifier and we want select according to the second column 
            


if __name__=='__main__':
    idlist=sys.argv[1] #lista di ids da tenere
    seqfile=sys.argv[2] #fasta file da cui estrarre le sequenze indicate nel idlist.txt
    pidlist=get_ids(idlist)#.read().strip().split('\t')
    get_seq(pidlist,seqfile)
