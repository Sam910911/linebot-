import requests,math
from bs4 import BeautifulSoup
compare = ''
url = 'https://www.etax.nat.gov.tw/etw-main/web/ETW183W1/'
response = requests.get(url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text,'html.parser')
data = soup.find_all('tbody')
table = data[0].find_all('tr')
latest = table[1].find('a').get('href')
#print(latest[23])
for i in range (23,28):
    compare += latest[i]
#==============================================================================
month = int(input('輸入'))
url = 'https://www.etax.nat.gov.tw'+str(latest)
url2 = 'https://www.etax.nat.gov.tw/etw-main/web/ETW183W2_'+str(month)
if int(compare) + 1 >= month:
    if month % 2 == 0:
        month -= 1
    url = 'https://www.etax.nat.gov.tw/etw-main/web/ETW183W2_'+str(month)
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text,'html.parser')
    data = soup.find_all('tbody')
    number = data[0].find_all('td',{'class':'number'})
    special = number[0].text
    grand = number[1].text
    first = number[2].text
    addsix = number[3].text 
    output = str(int(month/100))+"年"+str(month%100)+'、'+str(month%100 + 1)+"月統一發票\n特別獎:"+special+'\n特獎:'+grand+'\n頭獎:'+first+'\n增開六獎:'+addsix
    print(output)
else:
    print('please enter number 10105 ~ ' + compare)
