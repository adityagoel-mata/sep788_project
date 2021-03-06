"""ChatbotProject_Compilation"""

from google.colab import drive
drive.mount('/content/drive')

!cp /content/drive/MyDrive/py_colab_files/csv_Final_Dataset_Compilation.csv .
!cp /content/drive/MyDrive/py_colab_files/chatbotproject_1_topicselection.py .
!cp /content/drive/MyDrive/py_colab_files/chatbotproject_preprocessing_report1.py .
!cp /content/drive/MyDrive/py_colab_files/chatbotproject_finalised_bert.py .

filename = '/content/csv_Final_Dataset_Compilation.csv'
!pip install transformers

import random
import gensim.downloader as api
import chatbotproject_finalised_bert as bert
import chatbotproject_1_topicselection as topic
import chatbotproject_preprocessing_report1 as preprocess

from gensim.models import Word2Vec
model = api.load('word2vec-google-news-300')

#Fetch the wikipedia article

def fetch_article(user_input):
  
  filename_str = str(user_input) + '.txt'
  !cp /content/drive/MyDrive/py_colab_files/Overall_Combined/$filename_str .
  file = open(filename_str,'r', errors='ignore')
  paragraph = file.read()
  
  return paragraph

#Text_Similarity_Score

def text_similarity_score(dataset, question):
  answer = []
  for i in range(len(dataset)):
    text = dataset['Question'][i]
    distance = model.wmdistance(text, question)
    if (distance < 0.2):
      answer.append(str(dataset['Answer'][i]))

  if (len(answer)==0):
    answer_value = ''
  else:
    answer_value = random.choice(answer)

  return answer_value

#Chat Termination Method

def topic_continuation():
  
  response = input("\nDo you want to ask another question based on this topic (Y/N)? ")
  if (response[0] == "Y" or response[0] == "y"):
    response = "Yes"
    return response
  
  elif (response[0] == "N" or response[0] == "n"):
    response = "No"
    return response

def chat_continuation():
  
  response = input("\nOk. Would you like to discuss another topic?(Y/N)? ")
  if (response[0] == "Y" or response[0] == "y"):
    response = "Yes"
    return response
    
  elif (response[0] == "N" or response[0] == "n"):
    response = "No"
    return response

#Main Function

import warnings
warnings.filterwarnings('ignore')

blank = ''
nan = 'nan'
flag_chat = True

while flag_chat:

  print("\nOn which topic would you like to ask your question? Please select the index of the topic. \n")
  
  try:
    user_input = int(input())
  except ValueError:
    print("\nSorry, I am not aware of the input you entered. Either input a number between 0 to 105 or, you may find your answers at https://www.wikipedia.org/")
    continue

  if (user_input < 0 or user_input > 105):
    print("\nInvalid Index. Please enter a number in between 0 and 105 only. Let's start again!")
    continue
  
  dataset = topic.read_dataset(filename, user_input)
  pre_processed_data = preprocess.pre_process(dataset)
  
  flag_topic = True
  while flag_topic:
    print("\nWhat would you like to know on this topic? Please ask your question.")
    question = str(input())
    question = preprocess.pre_process_question(question)
    
    answer = text_similarity_score(dataset, question)
    print(answer)
        
    if (answer == blank or answer == nan):
      paragraph = fetch_article(user_input)
      bert.bert_computation(question, paragraph)
      topic_response = topic_continuation()
      if topic_response == "Yes":
        flag_topic = True
      if topic_response == "No":
        flag_topic = False
        chat_response = chat_continuation()
        if chat_response == "Yes":
          flag_chat = True
        if chat_response == "No":
          flag_chat = False
    
    else:
      topic_response = topic_continuation()
      if topic_response == "Yes":
        flag_topic = True
      if topic_response == "No":
        flag_topic = False
        chat_response = chat_continuation()
        if chat_response == "Yes":
          flag_chat = True
        if chat_response == "No":
          flag_chat = False


print("\nOk. See you then. Bye!")

