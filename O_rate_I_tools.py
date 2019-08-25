###############################################################
##################### Diagnosis plot tool #####################
###############################################################
# What is this  : Create a graph of the number and objective variable ratio by category or numerical class.
# Output is graph and matrix of variable.
#
#  1st argument : Input data file path
#  2nd argument : Objective variable
#  3rd argument : Unusing variable
#  4th argument : Data type file path
#  5th argument : Binomial Flag(if objective variable is binomial then 1 else 0)
#  6th argument : figure output path
#  7th argument : csv output path
#  8th argument : 
#  9th argument : 
# 10th argument : 
#
# create date   : 2019/08/15 -- crazysrot
# How to use    : from lib import O_rate_I_tools as OI
#                 OI.O_rate_I_tool(args1, args2, args3, args4, args5, args6, args7, args8, args9, args10)
###############################################################
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'AppleGothic'
#plt.rcParams['font.family'] = 'IPAPGothic'
import math
from lib import sturges_rule  as stur
#import japanize_matplotlib
#import sturges_rule  as stur

binomial_flg = 1
def O_rate_I_tool(args1, args2, args3, args4, args5, args6, args7):
    args = sys.argv
    print(args1)
    print(args2)
    print(args3)
    print(args4)
    print(args5)
    print(args6)
    print(args7)

    org_input_data = pd.read_csv(args1)
    colname = org_input_data.columns.values
    print_str = 'column name list : ' + str(colname)
    print(print_str)
    df_data_type = pd.read_csv(args4, header=None, sep=',')
    binomial_flg = args5

    ##### Make diagnosis plot per each explanatory variable
    for i in range(10):
#    for i in range(len(colname)):
        EX_DATA_TYPE = df_data_type.iloc[i-1,1]

        print_str = '---------------------------------------------------------------------------------------------------------------------------------------'
        print(print_str)
        print_str = '               No.' + str(i) + ', Colname:' + colname[i] + ', EX_DATA_TYPE:' + EX_DATA_TYPE
        print(print_str)
        print_str = '---------------------------------------------------------------------------------------------------------------------------------------'
        print(print_str)

        input_data = org_input_data.dropna(subset=[org_input_data.columns.values[i]])

        ##### Skip when Objective and Count variable 
        if colname[i] == args2 or colname[i] == args3 or EX_DATA_TYPE == 'text':
            print_str = '----------------Skip'
            print(print_str)
        else:
            print_str = '----------------Do'
            print(print_str)
            
            ##### make bin range to separete variable class
            ##### Categorical and numeric variable change the correspondence.
            if EX_DATA_TYPE == 'numeric':
                bin_num = stur.stur_rule(len(input_data[colname[i]]))
                max_val = np.round(max(input_data[colname[i]]))
                min_val = np.round(min(input_data[colname[i]]))

                if max_val == min_val:
                    print_str = '----------------Skip'
                    print(print_str)
                    continue
                else:
                    bin_matrix = np.arange(min_val,max_val + (max_val-min_val)/bin_num,(max_val-min_val)/bin_num)
                    bin_matrix = bin_matrix[bin_matrix<=max_val]
            elif EX_DATA_TYPE == 'category' or EX_DATA_TYPE == 'binomial':
                bin_num = len(input_data[colname[i]].unique())
                if bin_num > 100:
                    print_str = '----------------Skip'
                    print(print_str)
                    print('Number of bin is too much, therefore skip ' + colname[i])
                    print_str = 'Count of unique is ' + str(len(input_data[colname[i]].unique()))
                    print(print_str)
                    continue

            else:
                print_str ='This data is not in numeric or category or binomial'
                print(print_str)
                print_str = '--------------------------------Skip--------------------------------'
                print(print_str)

            ##### make matrix for diagnosis plot per each explanatory variable
            if EX_DATA_TYPE == 'numeric':
                grouped = input_data.groupby(pd.cut(input_data[colname[i]],bin_matrix))
                out_df = pd.concat([grouped.count()[args3], grouped.sum()[args2]], axis = 1)
                print(out_df[args3])
                out_df['obj_mean'] = grouped.mean()[args2]
                out_df['obj_var'] = grouped.var()[args2]
                left_matrix = np.arange(min_val,max_val,(max_val-min_val)/bin_num)
                left_matrix = left_matrix[left_matrix<=max_val]

            else:
                grouped = input_data.groupby([colname[i]])
                out_df = pd.concat([grouped.count()[args3], grouped.sum()[args2]], axis = 1)
                out_df['obj_mean'] = grouped.mean()[args2]
                out_df['obj_var'] = grouped.var()[args2]
                left_matrix = np.array(out_df.index.values, dtype='unicode')

            height_matrix = np.array(out_df['obj_mean'].fillna(0))

            ##### Create confidence interval
            if binomial_flg == 1:
                obj_ci = 1.96*np.sqrt((out_df['obj_mean']*(1.0-out_df['obj_mean'])) / out_df[args3])
            elif binomial_flg == 0:
                obj_ci = 1.96*np.sqrt(out_df['obj_var'] / out_df[args3])
                out_df['obj_median'] = grouped.median()[args2]
            
            print_str='-------- Length of left matrix=' + str(len(left_matrix))
            print(print_str)
            print_str='-------- Length of height matrix =' + str(len(height_matrix))
            print(print_str)
            print_str='-------- Type of left matrix=' + str(type(left_matrix))
            print(print_str)
            print_str='-------- Type of height matrix =' + str(type(height_matrix))
            print(print_str)
            
            ##### adjust between left and height matrix
            while len(left_matrix) > len(height_matrix):
                left_matrix = np.delete(left_matrix, len(left_matrix)-1)
            
            if EX_DATA_TYPE == 'numeric':
                print_str = '-------- Max value : ' + str(max_val)
                print(print_str)
                print_str = '-------- Minimum value : ' + str(min_val)
                print(print_str)
                print_str = '-------- Bin number of sturges : ' + str(bin_num)
                print(print_str)
