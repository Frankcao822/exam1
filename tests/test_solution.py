import os
import csv
import random
import pytest
import pandas as pd
from copy import deepcopy
from solution import *

random.seed(10)

def remove_blank_loc(data):
  result = list()
  for record in data:
    if record['nta'] == "" or record['nta_code'] == "":
      pass
    else:
      result.append(record)
  return result

def remove_outside_range(data, lat_range, lng_range):
  result = list()
  for record in data:
    if lat_range[0] <= float(record['latitude']) <= lat_range[1] and lng_range[0] <= float(record['longitude']) <= lng_range[1]:
      result.append(record)
  return result

# def make_default(data):
#   result = list()
#   for record in data:
#     if 

wifi_data_filepath = os.path.join(os.getcwd(), "data/wifi.csv")
exp_wifi_df = pd.read_csv(wifi_data_filepath)

exp_wifi_data = list(csv.DictReader(open(wifi_data_filepath, "r")))

exp_wifi_data_no_blanks = remove_blank_loc(deepcopy(exp_wifi_data))
exp_wifi_df_no_blanks = pd.DataFrame(exp_wifi_data_no_blanks)

exp_wifi_data_within_range = remove_outside_range(deepcopy(exp_wifi_data_no_blanks), (40.5095311, 40.9037228), (-74.244107, -73.714838))
exp_wifi_df_within_range = pd.DataFrame(exp_wifi_data_within_range)

# exp_wifi_data_defaulted = 


class Tests:
  def test_get_csv_data_shape(self):
    actual_wifi_data = get_csv_data(wifi_data_filepath)
    assert actual_wifi_data != None
    assert len(actual_wifi_data) == exp_wifi_df.shape[0]
    assert all([len(x) == exp_wifi_df.shape[1] for x in actual_wifi_data])

  def test_remove_rows_with_blank_neighborhood_fields(self):
    returned_data = remove_rows_with_blank_neighborhood_fields(deepcopy(exp_wifi_data))
    assert returned_data != None
    assert len(returned_data) == exp_wifi_df_no_blanks.shape[0]
    assert all([len(x) == exp_wifi_df_no_blanks.shape[1] for x in returned_data])

  def test_remove_out_of_range_entries(self):
    returned_data = remove_out_of_range_entries(deepcopy(exp_wifi_data_no_blanks), (40.5095311, 40.9037228), (-74.244107, -73.714838))
    assert returned_data != None
    assert len(returned_data) == exp_wifi_df_within_range.shape[0]
    assert all([len(x) == exp_wifi_df_within_range.shape[1] for x in returned_data])
    assert all([40.5095311 <= float(x['latitude']) <= 40.9037228 and -74.244107 <= float(x['longitude']) <= -73.714838 for x in returned_data])

  def test_make_type_free_default(self):
    returned_data = make_type_free_default(deepcopy(exp_wifi_data))