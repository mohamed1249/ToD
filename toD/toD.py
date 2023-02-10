import pandas as pd
import datetime as dt

class field:
    def __init__(self,name=None,NoT=0):
        self.ds = pd.Series(['Complement:'],index=['Task:'],dtype='object')
        self.name =name
        self.N=NoT
        for i in range(NoT):
            self.ds[input(f'Enter task number {i+1}: ')]=0
        self.AR=self.ds.iloc[1:].mean()
    def show(self):
        print(self.name+':')
        print(self.ds)
        print('Your achievement rate: %'+str(self.AR))
    def comp(self,task,ncomp=None):
        if type(task)==type([]):
            for n in range(len(ncomp)):
                self.ds[task[n]]=ncomp[n]
        elif type(task) == type({}):
            for e in task:
                self.ds[e]=task[e]
        elif type(task)==type(''):
            self.ds[task]=ncomp
        self.AR=self.ds.iloc[1:].mean()

class day(field):
    def __init__(self,d=None,N=None):
        if d == None:
            pass
        else:
            self.__d = dt.datetime(d[0],d[1],d[2])
            self.__fl=[]
            for n in range(N):
                self.__fl.append(field(input(f'Enter the name of field {n+1}: '),int(input('How many tasks in this field? '))))
            self.__b = pd.Series(['rate'],index=['thing'],dtype='object')
    def show(self):
        self.__AV=0
        print(self.__d.date())
        for field in self.__fl:
            field.show()
            self.__AV+=field.AR
        print('bonuses: ')
        print(self.__b)
        self.__ACH=(self.__AV+self.__b.iloc[1:].sum())/(len(self.__fl))
        print(f'Your achievement for today: %{self.__ACH}')
        del self.__AV
    def comp(self,field, task=None, ncomp=None):
        self.__AV=0
        if type(field)==type([]):
            for fld in field:
                for f in self.__fl:
                    if fld == f.name:
                        f.comp(task[field.index(fld)],ncomp[field.index(fld)])
        if type(field)==type({}):
            for fld in field:
                for f in self.__fl:
                    if fld == f.name:
                        f.comp(field[fld])
        if type(field)==type(''):
            for f in self.__fl:
                if field == f.name:
                    f.comp(task,ncomp)
        for field in self.__fl:
            self.__AV+=field.AR
        self.__ACH=(self.__AV+self.__b.iloc[1:].sum())/(len(self.__fl))
        del self.__AV
    def bonus(self,name,rate):
        for n in name:
            self.__b[n]=rate[name.index(n)]
    def __getitem__(self,key):
        if type(key)==type(""):
            for field in self.__fl:
                if field.name==key:
                    return field
        return self.__fl[key]
    def __setitem__(self,key,value):
        if type(key)==type(""):
            for field in self.__fl:
                if field.name==key:
                    field =value
        else:
            self.__fl[key] = value
    def __iadd__(self,add):
        self.__fl.append(add)
        return self
    def __bool__(self):
        if self.__ACH <75.0:
            return False
        return True
    def __call__(self,key=None):
        if key==None:
            print(str(self.__d.date())+f': %{self.__ACH}')
        elif key == 'ach':
            return self.__ACH
        elif key == 'bonus':
            return self.__b
        elif key == 'sump':
            return self.__b.iloc[1:].sum()
        else:
            for field in self.__fl:
                if key == field.name:
                    return field.AR
    def __str__(self):
        s= f'In day {self.__d.date()}, There was {len(self.__fl)} fields:\n'
        for field in self.__fl:
            s+=f'In field {field.name}, There was {field.N} tasks and you\'ve achieved %{field.AR} of those taskes.\n'
        s+= f"And you have done {self.__b.count()-1} things that have gived you bonus of %{self.__b.iloc[1:].sum()};\nSo that your achievement of day {self.__d.date()} was %{self.__ACH}"
        return s
    def commit(self):
        self.__last_series = pd.Series({'day:':self.__d.date()})
        for field in self.__fl:
            self.__last_series[field.name+':'] = ''
            self.__last_series = self.__last_series.append(field.ds[1:])
            self.__last_series[f'Your achievement rate in {field.name}:'] = field.AR
        self.__last_series['bonuses:'] = ''
        self.__last_series = self.__last_series.append(self.__b[1:])
        self.__last_series['Your achievement for today:'] = self.__ACH
        with open('{}{}.csv'.format(__file__[:-7]+'\data\\',str(self.__d.date().strftime("%Y_%b_%d"))), 'w') as f:
            self.__last_series.to_frame().to_csv(f,index=True,header=False)
    @staticmethod
    def getday(day):
        with open('{}{}.csv'.format(__file__[:-7]+'\data\\',day), 'r') as f:
            csvf = pd.read_csv(f,sep=';').dropna(axis=0,how='all')
            csvf.set_index('day:',inplace=True)
            csvf[csvf.isnull()]=''
            return csvf







        




# d=day([2022,2,20],1)
# d.comp({'study':{'toD':150},'sport':{'strech':100},'reading':{'2 houres':120}})
# d.bonus(['abdulsalam','zenab','tarteeb'],[40,160,40])
# d.commit()
# print(day().getday('2022_Feb_19'))