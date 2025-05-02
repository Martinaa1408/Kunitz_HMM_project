#!/usr/bin/bash
import sys
import math
def get_cm(filename,threshold,pe,pr=1): #get the confusion matrix
    cm=[[0,0],[0,0]]
    f=open(filename)
    for line in f:
        v=line.rstrip().split() #for each one of the rows i do the confusion matrix. I should specify the position of the e value and of the real in variable pe position e value, and pr in position of real value. 
        evalue=float(v[pe])
        r=int(v[pr]) #one means kunitz, while 0 means no kunitz. So i want to transform evalue into a prediction but how? Based on a threshold, whatever will be aboce the threshold what is below is kunitz class one and whatever is above is no kunitz.
        if evalue<=threshold:
            p=1
        else:
            p=0
        #cosi hai due coordinate, quello della predizione e del real value se corrispondono allora hai veri positivi e veri negativi, se non corrispondono allora falsi positivi e falsi negativi. Con questi valori riempi la confusion matrix!!!
        cm[p][r]=cm[p][r]+1 #in this way i update line by line my confusion matrix checking if the e value is above or below the threshold. 
    return cm

def get_q2(cm): #get accuracy function
    #true positive and true negative divided by all the prediction
    n=float(cm[0][0]+cm[0][1]+cm[1][0]+cm[1][1])
    return (cm[0][0]+cm[1][1])/n

def get_mcc(cm): #you have a denominator that contains all the combination
    d=math.sqrt((cm[0][0]+cm[1][0])*(cm[0][0]+cm[0][1])*(cm[1][1]+cm[1][0])*(cm[1][1]+cm[0][1]))
    return (cm[0][0]*cm[1][1]-cm[0][1]*cm[1][0])/d

def get_tpr(cm): #true positive rate
    return float(cm[1][1])/(cm[1][0]+cm[1][1])


def get_ppv(cm): #predicted value. We have to divide the true positive by false positive plus true positive, so all positive. Positive predicted values
    return float(cm[1][1])/(cm[1][1]+cm[0][1])

def full_seq_computing(filename,th):
    cm=get_cm(filename,th,2)
    #FOR THE FULL SEQ
    print("USING E-VALUE OF THE FULL SEQUENCE")
    q2=get_q2(cm)
    print('tn=',cm[0][0],'fn=', cm[0][1]) #ti dice i falsi negativi e veri negativi
    print('fp=',cm[1][0],'tp=', cm[1][1]) #ti dice i falsi positivi e i veri positivi
    # # print('q2=',q2) #i can have a good paccuracy but bad prediction, this because depeneds from balance of the classes. A prediction of the most abundant will give and influence the overall of accuracy. There is so another measure performance that can be used and is matthew correlation coefficient. One of the other parameter that we can consider
    mcc=get_mcc(cm)
    # print('mcc=',mcc)
    tpr=get_tpr(cm)
    ppv=get_ppv(cm)
    print('threshold=',th,'q2=',q2,"MCC=",mcc,"tpr=",tpr,'ppv=',ppv,"fullseq=", True)
    return

def single_domain_computing(filename,th):
    cm=get_cm(filename,th,3)
    #FOR THE BEST SINGLE DOMAIN
    print("USING E-VALUE OF THE BEST DOMAIN")
    q2=get_q2(cm)
    print('tn=',cm[0][0],'fn=', cm[0][1]) #ti dice i falsi negativi e veri negativi
    print('fp=',cm[1][0],'tp=', cm[1][1]) #ti dice i falsi positivi e i veri positivi
    # # print('q2=',q2) #i can have a good paccuracy but bad prediction, this because depeneds from balance of the classes. A prediction of the most abundant will give and influence the overall of accuracy. There is so another measure performance that can be used and is matthew correlation coefficient. One of the other parameter that we can consider
    mcc=get_mcc(cm)
    # print('mcc=',mcc)
    tpr=get_tpr(cm)
    ppv=get_ppv(cm)
    print('threshold=',th,'q2=',q2,"MCC=",mcc,"tpr=",tpr,'ppv=',ppv,"fullseq=", False)
    return

if __name__=='__main__':
    filename=sys.argv[1]
    th=float(sys.argv[2])
    if len(sys.argv)>3:
        selection=int(sys.argv[3]) #questo fa capire al performance.py se calcolare le performance fullseq(1) o best single domain (2) o entrambe (3)
    else:
        selection=0 #se non definito significa che è 0 e deve farli entrambi
    if selection==0: #questo indica di eseguire le performance sia con il fullseq che con il best single domain e-values utilizzando la stessa threshold th (utile quando la threshold è la stessa)
        full_seq_computing(filename,th)
        print('\n')
        single_domain_computing(filename,th)
    elif selection==1:#questo indica di eseguire le performance solo per la fullseq e-values utilizzando la threshold th (è utile quando stai vacendo la valutazione con la migliore threshold individuata per gli e-values fullseqs)
        full_seq_computing(filename,th)
    else:#questo indica di eseguire le performance solo per la single domain e-values utilizzando la threshold th (è utile quando stai vacendo la valutazione con la migliore threshold individuata per gli e-values single domain)
        single_domain_computing(filename,th)


