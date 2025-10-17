
class Person:
    def __init__(self, fname, lname,ege):
        self.firstname = fname
        self.lastname = lname
        self.ege=ege
    def england(self):
        print(self.firstname, self.lastname,self.ege)
    def persian(self):
        print(self.firstname,self.lastname,self.ege)
m=1
while m>=1:
    n=input("""
            1.فارسی
            2.england
            3.exit
            """)
    if n=='1':
        name=input("نام را وارد کنید")
        famil=input("نام خانوادگی را وارد کنید ")
        age=input("سن را وارد کنید ")
        x=Person(name,famil,age)
        x.persian()
    elif n==2:
        name=input("name ra vared konid")
        famil=input("famoil ra vareds konid ")
        age=input("sen vared kponid ")
        x=Person(name,famil,age)
        x.england()
    elif n==3:
        break