import numpy as np
from math import sqrt
import operator as op
#import textbox
import Geo_referencing

'''this table module actually has been used as this during the solving of linear equations 
sometimes a singular matrix can be produced so at that table pops up giving all coordinates as zero.
'''


def ncr(n, r):
    # for clculating ncr(number of total combinations of picking r points(in this whole thing it is 3) from a given n points(assumed it to be 8)
    try:
        r = min(r, n-r)
        if r == 0: return 1
        numer = reduce(op.mul, xrange(n, n-r, -1))
        denom = reduce(op.mul, xrange(1, r+1))
        return numer//denom
    except:
        print "no coordinates given for transformation"
        exit(True)

def main(Mx,My,Mrx,Mry):

    '''given  the Mx,My,Mrx,Mry Values from the shape file and solve them for A_F values
    and find the list of A_F values.
    1)here we consider initial 3 points so we take Mx[0],Mx[1],Mx[2] the x coordinates of the 3
    points similarly My[0],My[1],My[2] y coordinates of 3 points and similarly Mrx,Mry are taken
    and solved them this way we get 1-A to F values and by taking all the combinations we get ncr A to F values.
    '''
    length=len(Mx)
    count = 0
    val=ncr(length, 3)
    A = [[[0 for u in range(3)] for v in range(2)] for w in range(val)]
    for i in range(val):
        for j in range(i + 1, length):
            for k in range(j + 1, length):
                try:
                    equation1 = np.array([[Mx[i], My[i], 1], [Mx[j], My[j], 1], [Mx[k], My[k], 1]])
                    constant1 = np.array([Mrx[i], Mrx[j], Mrx[k]])
                    x = np.linalg.solve(equation1, constant1)

                    equation2 = np.array([[Mx[i], My[i], 1], [Mx[j],My[j], 1], [Mx[k], My[k], 1]])
                    constant2 = np.array([Mry[i], Mry[j],Mry[k]])
                    y = np.linalg.solve(equation2, constant2)

                # exception code that may be generated because of a singular points
                except np.linalg.linalg.LinAlgError as err:
                    if 'Singular matrix' in err.message:
                        print "the coordinates choosen are such a way that the matrix formed in one of the case was a singular matrix so retake values"
                        exit(True)
                    else:
                        raise
                p = 0
                for q in range(3):
                    A[count][p][q] = x[q]
                p = 1
                for q in range(3):
                    A[count][p][q] = y[q]
                count = count + 1
    #All the ncr (8c3)A_F values are stored in 3D list
    flg1, flg2,error,NewMx,NewMy,flag=List_MxMy_formedfromA_F_AvgERMS(Mx, My, count, A,Mrx, Mry, length)
    return flg1, flg2, error,flag,A


def List_MxMy_formedfromA_F_AvgERMS(Mx, My, count, A,Mrx,Mry,length):
    ''' Now by taking each A to F values and do the calculation using Mx,My and calculate the
    new Mrx,Mry values and now subtract it with the old values to find out the error.
    This way we get error in x and error in y and now we calculate rms for each point and then
    we get the average of all the points for any given A to F values.'''
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
    flg1, flg2,error,flag=Find_bestA_F(ERMSAvg, count,ERMS,length)
    return flg1, flg2,error,NewMx,NewMy,flag

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
    return flg1,flg2,error,flag

def Find_error_points(error,length):
    #find out the error points that have to be eliminated from the list
    max1 = 0
    max2 = 0
    flg1 = 0
    flg2 = 0
    for i in range(0,length):
        if (error[i] > max1):
            max1 =error[i]
            flg1 = i
    for i in range(0, length):
        if (error[i] > max2) and (i != flg1):
            max2 = error[i]
            flg2 = i
    return flg1, flg2


if __name__ == '__main__':
        flg1, flg2, error,flag,A= main(Geo_referencing.Mx, Geo_referencing.My, Geo_referencing.Mrx, Geo_referencing.Mry)
        flg1, flg2, error,flag,A = main(textbox.inputshapefile1.Mx, textbox.inputshapefile1.My, textbox.inputshapefile2.Mrx, textbox.inputshapefile2.Mry)

''' 
These coordinates were used for testing
Mx = [120,300,300,120,-120,-300,-300,-120]
   My = [300,120,-120,-300,-300,-120,120,300]
   Mrx = [12,30,30,12,-12,-30,-30,-12]
   Mry = [30,12,-12,-30,-30,-12,12,30]
   #coordinates from the shapefile of my_polygon and other_polygon'''
'''Shapefile.Mx=[-0.5096, -0.2453, 0.0591, 0.3319, 0.3504, 0.1289, -0.2178, -0.4906]
Shapefile.My=[0.4664, 0.6144, 0.6187, 0.3966, 0.0435, -0.2102, -0.2123, 0.09216]
Shapefile.Mrx=[-1.4803, -1.3629, -1.0987, -0.6693, -0.3691, -0.3154, -0.6366, -1.0811]
Shapefile.Mry=[-0.0122, 0.3634, 0.6267, -0.6619, 0.4104, 0.0525, -0.3451, -0.2571]
'''
