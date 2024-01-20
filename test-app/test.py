import json
import os
from llama_cpp import Llama
import time


def extract_json_from_job(job_description):
    output = llm.create_chat_completion(
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that extracts information from job ads. Be concise and succint.",
            },
            {
                "role": "user",
                "content": f"""You will be given the text of job ad.
Read the JOB_AD and then answer the QUESTIONS following the RULES.

# JOB_AD

{job_description}

# RULES

- Salary range: if the salary is not mentioned just say "missing", if the salary is indicated a "competitive" just say "missing".
- Workplace arrangement: can be one of "Full Remote", "Hybrid", "Onsite", "Unspecified".
- Developer role: can be one of "Backend", "Frontend", "Full Stack", "Devops", "Other"

# QUESTIONS

- What is the "Salary range"? 
- What is the "Workplace arrangement"?
- What is the "Developer role"?
""",
            },
        ]
    )
    print(output)
    return output["choices"][0]["message"]["content"]


with open("extract_of_10_job_details.json") as f:
    data = json.load(f)

print("Loaded data")

path_to_model = os.getenv("MODEL")
if path_to_model is None:
    raise ValueError("Environment variable MODEL is not set")
print(f"Using model {path_to_model}")
llm = Llama(model_path=path_to_model, chat_format="chatml", n_gpu_layers=-1, n_ctx=4096, n_threads=12)

results = []
start_time = time.time()

for job_description in data:
    extracted_info = extract_json_from_job(job_description)
    results.append(extracted_info)

end_time = time.time()
elapsed_time = end_time - start_time
minutes, seconds = divmod(elapsed_time, 60)
print("------")
print(f"Elapsed time {int(minutes)} minutes and {int(seconds)} seconds")
print("------")
print("Results:")
for i, result in enumerate(results, start=1):
    print(f"Answer {i}:")
    print(result)
print("------")
print("Have a nice day!")
