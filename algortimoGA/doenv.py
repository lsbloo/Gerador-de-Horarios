import os
from dotenv import load_dotenv
def loadenv():
    project_folder = os.path.expanduser('~/algortimoGA')
    load_dotenv(os.path.join(project_folder,'.env'))