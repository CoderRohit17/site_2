from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from decimal import Decimal
from selenium.webdriver.common.keys import Keys

chrome_options = Options()

driver = webdriver.Chrome(r'D:\chromedriver.exe', options=chrome_options)
inside_driver = webdriver.Chrome(r'D:\chromedriver.exe', options=chrome_options)

car_names = []
car_model = []
car_links = []
car_id = []



fvl = "https://www.firstvehicleleasing.co.uk/car-leasing"

driver.get(fvl)

click_more = True

while click_more:
    html = driver.find_element_by_tag_name('html')
    html.send_keys(Keys.END)
    time.sleep(1)
    element = driver.find_element_by_css_selector(".wide-margin-left")
    attr = element.get_attribute("style")
    if attr != "display: none;":
        time.sleep(1)
        try:
            element.click()
        except:
            print("No")

        time.sleep(1)
    else:
        click_more = False
    car_list = driver.find_elements_by_css_selector(".margin-bottom")
    print(len(car_list))

car_list = driver.find_elements_by_css_selector("#variant-grid .margin-bottom")
print(len(car_list))

for item in car_list:
    title = item.find_element_by_css_selector('.product__title').text
    subTitle = item.find_element_by_css_selector('#variant-grid p').text

    car_names.append(title)
    car_model.append(subTitle)
    print(title, ' ( ' + subTitle + ' ) ' )

for i in driver.find_elements_by_xpath("//aside[@class='product__buttons']/a[1]"):
    car_links.append(i.get_attribute('href'))

for i in driver.find_elements_by_xpath('//div[@class="sidebar-layout__main"]/div/div'):
    print(i.get_attribute('id'))
    car_id.append(i.get_attribute('id'))


for links in car_links:
    inside_driver.get(links)
    terms = inside_driver.find_elements_by_xpath('(//div[@class="product-tabs"])[2]/div/div/div/table/tbody/tr/td[1]')
    mileage = inside_driver.find_elements_by_xpath(
        '(//div[@class="product-tabs"])[2]/div/div/div/table/tbody/tr/td[2]')
    monthly = inside_driver.find_elements_by_xpath(
        '(//div[@class="product-tabs"])[2]/div/div/div/table/tbody/tr/td[3]/span')
    initial = inside_driver.find_elements_by_xpath(
        '(//div[@class="product-tabs"])[2]/div/div/div/table/tbody/tr/td[4]/span')

    print(car_id[car_links.index(links)])
    terms1 = []
    mileage1 = []
    monthly1 = []
    initial1 = []
    initialDiv = []
    currency = []
    for i in range(len(terms)):

        terms1.append(terms[i].text[:2])
        mileage1.append((mileage[i].text).replace(',','')[:5])
        monthly1.append((monthly[i].text).replace(',','')[1:])
        initial1.append((initial[i].text).replace(',','')[1:])
        # initialDiv.append(round(Decimal((initial[i].text).replace(',','')[1:])/Decimal((monthly[i].text).replace(',','')[1:])))
        if((monthly[i].text).replace(',','')[:1]=='£'):
            currency.append('Pound')
        if((monthly[i].text).replace(',','')[:1]=='$'):
            currency.append('Dollar')

        print(terms[i].text[:2],
              (mileage[i].text).replace(',','')[:5],
              (monthly[i].text).replace(',','')[1:],
              (initial[i].text).replace(',','')[1:],
              # round(Decimal((initial[i].text).replace(',','')[1:])/Decimal((monthly[i].text).replace(',','')[1:])),
              currency[i]
              )

    data = {'SITE_ID':'2',
            'Car_ID': car_id[car_links.index(links)],
            'TERM': terms1,
            'MILEAGE': mileage1,
            'MONTHLY PRICE': monthly1,
            'INITITAL PRICE': initial1,
            # 'INITITAL': initialDiv,
            'CURRENCY': currency
            }

    df = pd.DataFrame.from_dict(data)

    df.to_csv(car_id[car_links.index(links)]+'.csv')

data = {'Cars': car_names,
        'Variant': car_model,
        'Car ID': car_id}

df = pd.DataFrame.from_dict(data)

df.to_csv('offer_cars_list.csv')

inside_driver.quit()
driver.quit()

