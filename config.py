import os

with open(os.path.join("help", "help_general.txt"), "r") as helpFile:
    help = helpFile.read()

app_url = 'https://graph.facebook.com'
app_id = '1137866389628848'
app_secret = 'c0312c20837b4ed24642ccd3f1a2c534'
app_fields_band = 'name,username,about,description,band_members'
app_fields_venue = 'name,username,about,description'
app_fields_events = 'name,place,description,start_time,end_time'

db_password = 'abc123=0'
