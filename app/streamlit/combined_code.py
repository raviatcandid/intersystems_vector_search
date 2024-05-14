from db_operations import remove_table, insert_table_data, perform_vector_search, create_data_table, count_table_records
from helper import generate_text_embedding, extract_text_from_file, concatenate_vector_results, construct_dataframe
from openai_llm import retrieve_response_from_llm

def initialize_database_and_insert_data(uploaded_file):
    """
    Initializes the database by potentially dropping the existing table, creating a new table, and inserting
    data extracted from the uploaded file.
    """
    print("Attempting to drop existing table: ", remove_table())
    print("Attempting to create a new table: ", create_data_table())
    print("Current records in the table: ", count_table_records())
    
    text = extract_text_from_file(uploaded_file)
    dataframe = construct_dataframe(text)
    insertion_status = insert_table_data(dataframe)
    return insertion_status

def generate_response_to_question(question):
    """
    Generates a response to the given question using the OpenAI Language Learning Model after searching
    for relevant vectors in the database.
    """
    question_embeddings = generate_text_embedding(question)
    search_results = perform_vector_search(question_embeddings)
    combined_context = concatenate_vector_results(search_results)
    response = retrieve_response_from_llm(question, combined_context)
    return response, search_results[:5]
