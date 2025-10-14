import os
from fileinput import filename

import streamlit as st
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO

title = "Chapel Hill State School Year 6 Graduation Photos 🎓"
st.set_page_config(page_title=title, layout="wide")
st.title(title)
st.write("Upload photos of your child for the Year 6 Graduation slideshow. Please upload between 2 to 5 photos in JPG, PNG, or PDF format.")

# # Create API client.
# credentials = service_account.Credentials.from_service_account_info(
#     st.secrets["gcp_service_account"]
# )
# client = bigquery.Client(credentials=credentials)

# Read service account JSON from environment variable
service_account_info = json.loads(os.environ['GOOGLE_SERVICE_ACCOUNT_JSON'])

# Create credentials
credentials = Credentials.from_service_account_info(
    service_account_info,
    scopes=['https://www.googleapis.com/auth/drive']
)

# Build Drive service
service = build('drive', 'v3', credentials=credentials)
gdrive_folder_id = '13VGmL5rBBaiuUb2DqRajoPlEtdCSd2_c'


col1, col2 = st.columns(2)
with col1.form("form"):

    name = st.text_input("Child's full name")
    uploaded_files = st.file_uploader(
        "Upload 2-5 photos", accept_multiple_files=True, type=["jpg", "jpeg", "png", "pdf"]
    )


    submitted = st.form_submit_button("Submit")
    if submitted:
        if not name:
            st.error("Please enter a name.", icon="⚠️")
        elif not uploaded_files:
            st.error("Please upload at least one photo.", icon="⚠️")
        elif len(uploaded_files) > 5:
            st.error("Please upload no more than 5 photos.", icon="⚠️")
        else:
            columns = st.columns(len(uploaded_files))
            for i, uploaded_file in enumerate(uploaded_files):
                bytes_data = uploaded_file.read()
                filename = f"{name.replace(' ', '_')}_{i}_{uploaded_file.type.replace('/', '.')}"

                # file_metadata = {'name': filename, 'parents': gdrive_folder_id}
                # media = MediaIoBaseUpload(BytesIO(bytes_data), mimetype='application/octet-stream')
                # uploaded_file = service.files().create(body=file_metadata, media_body=media, fields='id', supportsAllDrives=True).execute()

                with open(filename, 'wb') as destination:
                    destination.write(bytes_data)

            columns[i].image(bytes_data, width=300)
            st.success(f'Successfully uploaded {len(uploaded_files)} photos.', icon="✅")
