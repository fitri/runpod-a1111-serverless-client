
# Image Generation Script Using Runpod API

This Python script interacts with the Runpod API to generate images based on a given text prompt. It utilizes the **Runpod AI** to generate realistic images with customizable parameters, such as samplers, image dimensions, and other settings.

## Prerequisites
_____
Before you run the script, ensure you have the following:

- Python 3.x installed on your system.
- A **Runpod API key** (stored as an environment variable `KEY_RUNPOD`).
- Required Python libraries installed via `pip`:
  - `requests`
  - `base64`
  - `random`
  - `time`
  - `os`

You can install the required Python packages by running:

```bash
pip install requests
```

## Setup

1. **Set up your environment variable:**

   You need to set your **Runpod API key** as an environment variable. In your terminal:

   ```bash
   export KEY_RUNPOD="your_api_key_here"
   ```

2. **Configure the script:**

   - Modify the `prompt` and `negative_prompt` as per your desired image.
   - You can adjust the `samplers` dictionary to choose the sampling technique you prefer.
   - The script saves the generated image in the `./images/` directory (make sure this folder exists).

## How It Works

1. The script sends a POST request to the Runpod API with your input parameters (e.g., prompt, sampler type, seed).
2. The image generation job ID is retrieved from the API response.
3. The script then polls the API at regular intervals to check the status of the job.
4. Once the image is generated, it is decoded from Base64 and saved locally with a name based on the sampler, job ID, and seed.

## Example Workflow

1. **Start the image generation:**

   The script will send a request to generate an image with the specified prompt and parameters.

2. **Poll for image completion:**

   The script will keep checking the status of the job until it is marked as **COMPLETED**.

3. **Image saved:**

   Once the image is ready, it is saved to the `./images/` directory with a unique filename.

## Sample Output

```bash
Using sampler: DPM++ 3M SDE
Waiting for image to be ready ...
Polling the status ...
Image saved as DPM++_3M_SDE_abcde_12345.png
Parameters: {...}
Seed: 67890
```

## Notes

- If you encounter any issues during the image generation (e.g., failed job), the script will provide error messages.
- You can change the **sampler index**, **prompt**, **image dimensions**, and other settings by modifying the respective variables in the script.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
