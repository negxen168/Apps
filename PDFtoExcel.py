import streamlit as st
import pandas as pd
import tabula
import io

st.title("PDF to Excel Converter")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    st.info("Extracting tables from PDF. Please wait...")
    # Save the uploaded file to a temporary location
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())
    
    # Extract tables from PDF using tabula
    try:
        tables = tabula.read_pdf("temp.pdf", pages="all", multiple_tables=True)
    except Exception as e:
        st.error(f"Error extracting tables: {e}")
        tables = []
    
    if tables:
        st.success(f"Extracted {len(tables)} table(s) from the PDF.")
        # Show the first table as a preview
        st.write("Preview of the first table:")
        st.dataframe(tables[0])
        
        # Save all tables to an Excel file (each table in a separate sheet)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            for i, table in enumerate(tables):
                table.to_excel(writer, sheet_name=f"Table_{i+1}", index=False)
        output.seek(0)
        
        st.download_button(
            label="Download Excel file",
            data=output,
            file_name="extracted_tables.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("No tables found in the PDF.")

