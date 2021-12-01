#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 16:06:27 2021

@author: dfox
"""
import pandas as pd
import numpy as np
import random
import datetime
import os
import shutil
import math


location = './'

currentdate = datetime.date.today()
currenttime = datetime.datetime.now()

stdf = pd.DataFrame()

for filename in os.listdir(location):
    if filename.startswith("SP_SearchTerm30Days_"): 
        xl = pd.ExcelFile('{}{}'.format(location, filename))
        stdf = stdf.append(xl.parse())

stdf.drop_duplicates()

stdf.sort_values(['Date'], inplace=True)

stdf.reset_index(drop=True, inplace=True)

print(stdf['14 Day Total KENP Read (#)'].sum())
sttsdf = stdf.groupby(by=['Targeting', 'Customer Search Term']).sum()
rows, cols = sttsdf.shape
if rows > 0:
    print([col for col in sttsdf])
    assert '14 Day Total KENP Read (#)' in sttsdf

for index, row in sttsdf.iterrows():
    num_borrows = int(math.ceil(row['14 Day Total KENP Read (#)'] / 580))
    sttsdf.at[index, 'KENP Borrows'] = num_borrows

sttsdf['KENP Borrows'].astype(int)

sttsdf['Total Conversions'] = sttsdf['KENP Borrows'] + sttsdf['14 Day Total Orders (#)']


sttstgtdf = sttsdf.groupby(by='Targeting').sum()
#sttstgtdf.reset_index(inplace=True)
sttscustdf = sttsdf.groupby(by='Customer Search Term').sum()
#sttscustdf.reset_index(inplace=True)

sttstgtdf['Total Conversions'] = sttstgtdf['Total Conversions'].astype(int)
sttscustdf['Total Conversions'] = sttscustdf['Total Conversions'].astype(int)

#filter these on Total Conversions > 0
tcdf = sttstgtdf[sttstgtdf['Total Conversions'] > 0]
ccdf = sttscustdf[sttscustdf['Total Conversions'] > 0]

tkdf = sttstgtdf[sttstgtdf['Clicks'] >= 5]
ckdf = sttscustdf[sttscustdf['Clicks'] >= 5]

tcdf.reset_index(inplace=True)
ccdf.reset_index(inplace=True)
tkdf.reset_index(inplace=True)
ckdf.reset_index(inplace=True)

tcdf = tcdf[['Targeting', 'Total Conversions']]
ccdf = ccdf[['Customer Search Term', 'Total Conversions']]

tkdf = tkdf[['Targeting', 'Clicks']]
ckdf = ckdf[['Customer Search Term', 'Clicks']]

print("\nTargeting:")
print(tcdf)
print(tkdf)

print("\nCustomer Search Term:")
print(ccdf)
print(ckdf)
