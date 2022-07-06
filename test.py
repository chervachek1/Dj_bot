import os
from dotenv import load_dotenv

load_dotenv(fr'C:\CONFIG.env')

GCP_PROJECT_ID = os.getenv('DISCORD_TOKEN')
print(GCP_PROJECT_ID)