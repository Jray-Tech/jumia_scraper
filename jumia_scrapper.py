from bs4 import BeautifulSoup as sweet_soup
from urllib.request import Request, urlopen
from operator import itemgetter

# because python was using an easily detectable url i ad to use a url with a known browser user agent.
#  FIREFOX 5.0
# opening up connection to grab the page

req = Request('https://www.jumia.com.ng/phones-tablets/', headers={'User-Agent': 'Mozilla/5.0'})

raw_web = urlopen(req)
web_page = raw_web.read()
raw_web.close()
# .products.-mabaya .sku.-gallery.
# parsing html page
page_soup = sweet_soup(web_page, 'html.parser')
product_tag_list = page_soup.find_all('section', {'class':'products -mabaya'})


product_tag = product_tag_list[0]
# getting all the informastion from the items in the products
product_list = product_tag.contents
display_list = []
i = 0
for product in product_list:
    i = i + 1
    try:
        product_name = product.a.h2.text
    except AttributeError:
        product_name = f'CURRENTLY UNAVAILABLE '
    try:
        product_link = product.a['href']
    except TypeError:
        product_link = f'CURRENTLY UNAVAILABLE'
    product_price_raw = product.find('div', {'class':'price-container clearfix'})
    try:
        discount = product_price_raw.span.text
        discount = discount.strip('-')
        discount = discount.rstrip('%')
        try:
            discount = float(discount)
        except ValueError:
            discount = 0.00
        try:
            prod = product_price_raw.find('span', {'class': 'price'})
            pay_price = prod.contents
            pay_price = pay_price[2]
            price_pay = pay_price['data-price']
        except IndexError:
            price_pay = 00000
        try:
            old = product_price_raw.find('span', {'class': 'price -old'})
            price_original_raw = old.contents
            price_original_raw = price_original_raw[2]
            price_original_raw = price_original_raw['data-price']
        except IndexError:
            price_original_raw = 20000
        price_original = price_original_raw.replace(',', '')
        price_original = int(price_original)
    except AttributeError:
        price_original = 20000
        price_pay = 20000
        discount = 0
    if price_original > 20000:
        display_product = {
            'product name': product_name,
            'product link': product_link,
            'product price': price_pay,
            'product discount': discount,
            'product i': i
        }
    display_list.append(display_product)

display_list = sorted(display_list, key=itemgetter('product discount'), reverse=True)
filename = 'new_products_2.csv'
f = open(filename, 'w')
headers = 'product_i, product_price, product_link, product_name, product_discount  \n'
f.write(headers)
for gadget in display_list:
    f.write(f'{gadget["product i"]},{gadget["product price"]}, {gadget["product link"]}, {gadget["product name"]}, {gadget["product discount"]}\n')
f.close()