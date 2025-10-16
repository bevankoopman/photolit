import json
import os

import streamlit as st
from google.cloud import storage
from google.oauth2 import service_account

title = "🎓 Chapel Hill State School Year 6 Graduation Photos 🎓"
st.set_page_config(page_title=title)
st.title(title)
st.write(
    "Upload photos of your child for the Year 6 Graduation slideshow. Please provide 1 to 5 photos in JPG or PNG format.")
st.write("Your photos will be securely stored and only used for the graduation ceremony slideshow.")

key_json = os.getenv("GCP_SERVICE_ACCOUNT_KEY")

if key_json is None:
    st.error("GCP service account key not found. Please contact the administrator.", icon="🚨")
    st.stop()

key_dict = json.loads(key_json)
credentials = service_account.Credentials.from_service_account_info(key_dict)
client = storage.Client(credentials=credentials, project=key_dict["project_id"])
bucket = client.bucket("photolit")

with st.form("form"):
    name = st.text_input("Child's full name")
    uploaded_files = st.file_uploader(
        "Upload 1-5 photos", accept_multiple_files=True, type=["jpg", "jpeg", "png"]
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

            progress_bar = st.progress(0, text=f"Uploading {len(uploaded_files)} photos...")

            for i, uploaded_file in enumerate(uploaded_files):
                bytes_data = uploaded_file.read()
                filename = f"{name.replace(' ', '_')}_{i}_{uploaded_file.type.replace('/', '.')}"
                blob = bucket.blob(filename)
                blob.upload_from_string(bytes_data)
                progress_bar.progress((i + 1) / len(uploaded_files),
                                      text=f"Uploaded {i + 1} of {len(uploaded_files)} photos.")
                columns[i].image(bytes_data, width=300)
            progress_bar.empty()

            st.success(f'Successfully uploaded {len(uploaded_files)} photos. Thanks!', icon="✅")
st.caption("For technical issues, please contact bevan@koopman.id.au.")