#                print_str = '-------- Bin of sturges : ' + str(bin_matrix)
#                print(print_str)
            else:
                print_str = '-------- Bin number : ' + str(bin_num)
                print(print_str)
                
            print_str = '-------- Left matrix : ' + str(len(left_matrix))
            print(print_str)
            print(left_matrix)
            print_str = '-------- Height matrix : ' + str(len(height_matrix))
            print(print_str)
            print(height_matrix)

            ##### Plot graph
#            plt.plot(left_matrix, height_matrix)
#            plt.bar(left_matrix, height_matrix)

            fig, ax1 = plt.subplots()
            ax1.bar(left_matrix, out_df[args3])
            ax1.set_xlabel(colname[i], fontname='MS Gothic')
#            ax1.set_xlabel(colname[i])
            labels = ax1.get_xticklabels()
            plt.setp(labels, rotation=45, fontsize=10);
            ax1.set_ylabel('freq - << ' + colname[i] + ' >>')
            ax2 = ax1.twinx()  # 2つのプロットを関連付ける
#            ax2.plot(left_matrix, out_df['obj_mean'], color='Red')
            ax2.errorbar(left_matrix, out_df['obj_mean'], obj_ci, fmt='ro',ecolor='r')
            if binomial_flg == 1:
                ax2.set_ylabel('Objective Rate - << ' + args2 + ' >>')
            else:
                ax2.set_ylabel('mean - << ' + args2 + ' >>')
#            plt.show()
            fig_name = args6 + '/' + str('{:0=3}'.format(i)) + '_' + str(colname[i]) + '.png'
            ##### Save plotted graph
            plt.savefig(fig_name, bbox_inches='tight') #tight means to change auto size picture.
            plt.close()
            
            ##### Save created matrix
            out_df['ci'] = obj_ci
#            print(out_df)
            #####縦計での構成比（objもallも）
            csv_name = args7 + '/' + str('{:0=3}'.format(i)) + '_' + str(colname[i]) + '.csv'
            out_df.to_csv(csv_name)
            
#            print_str = '---------------------------------------------------------------------------------------------------------------------------------------'

#            print(print_str)


