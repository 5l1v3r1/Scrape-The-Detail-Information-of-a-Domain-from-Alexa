
#Alexa-Details-of-Domain-Scrape
#by github.com/msklc
from bs4 import BeautifulSoup
from pandas import ExcelWriter
import requests
import pandas as pd
import datetime
q_time=datetime.datetime.now().strftime('%d-%m-%Y')
domain_name='haberler.com'
url = "https://www.alexa.com/siteinfo/{}".format(domain_name)
request = requests.get(url)
soup = BeautifulSoup(request.content,'lxml')

def Ranks():
    local_ranks=[]    
    global_rank = soup.find('p', {'class':'big data'}).text.strip()
    global_rank = global_rank.replace("#", "").strip()
    global df_rank
    df_rank=pd.DataFrame(global_rank,columns =["Rank({})".format(q_time)],index=['GLOBAL'])
    local_rank=soup.find('div',{'id':"countrydropdown"})
    for row in local_rank.select('li'):
        local_ranks.append(row.text.strip()) if row.text.strip() !='Sign up  for all  National Ranks' else None
    local_ranks = [s.split('#') for s in local_ranks]
    df_local=pd.DataFrame(local_ranks,columns =['',"Rank({})".format(q_time)])
    df_local.set_index('', inplace=True)    
    df_rank = df_rank.append(df_local)
    print('Ranks are scraped')
    TopKeywords()

def TopKeywords():
    topkeywords = soup.find("div", { "id" : "card_mini_topkw"})
    topkeyword_list = [keyword.text.strip() for keyword in topkeywords.find_all("span", { "class" : "truncation" })]
    group_keyword_list = [topkeyword_list[x:x+3] for x in range(0, len(topkeyword_list), 3)]
    global df_keyword
    df_keyword=pd.DataFrame(group_keyword_list,columns =['Top Keywords','Search Traffic','Share of Voice'])
    print('TopKeywords are scraped')
    SiteMetrics()
    
def SiteMetrics():
    metrics = soup.find("section", { "class" : "engagement"})
    d_pageview = [keyword.text.strip() for keyword in metrics.find_all('p',{'class':'small data'})]
    d_pageview  = [s.split(' ') for s in d_pageview ]
    global df_metrics
    df_metrics=pd.DataFrame(d_pageview,columns =['Value','Changing'],
                            index=['Daily pageviews per visitor',
                                   'Average time in minutes and seconds that a visitor spends',
                                   'Percentage of visits to the site that consist of a single pageview'])
    df_metrics.drop(df_metrics.columns[1:2],axis=1, inplace=True)
    print('SiteMetrics are scraped')
    SaveXLS()
    
def SaveXLS(): #Save XLSX
    writer = pd.ExcelWriter('Alexa_{}_{}.xlsx'.format(domain_name ,datetime.datetime.now().strftime('%d.%m.%Y_%H.%M'), engine = 'xlsxwriter'))
    df_rank.to_excel(writer, sheet_name = 'Ranks')
    df_keyword.to_excel(writer, sheet_name = 'TopKeywords')
    df_metrics.to_excel (writer, sheet_name = 'SiteMetrics')
    writer.save()
    writer.close()
    print('The results are saved to .XLSX file')
Ranks()