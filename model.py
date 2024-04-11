import helper_buddy as r
import streamlit as st


st.title("Terms & Condition Reviewer 📝")
st.divider()
apiKey = st.text_input("First, drop your google api key here / generate one from [here](https://aistudio.google.com/app/prompts/new_chat)",type="password")
r.setup_apikey(apiKey)
query = st.text_input("Then, company website or its name")
st.divider()

if(query):
   r.got_query_nowSearch(query) 
     


user_question = st.selectbox("Select any one question from below or type one in the box", options=(None,"What are your terms about data collection?", "Can my account get suspended for no reason?","Any info about your refund policy?","Do you guys sell user data?"))  
st.divider()


   
if "messages" not in st.session_state:
  st.session_state.messages = []


for message in st.session_state.messages:
   with st.chat_message(message["role"]):
       st.markdown(message["content"])

if prompt := st.chat_input("Ask a question to me 😇"):

  
  st.chat_message("user").markdown(prompt)

    # Add user message to chat history
  st.session_state.messages.append({"role": "user", "content": prompt})

  response = r.get_model_response_with_context_for_question(prompt)

  with st.chat_message("assistant"):
      st.markdown(response)

  st.session_state.messages.append({"role": "assistant", "content": response})

else:
   if(user_question):
      st.chat_message("user").markdown(user_question)
      st.session_state.messages.append({"role": "user", "content": user_question})
      response = r.get_model_response_with_context_for_question(user_question)
    # Display assistant response in chat message container
      with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
      st.session_state.messages.append({"role": "assistant", "content": response})