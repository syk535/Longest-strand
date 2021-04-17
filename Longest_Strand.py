#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np

# A regular method to obtain the longest strand between two files
def largest(sample_1, sample_2):
    p=len(sample_1)
    q=len(sample_2)
    table=np.zeros((p,q))
    for i in range(p):
        for j in range(q):
            if sample_1[i]==sample_2[j]:
                if i==0 or j==0:
                    table[i,j]=1
                else:
                    table[i,j]=table[i-1,j-1]+1
    max_len=table.max()
    place=np.where(table==max_len)
    return max_len, place


# A improved method to save the memory due to that the sizes of files are large
def largest_save(sample_1, sample_2):
    p=len(sample_1)
    q=len(sample_2)
    row_old=np.zeros(q)
    max_len=0
    for j in range (q):
        if sample_1[0]==sample_2[j]:
            row_old[j]=1
    for i in range(1,p):
        row_new=np.zeros(q)
        if sample_1[i]==sample_2[0]:
            row_new[1]=1
        for j in range(1,q):
            if sample_1[i]==sample_2[j]:
                row_new[j]=row_old[j-1]+1
                if row_new[j]>max_len:
                    max_len=row_new[j]
                    place=[[i,j]]
                elif row_new[j]==max_len:
                    place.append([i,j])
        row_old=row_new
    return max_len, place
    

    
    
# Read files in a way which can be extended to a large number of files with the name structure    
sample=list()
total=10
for i in range(1,total+1):
    name="sample."+str(i)
    with open(name,'rb') as file:
        sample_sub=file.read()
    sample.append(sample_sub)

max_all=np.zeros((total,total))
place_all=list()

# Find the longest strand between each pair of files
# Because the longest strand of bytes that exists in at least two files must be one of the longest strands between all pairs of files
for num_1  in range(total-1):
    for num_2 in range(num_1+1,total):
        max_i, place_i=largest_save(sample[num_1], sample[num_2])
        max_all[num_1,num_2]=max_i
        place_all.append(place_i)

# Analyze the longest strands between all pairs of files
max_len=max_all.max()
pairs=np.where(max_all==max_len)
num_pairs=len(pairs[0])
num_unique_largest_strand=1
files_selected=[pairs[0][0]+1,pairs[1][0]+1]
output=open('Output.txt','w')

# To discuss how many pairs to achieve the largest length and whether these longest strands are the same.
# If we have multiple distinct longest strands, it will show the corresponding files and offets, respectively.
if num_pairs==1 and len(place_all[place_selected])==1:
    place_selected=int(files_selected[0]*(2*total-1)/2-files_selected[0]**2/2+files_selected[1]-11)
    offset_1=[place_all[place_selected][0][0]-max_len+2,place_all[place_selected][0][0]+1]
    offset_2=[place_all[place_selected][0][1]-max_len+2,place_all[place_selected][0][1]+1]
    output.write('We have '+str(num_unique_largest_strand)+' unique largest strand.'+'\n')
    output.write('The length of the strand is '+str(int(max_len))+'.'+'\n')
    output.write('Files are Sample.'+str(files_selected[0])+' and Sample.'+str(files_selected[1])+'.'+'\n')
    output.write("Offset in Smaple."+str(files_selected[0])+" is "+str(offset_1)+'.'+'\n')
    output.write("Offset in Smaple."+str(files_selected[1])+" is "+str(offset_2)+'.')
else:
    g=len(place_all[place_selected])
    strings=list()
    offset=[[['Sample.'+str(pairs[0][0]+1),place_all[place_selected][0][0]-max_len+2,place_all[place_selected][0][0]+1]]]
    offset[0].append(['Sample.'+str(pairs[1][0]+1),place_all[place_selected][0][1]-max_len+2,place_all[place_selected][0][1]+1])
    string.append(sample[files_selected[0]-1][int(offset_1[0]-1):int(offset_1[1])])
    for i in range(1,g):
        offset1_new=['Sample.'+str(pairs[0][0]+1),place_all[place_selected][i][0]-max_len+2,place_all[place_selected][i][0]+1]
        offset2_new=['Sample.'+str(pairs[1][0]+1),place_all[place_selected][i][1]-max_len+2,place_all[place_selected][i][1]+1]
        if_in=0
        string_new=sample[files_selected[0]-1][int(offset1_new[1]-1):int(offset1_new[2])]
        for j in range(len(strings)):
            if string_new==strings[j]:
                offset[j].append(offset1_new)
                offset[j].append(offset2_new)
                if_in=1
                break
        if if_in==1:
            offset.append([offset1_new])
            offset.append([offset2_new])
            strings.append(string_new)
    for k in range(1,num_pairs):
        files_selected=[pairs[0][k]+1,pairs[1][k]+1]
        place_selected=int(files_selected[0]*(2*total-1)/2-files_selected[0]**2/2+files_selected[1]-11)
        g=len(place_all[place_selected])
        for i in range(g):
            offset1_new=['Sample.'+str(pairs[0][k])+1,place_all[place_selected][i][0]-max_len+2,place_all[place_selected][i][0]+1]
            offset2_new=['Sample.'+str(pairs[1][k])+1,place_all[place_selected][i][1]-max_len+2,place_all[place_selected][i][1]+1]
            if_in=0
            string_new=sample[files_selected[0]-1][int(offset1_new[1]-1):int(offset1_new[2])]
            for j in range(len(strings)):
                if string_new==strings[j]:
                    offset[j].append(offset1_new)
                    offset[j].append(offset2_new)
                    if_in=1
                    break
            if if_in==1:
                offset.append([offset1_new])
                offset.append([offset2_new])
                strings.append(string_new)
    num_unique_largest_strand=len(string)   
    output.write('We have '+str(num_unique_largest_strand)+' unique largest strand(s).'+'\n')
    output.wirte('The length of the strand(s) is '+str(max_len)+'.'+'\n')
    output.wirte('Different unique largest strands with corresponding file names and offsets are the following:'+'\n')
    output.wirte(offset)

##For our samples, only one pair achieve the largest length, and only one sub-strand in each file attain the length, which is the simplest condition.

##To test if two sub-strands are the same and achieve the largest length.
assert(len(sample[files_selected[0]-1][int(offset_1[0]-1):int(offset_1[1])])==max_len)
assert(sample[files_selected[0]-1][int(offset_1[0]-1):int(offset_1[1])]==sample[files_selected[1]-1][int(offset_2[0]-1):int(offset_2[1])])

