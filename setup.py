from setuptools import find_packages, setup
from typing import List
from networksecurity.constant.training_pipeline import HYPEN_DOT, REQUIREMENT_FILE_NAME

def get_requirements(file_path: str) -> List[str]:
    requirements = []
    
    with open(file_path, "r") as file_obj:
        lines = file_obj.readlines()
    requirements = [req.strip().replace('\n', '') for req in lines]
    if HYPEN_DOT in requirements:
        requirements.remove(HYPEN_DOT)
    
    return requirements

setup(name="Network-Security-Phising-Detection",
      version="0.1.0", author="Theo",
      author_email="theofrolic@gmail.com",
      packages=find_packages(), install_requires=get_requirements(REQUIREMENT_FILE_NAME))