from bs4 import BeautifulSoup
import requests


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

    url = f'https://www.cvbankas.lt/{work_area}{location}{keyword_search}'
    list_of_ads = []
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


def cv_lt(city='kaunas', keyword_search=''):
    city = {
        'kaunas': 1020,
        'vilnius': 1010,
        'klaipeda': 1030,
        'alytus': 1070,
        'birstonas': 1090,
        'jonava': 1150

    }
    city = 'kaunas'
    url = f"https://www.cv.lt/nuolatinis-darbas?cities={city}&texts={keyword_search}"
    source = requests.get(url)
    list_of_ads = []
    soup = BeautifulSoup(source.content, 'html.parser')
    full_card = soup.find_all('a', class_='job-wr')
    for card in full_card:
        try:
            logo = f"https://www.cv.lt{card.find('div', class_='img-wr').find('img').get('src')}"
        except AttributeError:
            logo = 'No logo declared'

        try:
            position = card.find('div', class_='info-wr').find('button').text
        except AttributeError:
            position = 'No position declared'

        try:
            employer = card.find('div', class_='img-wr').find('img').get('alt')
        except AttributeError:
            employer = 'No employer declared'

        try:
            salary = card.find('div', class_='info-wr').find('span', class_='salary').text
        except AttributeError:
            salary = 'No salary declared'

        try:
            location = card.find('div', class_='info-wr').find('span', class_='company').find('span').text
        except AttributeError:
            location = 'No location declared'

        try:
            how_old_ad = card.find('div', class_='time').find('span').text
        except AttributeError:
            how_old_ad = 'No age declared'

        try:
            ad_link = f"https://www.cv.lt{card.get('href')}"
        except AttributeError:
            ad_link = 'No link declared'

        card_items = {
            'logo': logo,
            'position': position,
            'employer': employer,
            'salary': salary,
            'salary_taxes': 'Neatskaičius mokesčių',
            'location': location,
            'how_old_ad': how_old_ad,
            'ad_link': ad_link
        }
        list_of_ads.append(card_items)
    return list_of_ads


for i in cvbankas_lt(work=''):
    print(i['position'])
