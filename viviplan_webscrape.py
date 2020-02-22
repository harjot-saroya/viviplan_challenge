from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import progressbar
import requests
import time
import csv
import re


def cleaner(word):
    '''
    (str)->str

    This function takes in a raw string that contains html tags and uses 
    regex to clean the string for easier viewing
    '''
    parser = re.compile(r'<.*?>')
    clean1 = parser.sub('', word)
    clean2 = re.sub(r'\r\n', '', clean1)
    clean3 = re.sub(r'\n', '', clean2)
    clean4 = re.sub(r'\xa0', '', clean3)
    clean5 = re.sub(r'   .*?', '', clean4)
    clean6 = re.sub(r'&amp', '', clean5)

    return clean6


# IMPORTANT: Set driver to your computer's chromedriver
driver = webdriver.Chrome('/Users/harjo/Downloads/chromedriver')

# Visit the website and collect text and links to individual profiles
page = requests.get(
    'https://www.wealthprofessional.ca/special-reports/top-50/top-50-advisors-2018/253632')
soup = BeautifulSoup(page.content, 'html.parser')
link1 = soup.findAll("a", {"class": "font1-22-20-20-B js-clamp-2"})
link2 = soup.findAll("a", {"class": "font1-22-20-20-B js-clamp-2"}, href=True)

data = {}
data['Name'] = []
data['Rank'] = []
data['Organization Name'] = []
data['Company'] = []
data['info_link'] = []
data['Description'] = []
data['Location'] = []

# Create progressbar
bar = progressbar.ProgressBar(maxval=50,
                              widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

# Begin webscraping of initial page
print('Collecting company info...')
bar.start()
for i in range(len(link1)):
    bar.update(i+1)

    for x in link1[i]:
        y = x.split(' ')
        rank = y[0]
        name = y[1] + ' ' + y[2]
        data['Rank'].append(rank)
        data['Company'].append(" ".join(y[3:]))
        data['Name'].append(name.replace(',', ''))
bar.finish()

#  Collect links for each person
bar = progressbar.ProgressBar(maxval=50,
                              widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
print('Collecting individual links...')
bar.start()
for i in range(len(link2)):
    bar.update(i+1)
    line = str(link2[i])
    start = line.find('href') + 6
    end = line.find('>')
    data_link = line[start:end-1]
    data['info_link'].append('https://www.wealthprofessional.ca' + data_link)
bar.finish()
bar = progressbar.ProgressBar(maxval=50,
                              widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
count = 0

# Visit each individual site for more details on each wealth professional
print('Visiting individual sites to collect additonal data...')
bar.start()
for link in data['info_link']:
    bar.update(count)
    driver.get(link)
    try:
        webelem = driver.find_element_by_link_text("CONTINUE TO SITE")
        driver.execute_script("arguments[0].click();", webelem)
    except NoSuchElementException:
        time.sleep(1)
    parser = re.compile(r'<.*?>')
    new_link = driver.current_url
    page3 = requests.get(new_link)
    soup3 = BeautifulSoup(page3.content, 'html.parser')
    link3 = soup3.findAll("div", {"class": "wrapper--detail__body"})
    conv = str(link3)
    c2 = conv.split('<br/>')
    # Some edge cases based on the website's page format I discovered
    if c2[2][4:] == '':
        clean = cleaner(c2[2])
        data['Location'].append(clean)
    elif c2[2] == '\\n':
        clean = cleaner(c2[1])
        data['Location'].append(clean)
    elif len(c2[2]) > 30:
        clean = cleaner(c2[2])
        data['Location'].append(clean)
    else:
        clean = cleaner(c2[2])
        data['Location'].append(clean)

    if len(c2) < 5:
        clean = cleaner(c2[2])
        clean2 = cleaner(c2[0])
        clean3 = cleaner(c2[1])
        data['Organization Name'].append(clean2)
        data['Location'][count] = clean3
        if len(clean) < 5:
            clean = cleaner(c2[3])

        data['Description'].append(clean)
    else:
        clean = cleaner(c2[4])
        clean2 = cleaner(c2[1])
        clean3 = cleaner(c2[0])
        data['Organization Name'].append(clean2)
        if len(clean) < 5:
            clean = cleaner(c2[3])
            data['Location'][count] = clean
        data['Description'].append(clean)
    count += 1
bar.finish()
# Write collected data to csv
bar = progressbar.ProgressBar(maxval=50, widgets=[progressbar.Bar(
    '=', '[', ']'), ' ', progressbar.Percentage()])
print('Writing data to csv...')
with open('data.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Name', 'Rank', 'Organization Name',
                         'Location', 'Company', 'Description'])
    bar.start()
    for i in range(len(data['Name'])):
        bar.update(i)
        filewriter.writerow([data['Name'][i], data['Rank'][i], data['Organization Name']
                             [i], data['Location'][i], data['Company'][i], data['Description'][i]])
bar.finish()
