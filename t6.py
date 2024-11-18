number=int(input("تعداد دانش آموزان اعزامی به اردو"))
van=number
van=van//10
n=number%10
if n>0:
    van=van+1
hazinevan=van*150000//number
print(hazinevan+25000)