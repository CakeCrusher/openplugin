import { OpenPlugin } from "./openplugincore";

export class OpenPluginMemo {
  plugins: Map<string, OpenPlugin>;
  pluginsDirectory: Map<string, string> | undefined;

  constructor() {
    this.plugins = new Map();
    this.pluginsDirectory;
  }

  async init() {
    this.pluginsDirectory = new Map();
    const plugins_url =
      'https://raw.githubusercontent.com/CakeCrusher/openplugin/main/migrations/plugin_store/openplugins.json';
    const response = await fetch(plugins_url);
    if (!response.ok) {
      throw new Error(
        `Unable to fetch plugins from github url '${plugins_url}'`
      );
    }
    // add all json key and values to pluginsDirectory
    const plugins = await response.json();
    for (const [key, value] of Object.entries(plugins)) {
      this.pluginsDirectory.set(key, value as string);
    }
    console.log("MEMO READY")
  }

  async initPlugin(pluginName: string) {
    if (!this.pluginsDirectory) {
      throw new Error('Plugin directory not initialized');
    }
    const pluginUrl = this.pluginsDirectory.get(pluginName);
    if (pluginUrl === undefined) {
      throw new Error('Plugin not found');
    }
    const plugin = new OpenPlugin(pluginName, process.env.OPENAI_API_KEY, pluginUrl);
    await plugin.init();
    this.addPlugin(plugin);
    return plugin;
  }

  // method to add an OpenPlugin to the plugins map
  addPlugin(plugin: OpenPlugin) {
    if (!plugin.plugin_name) throw new Error("Plugin name not found");
    this.plugins.set(plugin.plugin_name, plugin);
  }

  // method to remove an OpenPlugin from the plugins map
  removePlugin(pluginName: string) {
    this.plugins.delete(pluginName);
  }

  // method to get an OpenPlugin by name
  getPlugin(pluginName: string) {
    return this.plugins.get(pluginName);
  }
}
