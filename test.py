import csv

filepath = open("data/wifi.csv",  encoding='utf-8', mode="r")
data = list(csv.DictReader(filepath))
print(data)