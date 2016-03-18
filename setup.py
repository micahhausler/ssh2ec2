import os
from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="ssh2ec2",
    version="0.5",
    author="Mike Ryan",
    author_email="mike@awssystemadministration.com",
    description="SSH into EC2 instances via tags and metadata filters",
    license="MIT",
    url="https://github.com/mikery/ssh2ec2",
    keywords=["amazon", "aws", "ec2", "ssh", "cloud", "boto"],
    packages=['ssh2ec2'],
    install_requires=requirements,
    entry_points={
        'console_scripts': ['ssh2ec2=ssh2ec2:main'],
    }
)