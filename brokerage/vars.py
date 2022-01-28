import os
from dotenv import load_dotenv
load_dotenv()


BROKER_KEY=os.getenv("BROKER_KEY")
BROKER_SECRET=os.getenv("BROKER_SECRET")

all_variables = {item: value for item, value in vars().items()}