m = 200000
print(m)
for i in range(60):
    m += (m*5.375/100) - 5000
    m += (m*5.375/100) + 5000
print('best senario:')
print(m)
print('****')
print(m*5.375/100)
print('****')
# print('****')
# m = 4*30000
# for i in range(24):
#     m = m+(m*5.375/100)
# print('worst senario:')
# print(m)
# print('****')
# print(m*5.375/100)

# m = 8*35000
# for i in range(24):
#     m = m+(m*4.375/100)-5000
# print('best senario:')
# print(m)
# print('****')
# print(m*4.375/100)
# print('****')
# m = 8*25000
# for i in range(24):
#     m = m+(m*4/100)-4000
# print('worst senario:')
# print(m)
# print('****')
# print(m*4/100)


# for ii in range(5):
#     for i in range(12):
#         m += ((m)*5.375/100 )+ 2500
        
#     print(m)
# print('best senario:')
# print('****')
# print(m*5.375/100)