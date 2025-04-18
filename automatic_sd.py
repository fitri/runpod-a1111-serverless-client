#!python

from pprint import pprint
import requests
import base64
import random
import time
import os

endpoint_url = {
    "A1111": "https://api.runpod.ai/v2/ednyb1ratn2bvz"
}

url = endpoint_url["A1111"]

headers = {
    'Content-Type': 'application/json',
    'Authorization': os.environ["KEY_RUNPOD"]
}

prompt = """
A real life looks photograph with a purple tint, capturing a striking beautiful slender young woman with medium sized chest with wavy shoulder length brown hair, wearing a cotton black unzipped hoodie and white sleeveless shirt under with red short skirts, looking at the viewer while bendding to play a game in a retro gaming arcade, she have beautiful black eyes with realistic details eye features. She is playing Sonic the Hedgehog with the words "Sonic 2" printed on the game cabinet. The image has a retro, nostalgic quality with characteristic grain and a soft vignette around the edges.
"""

negative_prompt = """
extra hands, extra knee, male, cock, 2 people, cameraman, socks, penis
"""

random_seed = ""

if random_seed == "":
    random_seed = random.randint(0, 2**32 - 1)
else:
    random_seed = random_seed

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
}

samplers = samplers["06"]
# samplers = samplers[(str(random.randint(0, 19)).zfill(2))]
print(f"\nUsing sampler: {samplers}")


data = {
    'input': {
        "prompt": prompt,
        "negative_prompt" : negative_prompt,
        "sampler_index" : samplers,
        "seed" : random_seed,
        "cfg_scale": 5,
        "width" : 1191,
        "height" : 842,
        "steps" : 100,

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
        print("Polling the status ...")
        status_response = requests.get(result_url, headers=headers)
        status_data = status_response.json()

        if status_data.get('status') == 'COMPLETED':
            print("Decoding images")
            
            image64 = status_data['output']['data']['images'][0]
            image_name = f"{samplers}_{job_id[:5]}_{random_seed}.png"
            parameter = status_data['output']['data']['parameters']
            with open(f"./images/{image_name}", "wb") as f:
                f.write(base64.b64decode(image64))
            print(f"Image saved as {image_name}")
            pprint(f"Parameters: {parameter}")
            print(f"Seed: {random_seed}")
            break
        elif status_data.get('status') == 'FAILED':
            print("Error: Image generation failed.")
            break

        time.sleep(5)  # Wait 5 seconds before polling again

else:
    print(f"Error: {response.status_code}, {response.text}")

