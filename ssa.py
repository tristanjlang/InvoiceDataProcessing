'''
Set of historical credit account payment data from Company XYZ, a B2B retailer of auto parts

Company XYZ suffered from chronically high DSO (Days Sales Outstanding) with many credit customers
***large outstanding balances each month***

==> help understand why this is happening



what patterns & insights do you see that would be useful to Company XYZ,
  ==> in order to minimize risks to payment misses & delays?

What processes would you put in place to:
  ==> deter customers from late payments
  ==> improve customer behavior overall



*****
LOOKING FOR RELATIONSHIPS BETWEEN:
-total size of invoices vs credit score
-total size of invoices vs gdp change in region
-total size of invoices vs unemployment in region
-total size of invoices vs geographic region
-geographic region vs credit score
-total size of invoices vs salesmen/house accounts

OTHER FACTORS:
-market type
-geographic region
-whether accounts with salesmen vs house accounts have better payment histories
-credit score
-gdp change in region
-unemployment in region
*****

'''


import numpy as np
import pandas as pd
import re
import math
import pandasql
import scipy.stats

df = pd.read_csv('data exercise_v2.csv', na_values='#N/A')
df = df.dropna()

cleandf = pd.DataFrame(columns=['Market Type Fleet', 
                                'Market Type Unknown', 
                                'Market Type Service/Repair', 
                                'Market Type Distributor', 
                                'Market Type OED - Truck', 
                                'Market Type Co-Man / Vehicle Builder', 
                                'Region South', 
                                'Region Corporate', 
                                'Region Western', 
                                'Region Northeast', 
                                'Region Midwest', 
                                'Region PDC', 
                                'Average Days to Pay', 
                                'Average Invoice Amount', 
                                'Non Salesman Assigned Accounts?', 
                                'Credit Score', 
                                'GDP % Change (2011-12)', 
                                'Unemployment Average % (2011-12)'])

cleandf['Market Type Fleet'] = df['Market Type Code'] == 'Fleet'
cleandf['Market Type Unknown'] = df['Market Type Code'] == 'Unknown'
cleandf['Market Type Service/Repair'] = df['Market Type Code'] == 'Service/Repair'
cleandf['Market Type Distributor'] = df['Market Type Code'] == 'Distributor'
cleandf['Market Type OED - Truck'] = df['Market Type Code'] == 'OED - Truck'
cleandf['Market Type Co-Man / Vehicle Builder'] = df['Market Type Code'] == 'Co-Man / Vehicle Builder'
cleandf['Region South'] = df['Geographical Region'] == 'SOUTH'
cleandf['Region Corporate'] = df['Geographical Region'] == 'CORPORATE'
cleandf['Region Western'] = df['Geographical Region'] == 'WESTERN'
cleandf['Region Northeast'] = df['Geographical Region'] == 'NORTHEAST'
cleandf['Region Midwest'] = df['Geographical Region'] == 'MIDWEST'
cleandf['Region PDC'] = df['Geographical Region'] == 'PDC'
cleandf['Average Days to Pay'] = sum([df['1/1/2011'], df['2/1/2011'], df['3/1/2011'], df['4/1/2011'], df['5/1/2011'], df['6/1/2011'], df['7/1/2011'], df['8/1/2011'], df['9/1/2011'], df['10/1/2011'], df['11/1/2011'], df['12/1/2011'], df['1/1/2012'], df['2/1/2012'], df['3/1/2012'], df['4/1/2012'], df['5/1/2012'], df['6/1/2012'], df['7/1/2012'], df['8/1/2012'], df['9/1/2012'], df['10/1/2012'], df['11/1/2012'], df['12/1/2012'], df['1/1/2013'], df['2/1/2013'], df['3/1/2013'], df['4/1/2013'], df['5/1/2013'], df['6/1/2013']]) / len(['1/1/2011', '2/1/2011', '3/1/2011', '4/1/2011', '5/1/2011', '6/1/2011', '7/1/2011', '8/1/2011', '9/1/2011', '10/1/2011', '11/1/2011', '12/1/2011', '1/1/2012', '2/1/2012', '3/1/2012', '4/1/2012', '5/1/2012', '6/1/2012', '7/1/2012', '8/1/2012', '9/1/2012', '10/1/2012', '11/1/2012', '12/1/2012', '1/1/2013', '2/1/2013', '3/1/2013', '4/1/2013', '5/1/2013', '6/1/2013'])
cleandf['Average Invoice Amount'] = df['Average Invoice Amount'].map(lambda x: float(''.join(re.findall(r'[0-9.]+', x)) if ''.join(re.findall(r'[0-9.]+', x)) != '' else 0))
cleandf['Non Salesman Assigned Accounts?'] = df['Non Salesman Assigned Accounts?'] == 'YES'
cleandf['Credit Score'] = df['Credit Score']
cleandf['GDP % Change (2011-12)'] = df['GDP % Change (2011-12)'].map(lambda x: float(''.join(re.findall(r'[0-9.\-]+', x))) / 100)
cleandf['Unemployment Average % (2011-12)'] =df['Unemployment Average % (2011-12)'].map(lambda x: float(''.join(re.findall(r'[0-9.\-]+', x))) / 100)


#normalize features ==> multiply cleandf values by maxdict values to get the true value
maxdict = {}
maxdict['Average Days to Pay'] = max(cleandf['Average Days to Pay'])
maxdict['Average Invoice Amount'] = max(cleandf['Average Invoice Amount'])
maxdict['Credit Score'] = max(cleandf['Credit Score'])
maxdict['GDP % Change (2011-12)'] = max(cleandf['GDP % Change (2011-12)'])
maxdict['Unemployment Average % (2011-12)'] = max(cleandf['Unemployment Average % (2011-12)'])

cleandf['Average Days to Pay'] = cleandf['Average Days to Pay'] / maxdict['Average Days to Pay']
cleandf['Average Invoice Amount'] = cleandf['Average Invoice Amount'] / maxdict['Average Invoice Amount']
cleandf['Credit Score'] = cleandf['Credit Score'] / maxdict['Credit Score']
cleandf['GDP % Change (2011-12)'] = cleandf['GDP % Change (2011-12)'] / maxdict['GDP % Change (2011-12)']
cleandf['Unemployment Average % (2011-12)'] = cleandf['Unemployment Average % (2011-12)'] / maxdict['Unemployment Average % (2011-12)']


