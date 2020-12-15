'''webscrapping script for DE role'''
from bs4 import BeautifulSoup as bs
import requests
import csv


macrosection = "https://app.hedgeye.com/insights/all?type=macro"
homepage = "https://app.hedgeye.com"

#webpage parser
def parser(target_url):
    url = requests.get(target_url)
    parsed_url = bs(url.text, 'html.parser')
    return parsed_url


#collecting the hyperlinks for each macro in the latest marco section
macrosection_parsed = parser(macrosection)
macros_location = macrosection_parsed.find('div', class_='more-thumbnail-articles')
macro_grouping = macros_location.find_all('div', class_='col-sm-4')

latest_macro_href  = (macro.a.get('href') for macro in macro_grouping)

   
#functions for parsing and extracting required information from the latest macro pages
def datetime_published(link):
    return link.find('article').time.text.strip('\n')
    
    
def headline(link):
    return link.find('div', class_='headline-link').text.strip('\n')


def headshot_href(link):
    try:
        headshot = link.find('div', class_='headshot').img.get('src')
        return headshot
    except AttributeError as e:
        return e
            
def fullname(link):
    try:
        fullname = link.find('div', class_='full-name').text.strip('\n')
        return fullname
    except AttributeError as e:
        return e
    
def twitter_handle(link):
    try:
        twitter = link.find('div', class_='twitter-handle').text.strip('\n')
        return twitter
    except AttributeError as e:
        return e

def content_body(link):
    return link.find('article')


#schema for the output
csv_header = ('Datetime Published', 'Headline', 'Author Headshot href', 'Author Fullname', 'Author Twitterhandle', 'Content Body')


#the function that binds all the processes together to give the desired out put
#the output of this script is saved in the current work directory as latest_macros.csv
def final_output(number_of_macro = 6):
    try:
        assert (int(number_of_macro)  > 0)  and (int(number_of_macro) <= 30)
    except:
        print('please enter any number from 1 to 30')
        
    else:
        with open('latest_macros.csv', 'w', newline='\n', encoding = 'utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(csv_header)
            
            counter = 0
                                                        
            for link in latest_macro_href:
                
                if counter < number_of_macro:
                    macropage = homepage + link
                    macropage_parsed = parser(macropage)

                    macro_detail =  list(map(lambda func: func(macropage_parsed), (datetime_published, headline, headshot_href, fullname, twitter_handle, content_body)))
                    writer.writerow(macro_detail)

                    counter += 1

if __name__ == '__main__':
    final_output()