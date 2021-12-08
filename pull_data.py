from bs4 import BeautifulSoup
import requests
import csv
from google.cloud import storage
import pandas as pd


URL = "https://api.covidactnow.org/v2/states.csv?apiKey=bd3dfdfc355042c0996d60494588c092"
response = requests.get(URL)
decoded_content = response.content.decode('utf-8')
cr = csv.reader(decoded_content.splitlines(), delimiter=',')
my_list = list(cr)
df = pd.DataFrame(my_list)
df.to_csv("data.csv", index = False, header=False)
print(df)


"""    
with requests.Session() as s:
    download = s.get(URL)
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    fields = my_list[0]
    rows = my_list[1:]



def upload_blob(bucket_name, source_file_name, destination_blob_name):
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)


# Setting credentials using the downloaded JSON file

client = storage.Client.from_service_account_json(json_credentials_path='credentials-python-storage.json')

# Creating bucket object

bucket = client.get_bucket('py-python')

# Name of the object to be stored in the bucket
object_name_in_gcs_bucket = bucket.blob('my_first_gcs_upload.png')

# Name of the object in local file system
object_name_in_gcs_bucket.upload_from_filename(my_list)


from google.cloud import storage
from google.cloud.storage.bucket import Bucket
client = storage.Client()
bucket = Bucket.from_string("gs://bucket", client=client)

"""