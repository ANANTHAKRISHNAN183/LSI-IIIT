
import numpy as np
from math import sqrt
import operator as op

def ncr(n, r):
    # for clculating ncr
    r = min(r, n-r)
    if r == 0: return 1
    numer = reduce(op.mul, xrange(n, n-r, -1))
    denom = reduce(op.mul, xrange(1, r+1))
    return numer//denom

def main():

    '''Find the Mx,My,Mrx,Mry Values from the shape file and store solve them for A_F values
        and find the list of A_F values.
    '''
    Mx = [120,300,300,120,-120,-300,-300,-120]
    My = [300,120,-120,-300,-300,-120,120,300]
    Mrx = [12,30,30,12,-12,-30,-30,-12]
    Mry = [30,12,-12,-30,-30,-12,12,30]
    length=len(Mx)
    count = 0
    val=ncr(length, 3)
    A = [[[0 for u in range(3)] for v in range(2)] for w in range(val)]
    for i in range(val):
        for j in range(i + 1, length):
            for k in range(j + 1, length):
                equation1 = np.array([[Mx[i], My[i], 1], [Mx[j], My[j], 1], [Mx[k], My[k], 1]])
                constant1 = np.array([Mrx[i], Mrx[j], Mrx[k]])
                x = np.linalg.solve(equation1, constant1)


                equation2 = np.array([[Mx[i], My[i], 1], [Mx[j], My[j], 1], [Mx[k], My[k], 1]])
                constant2 = np.array([Mry[i], Mry[j], Mry[k]])
                y = np.linalg.solve(equation2, constant2)
                p = 0
                for q in range(3):
                    A[count][p][q] = x[q]
                p = 1
                for q in range(3):
                    A[count][p][q] = y[q]
                count = count + 1
    #A_F values are stored in 3D array
    flg1, flg2, error=List_MxMy_formedfromA_F_AvgERMS(Mx,My,count,A,Mrx,Mry,length)
    return Mx,My,Mrx,Mry,flg1,flg2,error


def List_MxMy_formedfromA_F_AvgERMS(Mx, My, count, A,Mrx,Mry,length):
    ''' find the Rms and AvgRms values using the above Obtained A_F values'''
    EMx = [[0 for v in range(length)]for w in range(count)]
    EMy = [[0 for v in range(length)]for w in range(count)]
    ERMS =[[0 for v in range(length)]for w in range(count)]
    ERMSAvg = [0 for w in range(count)]
    sum = 0
    for s in range(count):
        sum = 0
        for p in range(length):
            q = 0
            EMx[s][p] = A[s][q][0] * Mx[p] + A[s][q][1] * My[p] + A[s][q][2]
            q = 1
            EMy[s][p] = A[s][q][0] * Mx[p] + A[s][q][1] * My[p] + A[s][q][2]
            ERMS[s][p] = sqrt((EMx[s][p] * EMx[s][p]) + (EMy[s][p] * EMy[s][p]))

        for t in range(length):
            sum = sum + ERMS[s][t]
        Avg = sum /length
        ERMSAvg[s] = Avg
    flg1, flg2, error=Find_bestA_F(ERMSAvg, count, ERMS, EMx, EMy, Mrx, Mry,length)
    return flg1, flg2, error

def Find_bestA_F(ERMSAvg, count, ERMS, EMx, EMy,Mrx,Mry,length):
    ''' After finding the ERMS and ERMSAvg now we can calculate the minimum error and say that the
     minimum ERMSAvg would be the best A_F values and store the index of that location for accessing
     '''
    min_error = ERMSAvg[0]
    flag = 1
    for i in range(count):
        if (ERMSAvg[i] < min_error):
            min_error = ERMSAvg[i]
            flag = i
    flg1, flg2, error=find_error(flag, Mrx, Mry, EMx, EMy, count, ERMS,length)
    return flg1,flg2,error

def find_error(flag, Mrx, Mry, EMx, EMy,count,ERMS,length):
    #now find out the error between the new values(EMx[flag]) and the old reference values(Mrx)
    error_x = [0 for v in range(length)]
    error_y = [0 for v in range(length)]
    for i in range(length):
        error_x[i] = EMx[flag][i] - Mrx[i]
        error_y[i] = EMy[flag][i] - Mry[i]
    print "error in x is ",error_x
    print "error in y is ",error_y
    flg1,flg2,error=rms_error(error_x, error_y,length)
    return flg1,flg2,error


def rms_error(error_x, error_y,length):
    #now find the rms error
    error = [0 for v in range(length)]
    for i in range(length):
        error[i] = sqrt((error_x[i] * error_x[i]) + (error_y[i] * error_y[i]))
    print "error is ",error
    flg1,flg2=Find_error_points(error,length)
    return flg1,flg2,error

def Find_error_points(error,length):
    #find out the error points that have to be eliminated from the list
    max1 = 0
    max2 = 0
    flg1 = 0
    flg2 = 0
    for i in range(1,length):
        if (error[i] > max1):
            max1 = error[i]
            flg1 = i
    for i in range(1, length):
        if (error[i] > max2) and (i != flg1):
            max2 = error[i]
            flg2 = i
    print flg1,flg2
    return flg1, flg2


if __name__ == '__main__':
    Mx, My, Mrx, Mry, flg1, flg2, error = main()