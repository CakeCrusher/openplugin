# Add Plugin
How to add a plugin to OpenPlugin ecosystem.
Things to note:
- Authentication is not supported
- The plugin must be deployed to a publicly accessible URL
## Setup
1. Fork this repo, and clone it to your local machine
2. Createa a branch titled `plugin/<PLUGIN_NAME>` like so `git checkout -b plugin/todo`
3. Create new OpenAI secret key, [see here for guide](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)
4. Add the secret key to your environment variables with the name `OPENAI_API_KEY`
5. Create a virtual environment `python -m venv <NAME_OF_ENV>`
6. Activate the virtual environment
7. Navigate to directory `openplugin/migrations/plugin_store`
8. Install the requirements `pip install -r requirements.txt`
9. Run `python add_plugin.py`
10. Follow the prompts
11. Commit the changes to the repo (excluding your virtual environment)
12. Create a pull request to merge your branch into `CakeCrusher/openplugin` branch `main`