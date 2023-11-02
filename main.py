import openai
import time
# import os

openai.api_key = "Open AI API KEYが入ります"

createRes = openai.File.create(
  file=open("dataset.jsonl", "rb"),
  purpose='fine-tune'
)

# print(createRes)

model_id = createRes.id

print(model_id)

while True:
    print("waiting...")
    file_status = openai.File.wait_for_processing(model_id)
    if file_status == 'processed':
        break
    elif file_status == 'error':
        raise Exception("Fine-tuning failed!")
    else:
        time.sleep(30)

response_job = openai.FineTuningJob.create(training_file=model_id, model="gpt-3.5-turbo")
job_id = response_job.id

# モデルが準備されるまで30秒ごとにポーリング
while True:
    print("succeeded model waiting...")
    status = openai.FineTuningJob.retrieve(job_id).status
    if status == 'succeeded':
        break
    elif status == 'error':
        raise Exception("Fine-tuning failed!")
    else:
        time.sleep(30)

print(job_id)

content = "プロンプトがここに入ります"

completion = openai.ChatCompletion.create(
  model=job_id,
  messages=[
    {"role": "user", "content": content}
  ]
)

# print("ファインチューニングLIST", openai.FineTuningJob.list(limit=10))
print("The Question is:", content)
print("The Answer is:", completion.choices[0].message.content.encode("unicode-escape").decode("unicode-escape"))
# print("success!!", openai.FineTuningJob.list(limit=10))
