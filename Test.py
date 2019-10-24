import numpy as np
import weio
import sys



def compare_df(df_ref,df_cur,precision=1.e-3):

    SensorFailed=[]
    nOK=0
    for c in df_ref.columns.values:
        if c not in df_cur.columns.values:
            print('[WARN] Sensor missing in current version:',c)
        else:
            x0=df_ref[c].values
            x1=df_cur[c].values
            mref=np.mean(abs(x0))

            absdiff_mean = np.mean(np.abs(x0-x1))
            absdiff_max  = np.max(np.abs(x0-x1))

            if mref==0:
                mref=precision/100

            reldiff_mean = np.mean(np.abs(x0-x1)/mref)
            reldiff_max  = np.max( np.abs(x0-x1)/mref)

            if reldiff_mean>1e-3:
                print('{:15s} : rel mean {}, rel max {}'.format(c,reldiff_mean,reldiff_max))
                SensorFailed.append(c)
            else:
                nOK+=1
#                 
#             if absdiff_mean>1e-3:
#                 print('{:15s} : abs mean {}, abs max {}'.format(c,absdiff_mean,absdiff_max))
#                 SensorFailed.append(c)
#             else:
#                 nOK+=1
            
    if len(SensorFailed)==0:
        print('[ OK ] {}/{} sensors passed'.format(nOK,len(df_ref.columns.values)))
    else:
        print('[FAIL] {}/{} sensors passed'.format(nOK,len(df_ref.columns.values)))




if __name__=='__main__':
    if len(sys.argv)<=2:
        print('')
        print('usage:   file_ref file_new [precision]')
        print('')
        raise Exception('This script requires two files')

    file_ref=sys.argv[1]
    file_cur=sys.argv[2]
    if len(sys.argv)==4:
        precision=sys.argv[3]
    else:
        precision=1.e-3

    df_ref = weio.read(file_ref).toDataFrame()
    df_cur = weio.read(file_cur).toDataFrame()

    compare_df(df_ref,df_cur,precision)
