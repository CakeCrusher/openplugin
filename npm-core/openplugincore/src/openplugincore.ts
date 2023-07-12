import 'isomorphic-fetch';
import { OpenAPISpec, convertOpenAPISpecToOpenAIFunctions } from 'oplangchain/chains/openai_functions';
import dotenv from 'dotenv';
dotenv.config();

type OpenPluginManifest = {
  description_for_model: string;
  api: {
    url: string;
  };
  // ... other manifest properties
};

interface OpenPluginFunction {
  [key: string]: any;
}

type OpenAPIFunction = Record<string, any>;
type Callable = (...args: any[]) => any;
type OpenAPISpecType = OpenAPISpec | string;

export class OpenPlugin {
  plugin_name: string | undefined;
  root_url: string | undefined;
  description: string | null;
  manifest: OpenPluginManifest | null;
  functions: OpenPluginFunction[] | null;
  call_api_fn: Callable | null;
  verbose: boolean;
  
  constructor(
    plugin_name: string | undefined = undefined, 
    openai_api_key: string | undefined = undefined, 
    root_url: string | undefined = undefined, 
    verbose: boolean = false,
  ) {
    this.plugin_name = plugin_name;
    this.root_url = root_url;
    this.description = null;
    this.manifest = null;
    this.functions = null;
    this.call_api_fn = null;
    this.verbose = verbose;

    if (this.plugin_name === null && this.root_url === null) {
      throw new Error("Either plugin_name or root_url must be passed in as a parameter");
    }

    if (openai_api_key === null) {
      openai_api_key = process.env.OPENAI_API_KEY;
      if (openai_api_key === null) {
        throw new Error("OPENAI_API_KEY not found. You can pass in the parameter openai_api_key. You can also set the environment variable OPENAI_API_KEY=<API-KEY>.");
      }
      process.env.OPENAI_API_KEY = openai_api_key;
    }
  }

  async init() {
    // fetch plugins from github
    const plugins_url = "https://raw.githubusercontent.com/CakeCrusher/openplugin/main/migrations/plugin_store/openplugins.json";
    
    let plugins: { [key: string]: string; };
    try {
      const response = await fetch(plugins_url);
      if (!response.ok) {
        throw new Error(`Unable to fetch plugins from github url '${plugins_url}'`);
      }
      plugins = await response.json();
    } catch (error) {
      throw new Error(`Unable to fetch plugins from github url '${plugins_url}'`);
    }
    
    if (this.root_url === undefined) {
      const pluginUrl = plugins[this.plugin_name!];
      if (pluginUrl === undefined) {
        throw new Error("Plugin not found");
      }
      this.root_url = pluginUrl;
    }
  
    this.manifest = await this.fetch_manifest(this.root_url);
    if (!this.manifest?.description_for_model) {
      throw new Error("Manifest does not contain a description_for_model");
    }
    this.description = this.manifest?.description_for_model;
    [this.functions, this.call_api_fn] = await this.openapi_to_functions_and_call_api_fn(this.manifest);
  }
  
  async fetch_manifest(root_url: string) {
    const manifestUrl = root_url + "/.well-known/ai-plugin.json"
    console.log(`Fetching manifest from ${manifestUrl}`);
    const response = await fetch(manifestUrl);
    if (!response.ok) {
      throw new Error("Failed to fetch the manifest"); 
    }
    const manifest = await response.json();
  
    if (!this.plugin_name) {
      this.plugin_name = manifest.name_for_model;
    }
  
    if (this.verbose) {
      console.log(`"${this.plugin_name}" manifest: `, JSON.stringify(manifest, null, 2));
    }
  
    return manifest;
  }
  
  async openapi_to_functions_and_call_api_fn(manifest: any): Promise<
  [OpenAPIFunction[], Callable]
  > {
    let openapi_url: OpenAPISpecType | undefined = manifest.api.url;
    if (!openapi_url) {
      throw new Error("Manifest does not contain an api.url");
    }

    if (this.verbose) {
      console.log(`"${this.plugin_name}" openapi_url: `, openapi_url);
    }

    let convertedSpec;
    if (typeof openapi_url === "string") {
      try {
        convertedSpec = await OpenAPISpec.fromURL(openapi_url);
      } catch (e) {
        try {
          convertedSpec = OpenAPISpec.fromString(openapi_url);
        } catch (e) {
          throw new Error(`Unable to parse spec from source ${openapi_url}.`);
        }
      }
    } else {
      convertedSpec = OpenAPISpec.fromObject(openapi_url);
    }

    const { openAIFunctions: openai_fns, defaultExecutionMethod: call_api_fn } =
      convertOpenAPISpecToOpenAIFunctions(convertedSpec);

    if (this.verbose) {
      console.log(`"${this.plugin_name}" functions: `, JSON.stringify(openai_fns, null, 2));
    }
    return [openai_fns, call_api_fn as Callable];
  }
}
