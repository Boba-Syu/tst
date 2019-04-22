import math
import copy
q=1
while q>0:
    str1=input("请输入要排列的字符串：\n")             #用户输入选项
    str2=input("请输入要排列的字符串分隔符：\n")       #用户输入选项
    print('')
    n=len(str1)
    n_ = math.factorial(n)
    list1=[]
    list2=[]
    for i in range(1,n_+1):                             #定义填充列表
        exec('k%s=[]'%i)


    for i in range(n):                                  #填充首列表
        list1+=str1[i]
    k1=list1


    for i in range(1,n):                                #预填充
        i1=math.factorial(i)
        i2=math.factorial(i+1)+1
        for j in range(i1,i2):
            j1=(j-i1)%i1+1
            exec('k%s=k%s'%(j,j1))


    for i in range(1,n):                                #替换次序
        i1=math.factorial(i)
        for j1 in range(1,i+1):                         #替换基准
            for j2 in range(1,i1+1):                    #替换个案基准
                y1=j1*i1+j2
                for j in range(1,i+1):                  #查找替换 
                    exec('c,d=list1[j1-i-1],k%s[-j]'%j2)
                    if c==d:
                        b=copy.deepcopy(eval('k%s'%j2))
                        b[-i-1],b[-j]=b[-j],b[-i-1]
                        exec('k%s=copy.deepcopy(b)'%y1)
                        del b
                        break


    for i in range(n_):                                 #填充输出列表
        list2.append(eval('k%s'%(i+1)))
    print("排列依次为：")


    for i in range(n_):                                 #控制输出
        for j in range(n):
            print(list2[i][j],end='')
            if j<n-1:
                print(str2,end='')
            if j == n-1:
                print("")
    print('总计数为：%d'%n_)

    #s=0                                                #对于数字排列的限制输出，s计数
    #for i in range(n_):                                #输出次序
        #k=0;
        #for j in range(n-1):
            #if abs(eval(list2[i][j])-eval(list2[i][j+1]))==1:      #限制输出条件
               # k+=1
        #if k==0:                                       #条件输出
            #s+=1
            #print(list2[i])
    #print('相邻两个人的号码相差大于1的排法的总数为：',end='')
    #print(s)
    #print('具体如上所示.')
    #o=input()
    q=eval(input("是否继续：(是：1,否0).\n"))
    print('\n\n')
