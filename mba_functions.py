import json
import requests
from bs4 import BeautifulSoup

agent = {"User-Agent":"Mozilla/5.0"}

def usnews_scrape():
    temp_dict = {}
    url_list = [] 

    index_url = 'https://www.usnews.com/education/online-education/mba/search?mode=list&program=mba'
    response = requests.get(index_url, headers=agent)
    soup = BeautifulSoup(response.text, "html.parser")

    div_school_list = soup.find_all("div", 
                class_="padding-top-normal padding-bottom-normal padding-left-normal padding-right-normal")
    #list of divs that capture each school

    for program_block in div_school_list:
        school = program_block.find("h3", class_ = "heading-large block-tighter").find("a").text.strip() #name of school
        state = program_block.find("div", class_= "block-normal text-small").text[-2:] #state located
        rank = program_block.find("div", class_="text-strong").find("div").text.strip()[1:3].strip() #rank on us news
        
        school_url = program_block.find("h3", class_ = "heading-large block-tighter").find("a")["href"]
        url_list.append(school_url)
        response = requests.get(school_url, headers=agent)
        soup = BeautifulSoup(response.text, "html.parser")
        is_tuition = soup.find(attrs={"data-test-id":"G_PT_IN_STATE_TUITION"}).text.strip()[1:] #in state tuition per credit, part-time
        os_tuition = soup.find(attrs={"data-test-id":"G_PT_OUT_STATE_TUITION"}).text.strip()[1:] #out of state tuition per credit, part-time
        is_total = soup.find(attrs={"data-test-id":"STUDENT_FEES_TOTPT_IN_MINUS0_5"}).text.strip()[1:] #in state tuition total, part-time
        os_total = soup.find(attrs={"data-test-id":"STUDENT_FEES_TOTPT_OUT_MINUS0_5"}).text.strip()[1:] #out of state tuition total, part-time
        all_online = soup.find(attrs={"data-test-id":"ONLINE_COMPLETENESS"}).text.strip() #can the program be completed entirely online
            
        temp_dict[school] = {'state':state, 'rank':rank, 'is_tuition':is_tuition, 
                                'os_tuition':os_tuition, 'is_total':is_total, 
                                'os_total':os_total, 'all_online':all_online
                                }
    return temp_dict

usnews_dict = usnews_scrape()

with open('usnews_data.json', 'w') as f: #creates file in C:\PogramFiles(x86)\Notepad++ by default
    json.dump(usnews_dict, f)
