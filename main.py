
import csv
import pandas as pd
import SoupFunctions as SF
import ExchangeRate as ER


# Exchange rate from dollar to inr

er= ER.get_exchange_rate()
print(er)
rate=er['Rate']
date=er['Date']
inr  = rate
inr= float(inr)



def Convert(dollar):
   """It accepts a dollar value and returns its INR conversion"""
   # print(dollar)
   # print(inr)
   # print(type(dollar))
   # print(type(inr))
   if type(dollar)==str or type(dollar):
      dollar=float(dollar)
   dollar_to_inr=dollar*inr
   return dollar_to_inr

# The Magic
DF = pd.read_excel("ProductList.xls")
totalRows = len(DF.index)

for i in range(0,totalRows):
    productLink = DF._get_value(i,'Product Link')

########## Dropping Unwanted Columns
DF.drop(['Distributor Price','Distributor Ladder Price'],axis=1)
    


print("completed till line :42")


######## converting From Retail Price to INR
Price_fix_Index=[]
for i in range(0,totalRows):
   retailPrice=DF._get_value(i,'Retail Price')
   retailPrice=float(retailPrice)
   if retailPrice==0:
      Price_fix_Index.append(i)
   else:
      inr_conversion=retailPrice*inr
      DF._set_value(i,'Retail Price',inr_conversion)
with open("logs.txt",'w') as logs:
   logs.write(f'Found Retail Price Zero at {Price_fix_Index}\nThe exchange rate was {rate} and update date of exchage rate was{date}')



print("completed till line :57")

#########fixing wrong Retail Price

for price_index in Price_fix_Index:
   product_link=DF._get_value(price_index,'Product Link')
   soup=SF.get_soup(product_link)
   price=SF.get_price(soup)
   data=price
   dat_len=len(data)
   price2=""
   for i in range(0,dat_len):
      if (data[i]=="n" or data[i]=='$') or data[i]=='\\':
         pass
      else:
         price2+=data[i]
   inr_price=Convert(price2)
   DF._set_value(i,'Retail Price',inr_price)



print("completed till line :76")

###################Insert and update Description
DF.insert(2,"Description",'des')

for i in range(0,totalRows):
   print(f"completed {i} items")
   product_link2=DF._get_value(i,'Product Link')
   soup_=SF.get_soup(product_link2)
   description_=SF.get_product_description(soup_)
   #######updating description for product
   DF._set_value(i, 'Description',description_)




print("completed till line :90")

############Update images

############format
# http://exapmle.in/wp-content/uploads/2022/07/grgrrfg.jpg ! alt :  ! title : grgrrfg ! desc :  ! caption :  |

for i in range(0,totalRows):
   product_link_=DF._get_value(i,'Product Link')
   soup_=SF.get_soup(product_link_)
   main_image=SF.get_main_image(soup_)
   side_image_list=SF.get_side_images(soup_)
   image_table_data=""
   boiler_data=" ! alt :  ! title : BinaryLoop Product Image ! desc : Image of BinaryLoop Product ! caption :  |"
   image_table_data+=main_image
   image_table_data+=boiler_data

   for side_image_link in side_image_list:
      image_table_data+=side_image_link
      image_table_data+=boiler_data

print("completed till line :108")

#################add price
for i in range(0,totalRows):
   retailPrice=DF._get_value(i,'Retail Price')
   retailPrice=float(retailPrice)
   brand=DF._get_value(i,'Brand')
   if (brand=='Arduino')or(brand=='Raspberry Pi'):
      retailPrice+=(retailPrice*35)/100
   else:
      retailPrice+=(retailPrice*45)/100
   DF._set_value(i,'Retail Price',retailPrice)





print("completed till line :125")

# create csv file
DF.to_csv("_product.csv")
