from setuptools import setup, find_packages

requirements = [x.strip() for x in open("requirements.txt", "r").readlines()]

setup(
    name='BehindIt',
    version='0.1.0',
    description='Finding out who shared an instagram or tiktok content',
    author='Gobutsu',
    packages=find_packages(),  # Automatically find packages in your directory
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'behindit = behindit.main:main'
        ]
    },
    python_requires='>=3.6',
)
