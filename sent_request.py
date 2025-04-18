#!python

from pprint import pprint
import requests
import base64
import random
import time
import yaml
import os

# start script timer
start = time.time()

endpoint_url = {
    "A1111": "https://api.runpod.ai/v2/ednyb1ratn2bvz"
}

url = endpoint_url["A1111"]

headers = {
    'Content-Type': 'application/json',
    'Authorization': os.environ["KEY_RUNPOD"]
}

prompt = """
A real life looks photograph with vibrant colors capturing full body of a beautiful young woman with medium-large sized chest with wavy shoulder length dark-brown hair, wearing a japanese anime black and white themed maid style clothes with some laces watching a television in living room, she have beautiful black eyes with realistic details eye features.
"""

negative_prompt = """
extra hands, extra knee, male, 2 people, cameraman
"""

random_seed = ""

if random_seed == "":
    random_seed = random.randint(0, 2**32 - 1)
else:
    random_seed = random_seed

# Sampler method
samplers = {
"01": "DPM++ 2M",
"02": "DPM++ SDE",
"03": "DPM++ 2M SDE",
"04": "DPM++ 2M SDE Heun",
"05": "DPM++ 2S a",
"06": "DPM++ 3M SDE",
"07": "Euler a",
"08": "Euler",
"09": "LMS",
"10": "Heun",
"11": "DPM2",
"12": "DPM2 a",
"13": "DPM fast",
"14": "DPM adaptive",
"15": "Restart",
"16": "DDIM",
"17": "PLMS",
"18": "UniPC",
"19": "LCM",
"20": "random"
}

# Setting sampler including function to set random sampler
sampler = samplers["20"]
if sampler == "random":
    sampler = samplers[(str(random.randint(0, 19)).zfill(2))]

print(f"\nUsing sampler: {sampler}")


data = {
    'input': {
        "prompt": prompt,
        "negative_prompt" : negative_prompt,
        "sampler_index" : sampler,
        "seed" : random_seed,
        "cfg_scale": 5,
        "width" : 1191,
        "height" : 842,
        "steps" : 100
    }
}

response = requests.post(f"{url}/run", headers=headers, json=data)

if response.status_code == 200:
    job_id = response.json().get('id')
    if not job_id:
        print("Error: Job ID not found in response.")
        exit()

    # Step 2: Poll for the result
    print("\nWaiting for image to be ready ...")
    result_url = f"{url}/status/{job_id}"
    while True:
        # Show elapsed polling time
        elapsed = int(time.time() - start)
        print(f"\rPolling... Elapsed: {elapsed}s", end='', flush=True)
        
        status_response = requests.get(result_url, headers=headers)
        status_data = status_response.json()

        if status_data.get('status') == 'COMPLETED':
            print("Decoding images")
            
            image64 = status_data['output']['data']['images'][0]
            image_name = f"{sampler}_{job_id[:5]}_{random_seed}.png"
            parameter = status_data['output']['data']['parameters']
            with open(f"./images/{image_name}", "wb") as f:
                f.write(base64.b64decode(image64))
            print(f"Image saved as {image_name}")
            # pprint(f"Parameters: {parameter}")
            print(yaml.dump(parameter, sort_keys=False, default_style=None))
            print(f"Seed: {random_seed}")
            break
        elif status_data.get('status') == 'FAILED':
            print("Error: Image generation failed.")
            break

        time.sleep(1)  # Wait 5 seconds before polling again

else:
    print(f"Error: {response.status_code}, {response.text}")

