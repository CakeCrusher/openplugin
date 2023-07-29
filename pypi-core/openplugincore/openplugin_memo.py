import requests
from openplugincore import OpenPlugin
import os

class OpenPluginMemo:
    def __init__(self):
        self.plugins = {}
        self.plugins_directory = None

    def init(self):
        self.plugins_directory = {}
        plugins_url = 'https://raw.githubusercontent.com/CakeCrusher/openplugin/main/migrations/plugin_store/openplugins.json'
        response = requests.get(plugins_url)
        if not response.ok:
            raise Exception(f"Unable to fetch plugins from github url '{plugins_url}'")
        # add all json key and values to pluginsDirectory
        plugins = response.json()
        for key, value in plugins.items():
            self.plugins_directory[key] = value
        print('MEMO READY')

    def init_plugin(self, plugin_name):
        if not self.plugins_directory:
            raise Exception('Plugin directory not initialized')
        plugin_url = self.plugins_directory.get(plugin_name)
        if plugin_url is None:
            raise Exception('Plugin not found')
        plugin = OpenPlugin(plugin_name=plugin_name, openai_api_key=os.getenv('OPENAI_API_KEY'))
        plugin.init()
        self.add_plugin(plugin)
        return plugin

    # method to add an OpenPlugin to the plugins map
    def add_plugin(self, plugin):
        if not plugin.name:
            raise Exception('Plugin name not found')
        self.plugins[plugin.name] = plugin

    # method to remove an OpenPlugin from the plugins map
    def remove_plugin(self, plugin_name):
        self.plugins.pop(plugin_name, None)

    # method to get an OpenPlugin by name
    def get_plugin(self, plugin_name):
        return self.plugins.get(plugin_name)
