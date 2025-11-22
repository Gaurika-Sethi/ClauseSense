import streamlit as st
import os
from main import run as run_pipeline
from PIL import Image
import io

logo = Image.open("logo.jpg")

st.markdown("""
    <style>
        .stApp {
            background-color: #201c3d; 
        }
        [data-testid="stSidebar"] {
            background-color: #e6ecff;
        }
    </style>
""", unsafe_allow_html=True)


st.set_page_config(
    page_title="ClauseSense AI",
    layout="wide",
    page_icon=logo,  # ← your custom icon
)

# Display custom header with logo + title
col1, col2 = st.columns([1, 9])
with col1:
    st.image(logo, width=100)   # adjust size as needed
with col2:
    st.markdown("""
        <h1 style='margin-top:5px; margin-left:-15px;'>
            ClauseSense AI – Compliance Analyzer
        </h1>
    """, unsafe_allow_html=True)


st.write("Upload a document and policy file to generate a full compliance report.")

# ---------------------------
# Upload Section
# ---------------------------
uploaded_doc = st.file_uploader("Upload Document", type=["txt", "pdf"])
uploaded_policy = st.file_uploader("Upload Policy File", type=["txt"])

def save_file(upload, filename):
    with open(filename, "wb") as f:
        f.write(upload.getbuffer())
    return filename

if st.button("🚀 Run Compliance Analysis"):

    if not uploaded_doc or not uploaded_policy:
        st.error("Please upload both files.")
        st.stop()

    # Save both files
    doc_path = save_file(uploaded_doc, "temp_doc.txt")
    policy_path = save_file(uploaded_policy, "sample_policy.txt")

    st.info("Running ClauseSense… please wait.")

    # Run pipeline
    output_state = run_pipeline(doc_path)

    st.success("Analysis complete!")


    # -------------------------------------------------------------------
    # SHOW ONLY FINAL REPORT TEXT
    # -------------------------------------------------------------------
    st.header("📘 Final Compliance Report")
    final_text = output_state.get("final_report_text", "No report available.")
    st.code(final_text, language="text")


    # -------------------------------------------------------------------
    # DOWNLOAD BUTTONS
    # -------------------------------------------------------------------
    st.header("⬇️ Download Reports")

    col1, col2 = st.columns(2)

    with col1:
        if os.path.exists("final_report.txt"):
            with open("final_report.txt", "rb") as f:
                st.download_button(
                    label="Download TXT Report",
                    data=f,
                    file_name="ClauseSense_Report.txt",
                    mime="text/plain"
                )

    with col2:
        if os.path.exists("final_report.json"):
            with open("final_report.json", "rb") as f:
                st.download_button(
                    label="Download JSON Report",
                    data=f,
                    file_name="ClauseSense_Report.json",
                    mime="application/json"
                )
