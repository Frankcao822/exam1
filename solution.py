# write your Python code here according to the instructions written in the instructions

## import the csv module
import csv
import struct

def get_csv_data(filepath):
    """
    Opens the file at filepath, reads the data using the csv module's DictReader, 
    converts that data to a regular list and returns that list.

    :param filepath: The file path of the CSV data file to open
    :returns: A list of dictionaries, where each dictionary represents one row from the file
    """
    filepath = open("data/wifi.csv",  encoding='utf-8', mode="r")
    data = list(csv.DictReader(filepath))
    return data
    
def remove_rows_with_blank_neighborhood_fields(data):
    """
    Removes any rows with blank 'nta' or 'nta_code' fields from the data set

    :param data: The data, as a list of dictionaries
    :returns: The modified data, as a list of dictionaries
    """
    ## place your code here to complete this method according to the instructions above
    data1=[]
    count=0
    for i in data:
        if bool(i['nta']) == False:
            count+=1
            continue
        elif bool(i['nta_code']) == False:
            count+=1
            continue
        else:
            data1.append(i)
    data=data1
    #print(data)
    return data
def remove_out_of_range_entries(data, lat_range, lng_range):
    """
    Removes any entries which has latitude and longitude values out of range.
    
    :param data: The data, as a list of dictionaries
    :param lat_range: tuple (Float, Float) representing the permissable range of latitude values
    :param long_range: tuple (Float, Float) representing the permissable range of longitude values
    :returns: The modified data, as a list of dictionaries
    """
    ## place your code here to complete this method according to the instructions above
    data2=[]
    count=0
    #print(lat_range[1])
    #print(len(data))
    #a = struct.unpack(lat_range[0],lat_range[1])
    #print(40.75 in float(lat_range))
    for i in data:
        if lat_range[0]< float(i['latitude']) < lat_range[1] and lng_range[0] < float(i['longitude']) < lng_range[1]:
            #print(i['latitude'])
            count+=1
            continue
        else:
            data2.append(i)
            
    data=data2
    #print(count)
    return data
    
def make_type_free_default(data):
    """
    Makes 'Free' as the default 'type'. Any entries with empty values of 'type' are set to 'Free'.

    :param data: The data, as a list of dictionaries
    :returns: The modified data as a list of dictionaries
    """
    ## place your code here to complete this method according to the instructions above
    data1=[]
    for i in data:
        if i['type']=='':
            i['type']='Free'
        data1.append(i)
    data=data1
    return data
def remove_non_free_rows(data):
    """
    Removes any rows with anything other than 'Free' in the 'type' field.

    :param data: The data, as a list of dictionaries
    :returns: The modified data, as a list of dictionaries
    """
    ## place your code here to complete this method according to the instructions above
    data1=[]
    for i in data:
        if i['type']=='Free':
            data1.append(i)
    data=data1
    return data

def make_location_title_case(data):
    """
    Puts the data in the 'location' field into Title Case, where the first letter of each word is capitalized.

    :param data: The data, as a list of dictionaries
    :returns: The modified data, as a list of dictionaries
    """
    ## place your code here to complete this method according to the instructions above
    data1=[]
    for i in data:
        m=i['location']
        n=[]
        a=0
        for j in range(len(m)):
            if j==0:
                n.append(m[j].upper())
            else:
                
                n.append(m[j].lower())

        m ="".join(n)
        i['location']=m
        data1.append(i)
    data=data1
    return data
def fix_provider(data, old_provider, new_provider):
    """
    Swaps out the old provider name with the updated new provider name for any rows that match.

    :param data: The data, as a list of dictionaries
    :param old_provider: The old provider name to remove, e.g. 'SpotOnNetworks'
    :param new_provider: The new domain to replace the old_domain with, e.g. 'Spot On Networks'
    :returns: The modified data, as a list of dictionaries
    """
    ## place your code here to complete this method according to the instructions above
    data1=[]
    for i in data:
        if i['provider']==old_provider:
            i['provider']=new_provider
        data1.append(i)
    data=data1
    return data
def save_csv_data(data, filepath):
    """
    Saves the data into the specified file.  Include the field headers as the first row.

    :param data: The data, as a list of dictionaries
    :param filepath: The file path of the CSV data file to save to
    """
    ## place your code here to complete this method according to the instructions above
    a=list(data[0].keys())
    with open(filepath, 'w', newline='',encoding='utf-8') as b:
        writer = csv.DictWriter(b,fieldnames=a)
        writer.writeheader()
        writer.writerows(data)
def get_number_free_hotspots(filepath, neighborhood):
    """
    Calculates the average cost per impression of all records in the data set.

    :param filepath: The file path of the CSV data file to open
    :param neighborhood: The neighborhood within which to count free wifi hotspots
    :returns: The number of free wifi hotspots within the indicated neighborhood
    """
    ## place your code here to complete this method according to the instructions above
    data=get_csv_data(filepath)
    count=0
    for i in data:
        if i['nta']==neighborhood:
            if i['type']=='Free':
                count+=1
    return count

#################################################
## Do not modify the code below this line      ##
## except to comment out any function calls    ##
## that you do not wish to test at the moment  ##
#################################################

def main():
    ## use the functions defined above to complete munging of the data file

    # get the data from the file
    data = get_csv_data('data/wifi.csv')
    
    # munge it
    data = remove_rows_with_blank_neighborhood_fields(data)
    data = remove_out_of_range_entries(data, (40.5095311, 40.9037228), (-74.244107, -73.714838))
    data = make_type_free_default(data)
    data = remove_non_free_rows(data)
    data = make_location_title_case(data)
    data = fix_provider(data, 'SpotOnNetworks', 'Spot On Networks')

    # save to the new csv file
    save_csv_data(data, 'data/wifi_clean.csv')

    # print the average cost per impression from the data in the file
    num = get_number_free_hotspots('data/wifi_clean.csv', 'Fort Greene')
    print('There are ' + str(num) + ' free Wi-Fi hotspots in Fort Greene, Brooklyn.') 

if __name__ == "__main__":
    main()
