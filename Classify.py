#Inference model, Sequence 2 Domain:
from transformers import AutoTokenizer, TrainingArguments, Trainer, AutoModelForSequenceClassification, TextClassificationPipeline
class_names = {'LABEL_0': 'Civil Engineer', 'LABEL_1': 'PMO', 'LABEL_2': 'Network Security Engineer', 'LABEL_3': 'Software Developer', 'LABEL_4': 'DataScientist', 'LABEL_5': 'Arts'}

model = AutoModelForSequenceClassification.from_pretrained("C:/Users/youne/Desktop/aisummerschool/Weights/my_model", num_labels=6)
tokenizer = AutoTokenizer.from_pretrained('C:/Users/youne/Desktop/aisummerschool/Weights/my_token')

pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, return_all_scores=False)
#outputs a list of dicts like [[{'label': 'NEGATIVE', 'score': 0.0001223755971295759},  {'label': 'POSITIVE', 'score': 0.9998776316642761}]]

All_CVs = []
for i in range(1, 5):
    with open(f"skills{i}.txt", "r", encoding='utf-8') as f:
        All_CVs.append(f.read())
JobD = ""
with open(f"skills_jobd.txt", "r", encoding='utf-8') as f:
    JobD=f.read()
p_job=pipe(JobD)
predicted_label = p_job[0]['label']
predicted_job_domain = class_names[predicted_label]



for i,candidate in enumerate(All_CVs):
    out=pipe(candidate)
    #print(out)
    predicted_label = out[0]['label']

    # Step 3: Use the key to find the value in the class_names dictionary
    predicted_value = class_names[predicted_label]
    if predicted_value == predicted_job_domain:
        print("cv"+str(i+1)+" is accepted\n")
    else:
        print("cv"+str(i+1)+" is rejected\n") 

    #print("The following CV is fitting", predicted_value, "Domain.")