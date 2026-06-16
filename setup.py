from setuptools import find_packages, setup
from typing import List

def get_requirements()->List[str]:
    requirements_list:List[str] = []

    try:
        with open('requirement.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != '-e .':
                    requirements_list.append(requirement)
    except FileNotFoundError:
        print("requirement.txt file not found. Please ensure it exists in the same directory as setup.py.")

    return requirements_list
print(get_requirements())

setup(
    name='AI_Trip_Planner',
    version='0.1.0',
    packages=find_packages(),
    install_requires=get_requirements()
)