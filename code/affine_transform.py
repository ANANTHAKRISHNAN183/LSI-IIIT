
import numpy as np
from math import sqrt
import operator as op
import csv_file
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
    Mx = [120,300,300,120,-120,-300,-300,-120]
    My = [300,120,-120,-300,-300,-120,120,300]
    Mrx = [12,30,30,12,-12,-30,-30,-12]
    Mry = [30,12,-12,-30,-30,-12,12,30]

    #coordinates from the shapefile of my_polygon and other_polygon
    Mx=[-0.5096,-0.2453,0.0591,0.3319,0.3504,0.1289,-0.2178,-0.4906]
    My=[0.4664,0.6144,0.6187,0.3966,0.0435,-0.2102,-0.2123,0.09216]
    Mrx=[-1.4803,-1.3629,-1.0987,-0.6693,-0.3691,-0.3154,-0.6366,-1.0811]
    Mry=[-0.0122,0.3634,0.6267,-0.6619,0.4104,0.0525,-0.3451,-0.2571]'''
    Mx,My,Mrx,Mry=csv_file.main()
    print Mx,My,Mrx,Mry
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
    flg1, flg2,error,NewMx,NewMy=List_MxMy_formedfromA_F_AvgERMS(Mx,My,count,A,Mrx,Mry,length)
    return Mx,My,Mrx,Mry,flg1,flg2,error


def List_MxMy_formedfromA_F_AvgERMS(Mx, My, count, A,Mrx,Mry,length):
    ''' find the Rms and AvgRms values using the above Obtained A_F values'''
    NewMx=[[0 for v in range(length)]for w in range(count)]
    NewMy=[[0 for v in range(length)]for w in range(count)]
    ErrorMx = [[0 for v in range(length)]for w in range(count)]
    ErrorMy = [[0 for v in range(length)]for w in range(count)]
    ERMS =[[0 for v in range(length)]for w in range(count)]
    ERMSAvg = [0 for w in range(count)]
    sum = 0
    for s in range(count):
        sum = 0
        for p in range(length):
            q = 0
            NewMx[s][p] = A[s][q][0] * Mx[p] + A[s][q][1] * My[p] + A[s][q][2]
            ErrorMx[s][p]=NewMx[s][p]-Mrx[p]
            q = 1
            NewMy[s][p] = A[s][q][0] * Mx[p] + A[s][q][1] * My[p] + A[s][q][2]
            ErrorMy[s][p] = NewMy[s][p] - Mry[p]
            ERMS[s][p] = sqrt((ErrorMx[s][p] * ErrorMx[s][p]) + (ErrorMy[s][p] * ErrorMy[s][p]))

        for t in range(length):
            sum = sum + ERMS[s][t]
        Avg = sum /length
        ERMSAvg[s] = Avg
    flg1, flg2,error=Find_bestA_F(ERMSAvg, count,ERMS,length)
    return flg1, flg2,error,NewMx,NewMy

def Find_bestA_F(ERMSAvg, count, ERMS,length):
    ''' After finding the ERMS and ERMSAvg now we can calculate the minimum error and say that the
     minimum ERMSAvg would be the best A_F values and store the index of that location for accessing
     '''
    error=[0 for v in range(length)]
    min_error = ERMSAvg[0]
    flag = 1
    for i in range(count):
        if (ERMSAvg[i] < min_error):
            min_error = ERMSAvg[i]
            flag = i
    print ERMS[flag]
    for i in range(length):
        error[i]=ERMS[flag][i]
    flg1, flg2=Find_error_points(error,length)
    return flg1,flg2,error

def Find_error_points(error,length):
    #find out the error points that have to be eliminated from the list
    max1 = 0
    max2 = 0
    flg1 = 0
    flg2 = 0
    for i in range(1,length):
        if (error[i] > max1):
            max1 =error[i]
            flg1 = i
    for i in range(1, length):
        if (error[i] > max2) and (i != flg1):
            max2 = error[i]
            flg2 = i
    print flg1,flg2
    return flg1, flg2


if __name__ == '__main__':
    Mx, My, Mrx, Mry, flg1, flg2,error= main()
