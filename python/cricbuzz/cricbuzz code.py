#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from selenium import webdriver
import time


# ### Cricbuzz [Batting,Bowling,All Rounders,Teams]

# In[3]:


import pandas as pd
from selenium import webdriver
driverPath=r"C:\Users\Merit\Desktop\ss\chromedriver.exe"
driver = webdriver.Chrome(executable_path=driverPath)
driver.get("https://www.cricbuzz.com/cricket-stats/icc-rankings/men/batting")
batting=["tests","odis","t20s"]
table=["batsmen","bowlers","all-rounders","teams"]
for j in table:
    writer = pd.ExcelWriter(r'C:\Users\Merit\Desktop\cricket'+'\\' +j+ '.xlsx', engine='xlsxwriter')
    for i in batting:
        driver.find_element_by_xpath("//a[@id='"+j+"-tab']").click()
        if j == "all-rounders":
           
            driver.find_element_by_xpath("//a[@id='allrounders-"+i+"-tab']").click()
            data=driver.find_elements_by_xpath("//a[@id='allrounders-"+i+"-tab']//following::div[contains(@class,'cb-col cb-col-100 cb-font-14 cb-lst-itm text-center')]")
        else:
            driver.find_element_by_xpath("//a[@id='"+j+"-"+i+"-tab']").click()
            data=driver.find_elements_by_xpath("//a[@id='"+j+"-"+i+"-tab']//following::div[contains(@class,'cb-col cb-col-100 cb-font-14 cb-lst-itm text-center')]")
        nwlst=[]
        for dt in data:
            nwlst.append(dt.text.split("\n"))
        df=pd.DataFrame(nwlst,columns=["position","nan","players","country","rating"])
        df.dropna(inplace=True)
        df.drop(["nan"],axis=1,inplace=True)
        df.to_excel(writer, sheet_name=i, index=False)
        df.drop(df.index, inplace=True)
        df.reset_index( inplace=True)
        if j == "teams":
            driver.find_element_by_xpath("//a[@id='"+j+"-"+i+"-tab']").click()
            data=driver.find_elements_by_xpath("//a[@id='"+j+"-"+i+"-tab']//following::div[contains(@class,'cb-col cb-col-100 cb-font-14 cb-brdr-thin-btm text-center')]")
            nwlst=[]
            for dt in data:
                nwlst.append(dt.text.split("\n"))
            df1=pd.DataFrame(nwlst,columns=["position","team","rating","points"])
            df1.dropna(inplace=True)
            df1.to_excel(writer, sheet_name=i, index=False)
            df1.drop(df1.index, inplace=True)
            df1.reset_index( inplace=True)
    writer.save()
    writer.close()
driver.close()


# #### Cricbuzz Teams images 

# In[8]:


path=r"C:\Users\Merit\Desktop\ss\chromedriver.exe"
driver=webdriver.Chrome(executable_path=path)
driver.get("https://www.cricbuzz.com/cricket-team")
driver.find_element_by_xpath("//div[@id='teamDropDown']").click()
time.sleep(1)
image=driver.find_elements_by_xpath("//a[contains(text(),'International')]//following::a[contains(@class,'cb-teams-flag-img')]")
country = driver.find_elements_by_xpath("//a[contains(text(),'International')]//following::h2")
ListOfCountry = []
for i in country:
    ListOfCountry.append(i.text)
for i,j in zip(ListOfCountry,image):
    with open(r"C:\Users\Merit\Desktop\cricket\images"+"\\" +i+ ".png",'wb') as file:
        file.write(j.screenshot_as_png)
                
driver.close()


# ### State wise Company Details

# In[ ]:


path=r"C:\Users\Merit\Desktop\ss\chromedriver.exe"
writer = pd.ExcelWriter(r'C:\Users\Merit\Desktop\agila\eme.xlsx', engine='xlsxwriter')
driver=webdriver.Chrome(executable_path=path)
driver.maximize_window()
driver.get("https://ai.fmcsa.dot.gov/hhg/Search.asp?ads=a")
st=driver.find_elements_by_xpath("//label[contains(text(),'State :')]//following::option")
states=[]
for i in st:
    states.append(i.text)
for j in states[1:98]:
    stt=driver.find_element_by_xpath("//option[contains(text(),'"+j+"')]")
    stt.click()
    driver.find_element_by_xpath("//option[contains(text(),'Please select state')]//following::input[1]").click()
    time.sleep(1)
    TableID = driver.find_element_by_xpath("//h2[contains(text(),'Search Results')]//following::table[4]")
    AllRows = TableID.find_elements_by_tag_name("tr")
    headers = ["Company Name","Headquarters Location","Company Type","Fleet Size"]
    columns = dict()
    for h1 in headers:
        columns[h1] = []
    for rw in AllRows[1:]:
        data = rw.find_elements_by_tag_name("td")
        for name, item in zip(headers,data):
            value = item.text
            columns[name].append(value)
    df = pd.DataFrame.from_dict(columns, orient='index')
    df = df.transpose()
    df.drop(df.tail(1).index,inplace=True)
    print(df)
    df.to_excel(writer, sheet_name=j, index=False)
    df.drop(df.index, inplace=True)
    df.reset_index( inplace=True)
    driver.back()
writer.save()
writer.close()
driver.close()

