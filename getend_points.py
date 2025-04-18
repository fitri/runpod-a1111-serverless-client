import runpod
import os

runpod.api_key = os.getenv("RUNPOD_API_KEY")

# Fetching all available endpoints
endpoints = runpod.get_endpoints()

# Displaying the list of endpoints
print(endpoints)
