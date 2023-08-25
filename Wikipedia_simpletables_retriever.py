# In[1]:


# This code retrieves any wikipedia page with a simple format 
# (tables with only 1 headers row) it tries to retrieve tables titles from page 
# so the user can choose which one to save or lets the user save all tables if
# no titles were found.

# import relevant libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import sys


# In[2]:


# define function to print all tables
def retr_all_tables():
    id = 0
    files_saved = 0


    tables = soup.find_all('table')
    print('Retrieving',len(tables),'tables...')

    for table in tables:
        try:
            print('Retrieving table', id+1,'...')
            tab = soup.find_all('table')[id]


            # add title columns to DataFrame
            titles = table.find_all('th')
            table_titles = [title.text.rstrip() for title in titles]
            df = pd.DataFrame(columns = table_titles)

            # Fill data into DataFrame
            column_data = table.find_all('tr')

            for row in column_data[1:]:
                row_data = row.find_all('td')
                individual_row_data = [data.text.rstrip() for data in row_data]

                length = len(df)
                df.loc[length] = individual_row_data

            # look for directory or create new one
            newpath = r'C:\Users\AlanG\OneDrive - Universidad de Guadalajara\Desktop\Tables'
            if not os.path.exists(newpath):
                os.makedirs(newpath)

            # saving file
            csv_name = newpath + '\\table' + str(id + 1) + '.csv'

            try:
                df.to_csv(csv_name, index = False, encoding="latin1") #latin 1 encoding will show better in excel using characters like 'áéíóú'
                ncode = "latin1"
            except:
                df.to_csv(csv_name, index = False, encoding="utf-8")
                ncode = "utf-8"

            print('table' + str(id + 1) + '.csv saved.')

            id += 1
            files_saved += 1
        except:
            print("table", str(id + 1), "couldn't be saved.")
            id += 1
            pass

    print('Completed.')
    print('All', str(files_saved), 'files saved in', newpath)
    quit()


# In[3]:


# Ask for a valid Wikipedia URL
while True:
    try:
        url = input('Insert a Wikipedia URL:')
        if 'wikipedia' not in url and 'https' in url:
            print('Please insert a Wikipedia URL.')
            continue
        page = requests.get(url)
        soup = BeautifulSoup(page.text,'html')
        break
    except:
        print('Please insert a valid URL')
        continue


# In[4]:


print('Trying to retrieve table names...\n')

# try to retrieve table names
table_captions = soup.find_all('caption')
captions = [caption.text.rstrip() for caption in table_captions]

# if table names are not found
if len(captions) == 0:
    tablecount = soup.find_all('table')
    
    print("Couldn't retrieve table names, but",len(tablecount), 'tables were found.')
    print("Do you wish to save all tables?")

    
    while True:
        retrieve_all = input('(Y/N)>')
        retrieve_all = retrieve_all.upper()
        
        if retrieve_all == 'Y':
            retr_all_tables()
            print('Complete.\nExiting program...')
            sys.exit()
        if retrieve_all == 'N':
            print('Exiting program...')
            sys.exit()
        else:
            print('Plase insert a valid option.')
            continue



# In[5]:


# if table names are found
if len(captions) > 0:
    id = 0
    titles_list = list()
    
    print('Please select a table number to retrieve:\n')
    for caption in captions:
        id += 1
        titles_list.append(caption)
        print('[',id,']', caption)
    print('[ 0 ]', 'Retrieve all tables (may retrieve addional tables were no title was found)')
    
# ask for a table number if found
table_number = input('Insert table number:')
table_number = int(table_number)


# In[6]:


if table_number == 0:
    retr_all_tables()

if int(table_number) >= 1:
    try:
        table_number = int(table_number) - 1

        # search for table requested
i        table = soup.find_all('table')[table_number]

        # search for column names and add it to pandas dataframe
        titles = table.find_all('th')
        table_titles = [title.text.rstrip() for title in titles]
        df = pd.DataFrame(columns = table_titles)

        # fill column data into pandas dataframe
        column_data = table.find_all('tr')
        for row in column_data[1:]:
            row_data = row.find_all('td')
            individual_row_data = [data.text.rstrip() for data in row_data]

            length = len(df)
            df.loc[length] = individual_row_data

        # looking for destination folder or creating one if it doesn't exist
        newpath = r'C:\Users\AlanG\OneDrive - Universidad de Guadalajara\Desktop\Tables'
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        # saving file
        csv_name = newpath + '\\'+titles_list[table_number]+'.csv'

        try:
            df.to_csv(csv_name, index = False, encoding="latin1") # latin 1 encoding will show better in excel using characters like 'áéíóú'
            ncode = "latin1"
        except:
            df.to_csv(csv_name, index = False, encoding="utf-8")
            ncode = "utf-8" 

        print('Completed.')
        print('File encoding:', ncode)
        print('File saved in', newpath)
        quit()
    except:
        print("Error. Either table couldn't be retrieved or table selected doesn't exist.")



