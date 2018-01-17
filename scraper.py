
# coding: utf-8

# In[11]:


#import libraries
import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import re
import pickle


# In[3]:


def set_url_parse(url):
    url = url
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page,'html.parser')
    return soup


# In[12]:


reviews_df = pd.DataFrame()
prices_df = pd.DataFrame()


# In[13]:


urls =['https://www.cardekho.com/cars/Maruti','https://www.cardekho.com/cars/Hyundai','https://www.cardekho.com/cars/Honda','https://www.cardekho.com/cars/Toyota','https://www.cardekho.com/cars/Mahindra','https://www.cardekho.com/cars/Tata','https://www.cardekho.com/cars/Ford','https://www.cardekho.com/cars/Renault','https://www.cardekho.com/cars/Volkswagen','https://www.cardekho.com/cars/Audi','https://www.cardekho.com/cars/Nissan','https://www.cardekho.com/cars/Datsun','https://www.cardekho.com/cars/Mercedes-Benz','https://www.cardekho.com/cars/Jaguar','https://www.cardekho.com/cars/BMW','https://www.cardekho.com/cars/Skoda','https://www.cardekho.com/cars/Fiat','https://www.cardekho.com/cars/Ferrari','https://www.cardekho.com/cars/Land_Rover','https://www.cardekho.com/cars/Rolls-Royce','https://www.cardekho.com/cars/Porsche','https://www.cardekho.com/cars/Bentley','https://www.cardekho.com/cars/Mitsubishi','https://www.cardekho.com/cars/DC','https://www.cardekho.com/cars/Bugatti','https://www.cardekho.com/cars/Force','https://www.cardekho.com/cars/ICML','https://www.cardekho.com/cars/Isuzu','https://www.cardekho.com/cars/Lamborghini','https://www.cardekho.com/cars/Mahindra_Ssangyong','https://www.cardekho.com/cars/Mini','https://www.cardekho.com/cars/Aston_Martin','https://www.cardekho.com/cars/Premier','https://www.cardekho.com/cars/Volvo','https://www.cardekho.com/cars/Abarth','https://www.cardekho.com/cars/Conquest','https://www.cardekho.com/cars/Jeep','https://www.cardekho.com/cars/Maserati','https://www.cardekho.com/cars/Tesla','https://www.cardekho.com/cars/Lexus','https://www.cardekho.com/cars/Chevrolet']
brands = ['Maruti Suzuki','Hyundai','Honda','Toyota','Mahindra','Tata','Ford','Renault','Volkswagen','Audi','Nissan','Datsun','Mercedes-Benz','Jaguar','BMW','Skoda','Fiat','Ferrari','Land Rover','Rolls-Royce','Porche','Bentley','Mitsubishi','DC','Bugatti','Force','ICML','Isuzu','Lamborghini','Mahindra Ssangyong','Mini','Aston Martin','Premier','Volvo','Abarth','Conquest','Jeep','Meserati','Tesla','Lexus','Chevrolet']


# In[14]:


counter = 0
for u in urls:
    soup = set_url_parse(u)
    name_box = soup.find_all('a',attrs={'class': "modeltext"})
    cars=[]
    for i in name_box:
        cars.append(i.get('href'))
    car_names=[] 
    for i in name_box:
        car_names.append(i.get('title'))
    for car_url in range(len(cars)):
        print("For car: ", car_names[car_url])
        data1 = []
        data1.append(car_names[car_url])
        #for every car
        soup = set_url_parse(cars[car_url])
        #find price of every car
        price = soup.find('div',attrs={'class': "priceleft"})
        string = price.find('div').text
        find = re.search('[-+]?([0-9]*\.[0-9]+|[0-9]+) - [-+]?([0-9]*\.[0-9]+|[0-9]+)',string)
        data1.append(find.group(0))    
        prices_df= pd.concat([prices_df,pd.DataFrame(data1).T],axis=0)
        href_reviews = soup.find('a',attrs={'class':'viewallbnt'})
        url = href_reviews.get('href')
        soup = set_url_parse(url)
        all_rev_href = soup.find_all('span',attrs={'class':'rvewdetailheading'})
        for i in all_rev_href:
            data = []
            data.append(brands[counter])
            data.append(car_names[car_url])
            l = i.find('a')
            url = l.get('href')
            soup = set_url_parse(url)
            tmp = soup.find('h1',attrs={'itemprop':'name'})
            heading = tmp.text
            data.append(heading)
            tmp = soup.find('div',attrs={'itemprop':'reviewBody'})
            data.append(tmp.text)
            tmp = soup.find_all('span',attrs={'class':'starorange'})
            data.append(len(tmp))
            reviews_df = pd.concat([reviews_df,pd.DataFrame(data).T],axis=0)
        counter = counter + 1


# In[15]:


reviews_df.columns = ['Brand','Name','Heading','Description','Rating']
prices_df.columns = ['Car_name','Price']


# In[16]:


print(len(reviews_df))


# In[17]:


print(len(prices_df))


# In[19]:


with open('mypickle.pickle', 'wb') as f:
    pickle.dump(reviews_df, f)

