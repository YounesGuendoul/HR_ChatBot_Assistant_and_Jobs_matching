from sentence_transformers import SentenceTransformer, util
sentences = ["you should be able to travel.", "I like to stay at home"]

stnc1 = ""
with open(f"softskills1.txt", "r", encoding='utf-8') as f:
    stnc1 += f.read() 

stnc2 = ""
with open(f"softskills3.txt", "r", encoding='utf-8') as f:
    stnc2 += f.read() 

stncjob = ""
with open(f"soft_skills_jobd.txt", "r", encoding='utf-8') as f:
    stncjob += f.read() 

sentences = [stnc1, stncjob]
#Model 1
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

#Compute embedding for both lists
embedding_1= model.encode(sentences[0], convert_to_tensor=True)
embedding_2 = model.encode(sentences[1], convert_to_tensor=True)

value = util.pytorch_cos_sim(embedding_1, embedding_2)
print('Matching CV1 with the job',value,'\n')


sentences = [stnc2, stncjob]
#Model 1

#Compute embedding for both lists
embedding_1= model.encode(sentences[0], convert_to_tensor=True)
embedding_2 = model.encode(sentences[1], convert_to_tensor=True)

value = util.pytorch_cos_sim(embedding_1, embedding_2)
print('Matching CV3 with the job',value,'\n')
