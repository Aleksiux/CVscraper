import requests
from bs4 import BeautifulSoup

PAGE_RANGE = range(1, 20)
# url = f'https://autoplius.lt/skelbimai/naudoti-automobiliai?make_id=59&model_id=24599'
# list_of_ads = []
# source = requests.get(url)
# soup = BeautifulSoup(source.content, 'html.parser')
# full_card = soup.find_all('div',
#                           class_='auto-lists lt')
# print(soup)
# for card in full_card:
#     print(card)
#     card_items = {
#     }
#     list_of_ads.append(card_items)
list_of_ads = []
def cvbankas_lt(city='', keyword='', work=''):
    location_dict = {
        'kaunas': 530,
        'vilnius': 606,
        'klaipeda': 538,
        'alytus': 507,
        'birstonas': 510,
        'jonava': 520,
    }
    work_area_dict = {
        'it': 76,
        'administration': 202,
        'production': 85,
        'medicine': 408,
        'transport_driving': 1047,
    }
    location = ''
    if city != '':
        location = f"&location%5B%5D={location_dict[city]}"

    work_area = '?padalinys%5B%5D=202&padalinys%5B%5D=85&padalinys%5B%5D=76&padalinys%5B%5D=408&padalinys%5B%5D=1047'
    if work != '':
        work_area = f"?padalinys%5B%5D={work_area_dict[work]}"

    keyword_search = ''
    if keyword != '':
        keyword_search = f"&keyw={keyword}"
    for page in PAGE_RANGE:
        url = f'https://www.cvbankas.lt/{work_area}{location}&page={page}'
        if url is None:
            break
        source = requests.get(url)
        soup = BeautifulSoup(source.content, 'html.parser')
        full_card = soup.find_all('article',
                                  class_='list_article list_article_rememberable jobadlist_list_article_rememberable')
        for card in full_card:
            logo = card.find('div', class_='list_logo_c').find('img').get('src')
            position = card.find('h3', class_='list_h3').text
            employer = card.find('span', class_='dib mt5').text
            try:
                salary_amount = card.find('span', class_='salary_amount').text
                salary_period = card.find('span', class_='salary_period').text
                salary = f"{salary_amount} {salary_period}"
            except AttributeError:
                salary = "No salary declared"
            """
            Salary taxes shows if salary is net or gross
            """
            try:
                salary_taxes = card.find('span', class_='salary_calculation').text
            except AttributeError:
                salary_taxes = 'No salary taxes declared'
            location = card.find('span', class_='list_city').text
            try:
                how_old_ad = card.find('span', class_='txt_list_2').text
            except AttributeError:
                how_old_ad = 'end time is not set'
            ad_link = card.find('a', class_='list_a can_visited list_a_has_logo').get('href')
            card_items = {
                'logo': logo,
                'position': position,
                'employer': employer,
                'salary': salary,
                'salary_taxes': salary_taxes,
                'location': location,
                'how_old_ad': how_old_ad,
                'ad_link': ad_link
            }
            list_of_ads.append(card_items)
    return list_of_ads


for i in cvbankas_lt(work='it'):
    print(i)