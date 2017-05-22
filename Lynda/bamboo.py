# -*- coding: utf-8 -*-
"""
Created on Fri May 19 12:53:50 2017

@author: mbh

649138297351-e2k9tdh39qamvck2ik79s4ktjub0dgoi.apps.googleusercontent.com
LcRrM0AAwHYpCzD5wAxoHwwd
"""

from __future__ import print_function
import httplib2
import os
from pprint import pprint
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import sys
import datetime

#comment out these lines to allow command line arguments to be passed
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Bamboo'

#sensor01 = sys.argv[1]
sensor01 = 123
fmt = '%Y-%m-%d %H:%M:%S'
d = datetime.datetime.now()
d_string = d.strftime(fmt)

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,'sheets.googleapis.com-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials
    
def getValues(range_,spreadsheet_id):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?''version=v4')
    service = discovery.build('sheets', 'v4', http=http,discoveryServiceUrl=discoveryUrl)
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_).execute()
    values = result.get('values', [])
    return values
    
def putValues(data,range_,spreadsheet_id):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?''version=v4')
    service = discovery.build('sheets', 'v4', http=http,discoveryServiceUrl=discoveryUrl)    
    value_input_option = 'USER_ENTERED'  # TODO: Update placeholder value.
    value_range_body = {"values": [data]}
    request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, body=value_range_body)
    response=request.execute()
#    pprint(response)

def Lynda():
    spreadsheet_id = '1dCDB9UnN8Kw22EJ2CUShLCdwkDXdRvDWrGL-B6edwGY'
    detailsTable="'Bamboo details'!BambooDetails"
    values=getValues(detailsTable,spreadsheet_id)
    
#    #baseline EE and EC values
#    row=values[0]
#    selection=[row[0]]
#    EE_base=float(getValues("EC_Balance!embodiedEnergy_kWh",spreadsheet_id)[0][0]) #embodied energy (kWh) 
#    EC_base=float(getValues("EC_Balance!embodiedCarbon_t",spreadsheet_id)[0][0]) #embodied carbon (t)
#    results_base=[float(getValues("EC_Balance!carbonResults",spreadsheet_id)[0][column]) for column in range(4)]
#    print(EE_base,EC_base,results_base)

    row=values[0]
    selection=[row[0]]
    putValues(selection,"'Bamboo details'!Selection",spreadsheet_id)
    results=[float(getValues("EC_Balance!carbonResults",spreadsheet_id)[0][column]) for column in range(4)]
    base_AC=results[2] #base annual emissions
    base_EC=results[3] #base embodied emissions
    rownum=8
    opRange="'Overview'!"+"C"+str(rownum)+":"+"F"+str(rownum)
    putValues(results,opRange,spreadsheet_id)
    opRange="'Overview'!F8"
    putValues([0],opRange,spreadsheet_id)
    lastResults=results    
    rowCount=1
    for row in values[1:]:
        selection=[row[0]]
        putValues(selection,"'Bamboo details'!Selection",spreadsheet_id)
        results=[float(getValues("EC_Balance!carbonResults",spreadsheet_id)[0][column]) for column in range(4)]
        rownum=8+rowCount
        opRange="'Overview'!"+"C"+str(rownum)+":"+"F"+str(rownum)
        putValues(results,opRange,spreadsheet_id)
        opRange="'Overview'!"+"F"+str(rownum)
        putValues([results[3]-base_EC],opRange,spreadsheet_id)
        opRange="'Overview'!"+"G"+str(rownum)
        try:
            carbon_payback=(results[3]-base_EC)/(base_AC-results[2])
        except ZeroDivisionError:
            carbon_payback="N/A"
        putValues([carbon_payback],opRange,spreadsheet_id)
        
        opRange="'Overview'!"+"H"+str(rownum)
        try:
            inc_carbon_payback=(results[3]-lastResults[3])/(lastResults[2]-results[2])
        except ZeroDivisionError:
            carbon_payback="N/A"
        putValues([inc_carbon_payback],opRange,spreadsheet_id)
        lastResults=results
        rowCount+=1

#        HLP=float(getValues("SpaceHeating!HLP",spreadsheet_id)[0][0]) #heat loss parameter
#        SHL=float(getValues("SpaceHeating!SHL",spreadsheet_id)[0][0]) #specific heat load
#        AHD=float(getValues("SpaceHeating!AHD",spreadsheet_id)[0][0]) #annual heat demand
#        NED=float(getValues("Bamboo Electricity!net_electricity_demand",spreadsheet_id)[0][0]) #net electricity demand 
#        AC=float(getValues("EC_Balance!annual_CO2",spreadsheet_id)[0][0]) #annual CO2 t
#        EE=float(getValues("EC_Balance!embodiedEnergy_kWh",spreadsheet_id)[0][0])-EE_base #embodied energy (kWh) 
#        EC=float(getValues("EC_Balance!embodiedCarbon_t",spreadsheet_id)[0][0])-EC_base #embodied carbon (t)


#        print(HLP,SHL,AHD,NED,EE,EC)
        


    
    













    
#def main():
#    """Shows basic usage of the Sheets API.
#
#    Creates a Sheets API service object and prints the names and majors of
#    students in a sample spreadsheet:
#    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
#    """
#    credentials = get_credentials()
#    http = credentials.authorize(httplib2.Http())
#    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
#                    'version=v4')
#    service = discovery.build('sheets', 'v4', http=http,
#                              discoveryServiceUrl=discoveryUrl)
#
#    spreadsheet_id = '1dCDB9UnN8Kw22EJ2CUShLCdwkDXdRvDWrGL-B6edwGY'
#    OPrangeName = 'Bamboo details!Selection'
#    result = service.spreadsheets().values().get(
#        spreadsheetId=spreadsheet_id, range=OPrangeName).execute()
#    values = result.get('values', [])
#
#    if not values:
#        print('No data found.')
#    else:
#        print(values)
#        print('Name, Major:')
##        for row in values:
##            # Print columns A and E, which correspond to indices 0 and 4.
##            print('%s, %s' % (row[0], row[4]))
#
#    range_ = 'Bamboo details!B37:C37'  # TODO: Update placeholder value.
#    value_input_option = 'USER_ENTERED'  # TODO: Update placeholder value.
#    value_range_body = {"values": [[d_string, sensor01]]}
#    request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, body=value_range_body)
#    response = request.execute()
#    pprint(response)
#if __name__ == '__main__':
#    main()
