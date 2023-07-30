from setuptools import setup, find_packages

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name='openplugincore', 
        version="0.6.1",
        author="Sebastian Sosa",
        author_email="1sebastian1sosa1@gmail.com",
        description='Seamlessly integrate with OpenAI ChatGPT plugins via API (or client), offering the same powerful functionality as the ChatGPT api + plugins!',
        long_description='Seamlessly integrate with OpenAIs ChatGPT plugins via API (or client), offering the same powerful functionality as the ChatGPT api + plugins!',
        packages=find_packages(),
        package_data={
            "openplugincore": ["*.json"],  # include all .json files in the openplugin package
        },
        exclude=['tests'],
        install_requires=[
            'requests',
            'openai',
            'langchain',
            'python-dotenv',
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