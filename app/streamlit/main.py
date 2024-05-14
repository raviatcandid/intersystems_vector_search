import streamlit as st
from db_operations import verify_table_existence, count_table_records
from combined_code import initialize_database_and_insert_data, generate_response_to_question

st.set_page_config(layout='wide')

def main():
    st.title("Vector Search with LLM in InterSystems IRIS")

    # Check and manage database health status using session state
    st.session_state['health_status'] = verify_table_existence()

    col2_3, col4 = st.columns([3, 9])
    with col2_3:

        if st.session_state['health_status']:
            st.success("Database is healthy")
        else:
            st.error("Database is not healthy")

        uploaded_file = st.file_uploader("Upload a file (.pdf, .txt)", type=['pdf', 'txt'], key='file_uploader')
        if uploaded_file is not None:
            # Process the file only if a new file has been uploaded
            if 'last_uploaded_file' not in st.session_state or uploaded_file.name != st.session_state.get('last_uploaded_file'):
                st.session_state['last_uploaded_file'] = uploaded_file.name
                status = initialize_database_and_insert_data(uploaded_file)
                if status:
                    st.session_state['uploaded_status'] = f"Data is loaded into DB: {count_table_records()} records are in DB"
                else:
                    st.error("Failed to process the document.")
            # Display the status message from the last upload process
            if 'uploaded_status' in st.session_state:
                st.write(st.session_state['uploaded_status'])

    with col4:
        st.markdown("### Ask Questions")
        user_query = st.text_input("Enter your question here", key="query_input")
        if st.button('Submit', key="submit_query"):
            if user_query:
                try:
                    answer, search_results = generate_response_to_question(user_query)
                    st.write(answer)
                    st.markdown("#### Intersystems Vector Search documents:")
                    st.write(search_results)
                except Exception as e:
                    st.error(f"Error processing query: {str(e)}")
            else:
                st.error("Please enter a valid question.")

if __name__ == "__main__":
    main()
