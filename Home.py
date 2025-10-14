import os
import streamlit as st

title = "Chapel Hill State School Year 6 Graduation Photos 🎓"
st.set_page_config(page_title=title, layout="wide")
st.title(title)

# # Create API client.
# credentials = service_account.Credentials.from_service_account_info(
#     st.secrets["gcp_service_account"]
# )
# client = bigquery.Client(credentials=credentials)

project_id = 'guidestream'

col1, col2 = st.columns(2)
with col1.form("experiment_form"):

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
            os.makedirs("uploaded", exist_ok=True)
            columns = st.columns(len(uploaded_files))
            for i, uploaded_file in enumerate(uploaded_files):
                bytes_data = uploaded_file.read()
                columns[i].image(bytes_data, width=300)

                with open(f"uploaded/{name.replace(" ", "_")}_{i}_{uploaded_file.type.replace("/", ".")}", 'wb') as f:
                    f.write(bytes_data)
            st.success(f'Successfully uploaded {len(uploaded_files)} photos.', icon="✅")
