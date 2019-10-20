import json
def min(d,ch):
    mini=9999
    index=-1
    if ch==1:
        for i in range (len(d)):
            if d['s'+str(i)][0]<mini and d['s'+str(i)][1]!=1:
                mini=d['s'+str(i)][0]
                index=i
        return 's'+str(index)
    if ch == 2:
        for i in range(len(d)):
            if d['l'+str(i)][0] < mini and d['l'+str(i)][1] != 1:
                mini = d['l'+str(i)][0]
                index = i
        return ('l'+str(index))
    if ch == 3:
        for i in range(len(d)):
            if d['w'+str(i)][0] < mini and d['w'+str(i)][1] != 1:
                mini = d['w'+str(i)][0]
                index = i
        return ('w'+str(index))
# s_empty=5
# l_empty=8
# two_w=22
ds={'s0':[1,0],'s1':[1,0],'s2':[1,0],'s3':[2,0],'s4':[3,0]}
dl={'l0':[2,0],'l1':[3,0],'l2':[4,0],'l3':[1,0]}
two_w={'w0':[1,0],'w1':[3,0]}


# file1 = open("file.txt", "r") 
# for line in file1.readlines():
#     print(line)
#     print(type(line))
#     # print(dict1)
# # file1.readlines()
# file1.close()

ch=int(input('enter choice:'))
if(ch==1):
    temp=min(ds,ch)
    ds[temp][1]=1
elif (ch==2):
    temp=min(dl,ch)
    dl[temp][1]=1
elif (ch==3):
    temp=min(two_w,ch)
    two_w[temp][1]=1

# ds={'ds':ds}
# dl={'dl':dl}
# two_w={'two_w':two_w}
# with open('file.txt','w') as e:
#     e.writelines(json.dumps(ds))
#     e.writelines(json.dumps(dl))
#     e.writelines(json.dumps(two_w))

with open("data_file.json", "w") as write_file:
    json.dump([ds,dl,two_w], write_file)
