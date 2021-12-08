import requests
import csv
#from google.cloud import storage
import pandas as pd
import numpy as np



URL = "https://api.covidactnow.org/v2/states.csv?apiKey=bd3dfdfc355042c0996d60494588c092"
historical = "https://api.covidactnow.org/v2/states.timeseries.csv?apiKey=bd3dfdfc355042c0996d60494588c092"

def pull_data(URL):
    response = requests.get(URL)
    decoded_content = response.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    df = pd.DataFrame(my_list)
    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header
    df = df.reset_index(drop = True)
    file_name = "historical.csv"
    if "lastUpdatedDate" in df.columns:
        file_name = str(df["lastUpdatedDate"][0])+".csv"
    df.to_csv(file_name, index = False, header=False)
    return df


cols = ['date', 'country', 'state', 'fips', 'actuals.cases', 'actuals.deaths',
       'actuals.positiveTests', 'actuals.negativeTests',
       'actuals.contactTracers', 'actuals.hospitalBeds.capacity',
       'actuals.hospitalBeds.currentUsageTotal',
       'actuals.hospitalBeds.currentUsageCovid', 
       'actuals.icuBeds.capacity', 'actuals.icuBeds.currentUsageTotal',
       'actuals.icuBeds.currentUsageCovid', 'actuals.newCases',
       'actuals.vaccinesDistributed', 'actuals.vaccinationsInitiated',
       'actuals.vaccinationsCompleted', 'metrics.testPositivityRatio',
        'metrics.caseDensity',
       'metrics.contactTracerCapacityRatio', 'metrics.infectionRate',
       'metrics.infectionRateCI90', 
       'metrics.icuCapacityRatio', 'riskLevels.overall',
       'metrics.vaccinationsInitiatedRatio',
       'metrics.vaccinationsCompletedRatio', 'actuals.newDeaths',
       'actuals.vaccinesAdministered', 'riskLevels.caseDensity',
       'cdcTransmissionLevel']

col_names = ['Date', 'Country', 'State', 'fips', 
        'Number of Cases', 'Number of Deaths',
        'Number of Positive Tests', 'Number of Negative Tests',
        'Contact Tracers', 'Hhospital Beds Capacity',
        'Hospital Beds Current Usage Total',
       'Hospital Beds Current Usage Covid', 
       'ICU Beds Capacity', 'ICU Beds Current Usage Total',
       'ICU Beds Current Usage Covid', 'Number of New Cases',
       'Vaccines Distributed', 'Vaccinations Initiated',
       'Vaccinations Completed', 'Test Positivity Ratio',
        'Case Density',
       'Contact Tracer Capacity Ratio', 'Infection Rate',
       'Infection Rate CI90', 
       'ICU Capacity Ratio', 'Risk Levels Overall',
       'Vaccinations Initiated Ratio',
       'Vaccinations Completed Ratio', 'New Deaths',
       'Vaccines Administered', 'Risk Levels - Case Density',
       'CDC Transmission Level']

def clean_data(historical_data):

    historical_data = historical_data[cols]
    historical_data.columns = col_names
    historical_data = historical_data.replace('', np.nan)

    temp = historical_data.iloc[:, 4:].copy()
    temp = temp.astype(float)
    
    historical_data.iloc[:, 4:] = temp
    return historical_data

##
# """    
# with requests.Session() as s:
#     download = s.get(URL)
#     decoded_content = download.content.decode('utf-8')
#     cr = csv.reader(decoded_content.splitlines(), delimiter=',')
#     my_list = list(cr)
#     fields = my_list[0]
#     rows = my_list[1:]



# def upload_blob(bucket_name, source_file_name, destination_blob_name):
#     # bucket_name = "your-bucket-name"
#     # source_file_name = "local/path/to/file"
#     # destination_blob_name = "storage-object-name"

#     storage_client = storage.Client()
#     bucket = storage_client.bucket(bucket_name)
#     blob = bucket.blob(destination_blob_name)

#     blob.upload_from_filename(source_file_name)


# # Setting credentials using the downloaded JSON file

# client = storage.Client.from_service_account_json(json_credentials_path='credentials-python-storage.json')

# # Creating bucket object

# bucket = client.get_bucket('py-python')

# # Name of the object to be stored in the bucket
# object_name_in_gcs_bucket = bucket.blob('my_first_gcs_upload.png')

# # Name of the object in local file system
# object_name_in_gcs_bucket.upload_from_filename(my_list)


# from google.cloud import storage
# from google.cloud.storage.bucket import Bucket
# client = storage.Client()
# bucket = Bucket.from_string("gs://bucket", client=client)

# """