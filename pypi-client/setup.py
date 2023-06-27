from setuptools import setup, find_packages

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name='openpluginclient', 
        version="0.1.7",
        author="Sebastian Sosa",
        author_email="1sebastian1sosa1@gmail.com",
        description='Python package for accessing ChatGPT plugins via API',
        long_description='Client for accessing ChatGPT plugins via OpenPlugin API',
        packages=find_packages(),
        package_data={
            "openpluginclient": ["*.json"],  # include all .json files in the openplugin package
        },
        exclude=['tests'],
        install_requires=[
            'requests'
        ], # add any additional packages
        
        keywords=[
            'python',
            'openai',
            'chatgpt',
            'chat',
            'plugin'
        ],
        classifiers= [
            "Development Status :: 2 - Pre-Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)