from bs4 import BeautifulSoup
import requests


def get_soup(productLink):
   """Will retrun Soup of given Product Link"""
   response = requests.get(productLink)
   the_page = response.text
   soup = BeautifulSoup(the_page,"html.parser")
   return soup


def get_price(soup):
  """Gets Current price from the soup of entered product"""
  price_divs=soup.select('.nowPrice')
  for price_div in price_divs:
    price_wrapper=price_div.find('b')
    price=price_wrapper.text
    return price


def getDetails(Link):
    """It will take the link then get all the necessary information from the link then return the data in a dictionary"""
    site = Link
    response = requests.get(site)
    the_page = response.text
    soup = BeautifulSoup(the_page,"html.parser")

    #get the cotegory list from the soup
    category_list=get_category(soup)
    #get the main image
    main_image=get_main_image(soup)
    #get side image
    side_images=get_side_images(soup)
    #get Description
    description=get_product_description(soup)
    data={"Main-image":main_image,"Side-image-list":side_images,"Categories":category_list,"Description":description}
    return data

    
def get_category(soup):
  """It takes the soup, gets the cotegories of the products and returns it in a list"""
  selector = soup.select('.t')
  counter=0
  category_list=[]
  for product_category_selector in selector:
    p_c_s_a = product_category_selector.find_all('a')
    if (counter==1):
       break
    else:
       for p_c in (p_c_s_a):
           category_list.append(p_c.text)
           print(p_c.text)
           counter=1
  return category_list


def get_product_description(soup):
  
  """this will take an soup and return desription of the product from the soup"""

  product_intro_selectors = soup.select('.leftBox .desc')
  return product_intro_selectors
#################below commented code will just return text
# for product_intro_selector in product_intro_selectors:
#   product_intro_selector.get_text()


def get_main_image(soup):
  """Takes a soup and returns link of main image from the soup"""
  main_image_link=""
  product_main_image_selectors = soup.select('.thumbShow')
  for product_main_image_selector in product_main_image_selectors:
    main_image_tag=product_main_image_selector.find('img')
    main_image_link=main_image_tag['src']
  return main_image_link


def get_side_images(soup):
  """this will take the soup and return all the side images in a list"""
  side_image_list=[]
  product_side_image_selectors = soup.select('.thumbNav')
  for product_side_image_selector in product_side_image_selectors:
    side_image_tags=product_side_image_selector.find_all('img')
    for side_image_tag in side_image_tags:
      side_image=side_image_tag['src']
      side_image_list.append(side_image)
  return side_image_list
