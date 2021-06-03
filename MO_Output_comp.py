import glob
import os
import numpy as np

def listPatternFiles(searchDir, pattern):
    files = glob.glob(os.path.join(searchDir, pattern))
    return files

def comp_type(output_df_type,ref_df_type):  
    return (output_df_type.dtypes.values == ref_df_type.dtypes.values).all()

def comp_names(output_df_col,ref_df_col):
    return (output_df_col.columns == ref_df_col.columns).all()

def comp_format(output_df,ref_df,object_as_datetime=True):
    for j in range(ref_df.shape[1]):
        ref_col = ref_df[ref_df.columns[j]]
        test_col = output_df[output_df.columns[j]]  

        if isinstance(ref_col[0],(object)) and not\
            isinstance(ref_col[0],(np.int32,np.int64,np.float32,np.float64)):
            if object_as_datetime:
                ref_col_split = ref_col.apply(lambda x: x.split(' '))
                len_ref_col_split = ref_col_split.apply(lambda x: len(x))
                test_col_split = test_col.apply(lambda x: x.split(' '))
                len_test_col_split = test_col_split.apply(lambda x: len(x))

                if max(len_ref_col_split) != max(len_test_col_split) or\
                    min(len_ref_col_split) != min(len_test_col_split):
                    return False
            else:   # For objects in general, to be reviewed with more specific datasets 
                len_ref_col = ref_col.apply(lambda x: len(x))
                len_test_col = test_col.apply(lambda x: len(x))
                if max(len_ref_col) != max(len_test_col) or\
                    min(len_ref_col) != min(len_test_col):
                    return False
        elif isinstance(ref_col[0],(np.int32,np.int64)):
            ref_col_mod = ref_col.apply(lambda x: x % 1)
            test_col_mod = test_col.apply(lambda x: x % 1)
            if sum(ref_col_mod) != sum(test_col_mod):
                return False
        elif isinstance(ref_col[0],(np.float32,np.float64)):
            ref_col_split = ref_col.apply(lambda x: str(x).split('.'))
            test_col_split = test_col.apply(lambda x: str(x).split('.'))
            len_ref_col_split = ref_col_split.apply(lambda x: len(x))
            len_test_col_split = test_col_split.apply(lambda x: len(x))
            if max(len_ref_col_split) != max(len_test_col_split) or\
                min(len_ref_col_split) != min(len_ref_col_split):
                return False
        else:
            raise ValueError('Type not recognized for column %d.' % j)
    return True

def is_equal(output_df,ref_df):
  
    sameDim = output_df.shape == ref_df.shape
    if sameDim:
      sameType = comp_type(output_df, ref_df)
    else:
      sameType = False    
    sameName = comp_names(output_df,ref_df)
    if sameDim and sameType:
      sameFormat = comp_format(output_df,ref_df)
    else:
      sameFormat = False 
    
    return all([sameDim, sameType, sameName, sameFormat])

def compareSingleFile(outputFile, referenceFile, delimiter = ';', decimal='.'):
    outputData = pd.read_csv(outputFile, delimiter=delimiter, decimal=decimal)
    print(outputFile)
    referenceData = pd.read_csv(referenceFile, delimiter=delimiter, decimal=decimal)

    return is_equal(outputData, referenceData)

def compareFiles(workingDir,outputFilePattern, refFileDir, refFileName):
    equal = []
    listOutputfiles = listPatternFiles(workingDir, outputFilePattern)
    print(listPatternFiles(refFileDir,refFileName))
    refFile = listPatternFiles(refFileDir,refFileName)[0]
    for file in listOutputfiles:
        equal.append(compareSingleFile(file,refFile))

    return all(equal)
  
refFileDir = '/dbfs/mnt/silver/MOM/FrozenRun20210511-reportdate_20210510/Model Outputs/'
refFileName = 'Daily_202105110940_BASE CASE_20201201_20251231_AuctionResult1.csv'
WorkingDir = '/dbfs/mnt/silver/MOM/Prod_Base Case/2021/05/27/20210528000812/Model Outputs/'
outputFilePattern = r'*AuctionResult*' 

#The four previous strings should be modified when needed

compareFiles(WorkingDir, outputFilePattern, refFileDir, refFileName)
