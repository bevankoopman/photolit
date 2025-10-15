import os
import dropbox
import streamlit as st

from io import BytesIO

title = "Chapel Hill State School Year 6 Graduation Photos 🎓"
st.set_page_config(page_title=title, layout="wide")
st.title(title)
st.write("Upload photos of your child for the Year 6 Graduation slideshow. Please upload between 1 to 5 photos in JPG or PNG format.")
st.write("Your photos will be securely stored and only used for the graduation ceremony slideshow.")

# Initialize Dropbox client with your access token
ACCESS_TOKEN = os.environ.get("DROPBOX_ACCESS_TOKEN")  # safer to store in env vars
APP_KEY = os.environ.get("DROPBOX_APP_KEY")
dbx = dropbox.Dropbox(ACCESS_TOKEN, app_key=APP_KEY)


col1, col2 = st.columns(2)
with col1.form("form"):

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
                dbx.files_upload(bytes_data, f'/{filename}', mode=dropbox.files.WriteMode("overwrite"))
                progress_bar.progress((i + 1) / len(uploaded_files), text=f"Uploaded {i + 1} of {len(uploaded_files)} photos.")
                columns[i].image(bytes_data, width=300)
            progress_bar.empty()

            st.success(f'Successfully uploaded {len(uploaded_files)} photos.', icon="✅")
