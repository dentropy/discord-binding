from urllib.parse import urlparse
from pprint import pprint
import pandas as pd
from pprint import pprint

from modules.query_resolver import query_resolver

import psycopg2
import psycopg2.extras
from pgvector.psycopg2 import register_vector
import numpy as np


import os
from decouple import AutoConfig
current_directory = os.getcwd()
parent_directory = os.path.dirname(current_directory)
config = AutoConfig(search_path=current_directory)
url = urlparse(config("db_url"))
connection = psycopg2.connect(
    host=url.hostname,
    port=url.port,
    database=url.path[1:],
    user=url.username,
    password=url.password
)
cursor = connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
register_vector(connection)

# AI 
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
# #Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
# # Load model from HuggingFace Hub
embedding_model='sentence-transformers/all-MiniLM-L6-v2'
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
# END AI

cursor.execute("select count(*) as count from messages_t")
query_results = cursor.fetchall()
result_df = pd.DataFrame(query_results)
num_of_messages = result_df.iloc[0]["count"]
for i in range(0, num_of_messages, 100):
    query = f"""
        select 
            *
        from
            messages_t
        limit 100
        offset {i}
    """
    cursor.execute(query)
    query_results = cursor.fetchall()
    result_df = pd.DataFrame(query_results)
    print(len(result_df))

    message_ids = []
    sentences = []
    for msg_content in result_df.itertuples():
        message_ids.append(msg_content.id)
        sentences.append(msg_content.msg_content)
        # print(msg_content.msg_content)
        # msg_content = row.iloc[0]["msg_content"]
        # print(msg_content)

    # START AI
    # Tokenize sentences
    encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)
    # Perform pooling
    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
    # Normalize embeddings
    sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)
    # END AI
    print("Sentence embeddings:")
    print(len(sentence_embeddings))
    print(len(sentence_embeddings[0]))
    print(len(sentence_embeddings[1]))
    query = """
    INSERT INTO messages_vectors_bert_t (
        message_id      ,
        embedding_model ,
        embedding
    )
    VALUES (
        %s, %s, %s
    );
    """
    for i in range(len(message_ids)):
        print("INSERTING")
        cursor.execute(query, (message_ids[i], embedding_model, np.array( sentence_embeddings[i]) ))
        connection.commit()

# # Sentences we want sentence embeddings for
# sentences = ['This is an example sentence', 'Each sentence is converted']


# # Tokenize sentences
# encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')

# # Compute token embeddings
# with torch.no_grad():
#     model_output = model(**encoded_input)

# # Perform pooling
# sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

# # Normalize embeddings
# sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)

# print("Sentence embeddings:")
# print(sentence_embeddings)
# print(len(sentence_embeddings[0]))
# print(len(sentence_embeddings[1]))