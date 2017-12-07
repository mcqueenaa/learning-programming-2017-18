import matplotlib.pyplot as plt

i_f1_m_Dzhuen = []
i_f2_m_Dzhuen = []
i_f1_f_Dzhuen = []
i_f2_f_Dzhuen = []
I_f1_m_Dzhuen = []
I_f2_m_Dzhuen = []
I_f1_f_Dzhuen = []
I_f2_f_Dzhuen = []
e_f1_m_Dzhuen = []
e_f2_m_Dzhuen = []
e_f1_f_Dzhuen = []
e_f2_f_Dzhuen = []

i_f1_m_Naikhin = []
i_f2_m_Naikhin = []
i_f1_f_Naikhin = []
i_f2_f_Naikhin = []
I_f1_m_Naikhin = []
I_f2_m_Naikhin = []
I_f1_f_Naikhin = []
I_f2_f_Naikhin = []
e_f1_m_Naikhin = []
e_f2_m_Naikhin = []
e_f1_f_Naikhin = []
e_f2_f_Naikhin = []

with open('table.csv', 'r', encoding = 'utf-8') as t:
    table = t.readlines()

for i in table:
    if i != 1:
        line = i.split(';')
        if line[2] == 'Dzhuen':
            if line[3] == 'i':
                if line[1] == 'm':
                    i_f1_m_Dzhuen.append(float(line[4]))
                    i_f2_m_Dzhuen.append(float(line[5]))
                else:
                    i_f1_f_Dzhuen.append(float(line[4]))
                    i_f2_f_Dzhuen.append(float(line[5]))
            elif line[3] == 'I':
                if line[1] == 'm':
                    I_f1_m_Dzhuen.append(float(line[4]))
                    I_f2_m_Dzhuen.append(float(line[5]))
                else:
                    I_f1_f_Dzhuen.append(float(line[4]))
                    I_f2_f_Dzhuen.append(float(line[5]))
            else:
                if line[1] == 'm':
                    e_f1_m_Dzhuen.append(float(line[4]))
                    e_f2_m_Dzhuen.append(float(line[5]))
                else:
                    e_f1_f_Dzhuen.append(float(line[4]))
                    e_f2_f_Dzhuen.append(float(line[5]))
        if line[2] == 'Naikhin':
            if line[3] == 'i':
                if line[1] == 'm':
                    i_f1_m_Naikhin.append(float(line[4]))
                    i_f2_m_Naikhin.append(float(line[5]))
                else:
                    i_f1_f_Naikhin.append(float(line[4]))
                    i_f2_f_Naikhin.append(float(line[5]))
            elif line[3] == 'I':
                if line[1] == 'm':
                    I_f1_m_Naikhin.append(float(line[4]))
                    I_f2_m_Naikhin.append(float(line[5]))
                else:
                    I_f1_f_Naikhin.append(float(line[4]))
                    I_f2_f_Naikhin.append(float(line[5]))
            else:
                if line[1] == 'm':
                    e_f1_m_Naikhin.append(float(line[4]))
                    e_f2_m_Naikhin.append(float(line[5]))
                else:
                    e_f1_f_Naikhin.append(float(line[4]))
                    e_f2_f_Naikhin.append(float(line[5]))
print(i_f1_m_Dzhuen)
alll = []
alll.append(i_f1_m_Dzhuen)
alll.append(i_f2_m_Dzhuen)
alll.append(i_f1_f_Dzhuen)
alll.append(i_f2_f_Dzhuen)
alll.append(I_f1_m_Dzhuen)
alll.append(I_f2_m_Dzhuen)
alll.append(I_f1_f_Dzhuen)
alll.append(I_f2_f_Dzhuen)
alll.append(e_f1_m_Dzhuen)
alll.append(e_f2_m_Dzhuen)
alll.append(e_f1_f_Dzhuen)
alll.append(e_f2_f_Dzhuen)

alll.append(i_f1_m_Naikhin)
alll.append(i_f2_m_Naikhin)
alll.append(i_f1_f_Naikhin)
alll.append(i_f2_f_Naikhin)
alll.append(I_f1_m_Naikhin)
alll.append(I_f2_m_Naikhin)
alll.append(I_f1_f_Naikhin)
alll.append(I_f2_f_Naikhin)
alll.append(e_f1_m_Naikhin)
alll.append(e_f2_m_Naikhin)
alll.append(e_f1_f_Naikhin)
alll.append(e_f2_f_Naikhin)

average = []
for a in alll:
    s = 0
    for i in a:
        s += i
    av = s/len(a)
    average.append(av)
        

#Джуен
X = [1,2,3]
Yf1m = [average[0], average[4], average[8]]
Yf2m = [average[1], average[5], average[9]]
Yf1f = [average[2], average[6], average[10]]
Yf2f = [average[3], average[7], average[11]]

#Найкин
X = [1,2,3]
Yf1mN = [average[12], average[16], average[20]]
Yf2mN = [average[13], average[17], average[21]]
Yf1fN = [average[14], average[18], average[22]]
Yf2fN = [average[15], average[19], average[23]]

names = ['i', 'I', 'e']
plt.xticks(X, names) ##!!!! чтобы в иксе были строки

##fig, ax = plt.subplots(nrows = 2, ncols=1)
##
##for row in ax:
##    for col in row:
##      
##          col.plot(X, Yf1m)
##          col.plot(X, Yf2m)
##          col.plot(X, Yf1f)
##          col.plot(X, Yf2f)
##      if row == 2:
##          col.plot(X, Yf1mN)
##          col.plot(X, Yf2mN)
##          col.plot(X, Yf1fN)
##          col.plot(X, Yf2fN)
      
plt.plot(X, Yf1m)
plt.plot(X, Yf2m)
plt.plot(X, Yf1f)
plt.plot(X, Yf2f) 
plt.show()

plt.xticks(X, names)
plt.plot(X, Yf1mN)
plt.plot(X, Yf2mN)
plt.plot(X, Yf1fN)
plt.plot(X, Yf2fN) 
plt.show()
            





