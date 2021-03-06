# Import, pay yer tariffs!
import pypyodbc
import requests
import json
from pprint import pprint
from Google_API_PyQuest import api_request

# Global Variables
url = "https://maps.googleapis.com/maps/api/place/autocomplete"
data_type = "/json"
input_type = "?input="
API_Key = api_request()

# Opening Connection
print("< Opening Connection >")

connection = pypyodbc.connect(r'Driver={SQL Server};'
                              r'Server=SCFSQL01;'
                              r'Database=SummarizedReportData;'
                              r'Trusted_Connection=yes;')

print("\n")

# Show connection info
print("< Connection Information>")								
print(connection)								
print("\n")

# Query info
cursor = connection.cursor()
SQLCommand = ("""
    SELECT TOP 10
        PERSON_SK
    ,	ADDRESS_LINE_1
    ,	CITY
    ,	STATE
    ,	POSTAL_CODE = LEFT(Postal_Code, 5)
    FROM
	SummarizedReportData.dbo.CUST_PT_PIV_Demgraf
    ;
    """)
Values = [2]
cursor.execute(SQLCommand)#, Values)
results = cursor.fetchone()

# Print query results
print("< Query Results >")
while results:
    col_person_sk = str(results[0])
    col_address_1 = str(results[1])
    col_city = str(results[2])
    col_state = str(results[3])
    col_zip = str(results[4])
    address_list = [col_address_1, col_city, col_state, col_zip]
    space = " "
    col_full_address = space.join(address_list).replace("None", "").replace("  ", " ")

    API_URL = url + data_type + input_type + col_full_address + "&types=address"  + "&key=" + API_Key
    
    print("Person_SK: ", col_person_sk, " Address: ", col_full_address)
    print(API_URL)
    r = requests.get(API_URL, verify = False)

    r_json = r.json()
    try:
            print("\n")
            print("\t" + r_json['predictions'][0]['description'])
            print("\n")
    except IndexError:
            print("\n")
            print("I'm sorry, that search doesn't match any records!")
            print("\n")
    results = cursor.fetchone()
print("\n")
	
# Close connection
print("< Closing Connection >")
connection.close()
print("\n")
