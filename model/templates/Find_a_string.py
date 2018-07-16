import textwrap
a = 'ABCDEFGHIJKLIMNOQRSTUVWXYZ'
b = 'ABCDCDC'

def  count_substring(string, sub_string):
    count = 0
    sub_len = len(sub_string)
    for i  in range(len(string)):
        if i+sub_len <= len(string):
            if (string[i:i+sub_len])==sub_string:
                count+=1
    return count
def abcc(a,b):
    leng=4
    j=0
    lists=[]
    for  i in range(len(a)):
        if j <= len(a):
            print(a[j:j+leng])
            j=j+leng
    return

#print(abcc(a,4))



print(textwrap.fill(a,4))