import 'isomorphic-fetch';
import {
  OpenAPISpec,
  convertOpenAPISpecToOpenAIFunctions,
} from 'oplangchain/chains/openai_functions';
import { ChatOpenAI } from 'oplangchain/chat_models/openai';
import { LLMChain } from 'oplangchain/chains';
import {
  ChatPromptTemplate,
  HumanMessagePromptTemplate,
} from 'oplangchain/prompts';
import { JsonOutputFunctionsParser } from 'oplangchain/output_parsers';

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

type LlmChainOutput = {
  name: string;
  arguments: any;
};
type ChatgptFunctionMessage = {
  role: 'function';
  name: string;
  content: string;
};

export class OpenPlugin {
  pluginName: string | undefined;
  rootUrl: string | undefined;
  description: string | null;
  manifest: OpenPluginManifest | null;
  functions: OpenPluginFunction[] | null;
  callApiFn: Callable | null;
  verbose: boolean;

  constructor(
    pluginName: string | undefined = undefined,
    rootUrl: string | undefined = undefined,
    openaiApiKey: string | undefined = process.env.OPENAI_API_KEY,
    verbose: boolean = false
  ) {
    this.pluginName = pluginName;
    this.rootUrl = rootUrl;
    this.description = null;
    this.manifest = null;
    this.functions = null;
    this.callApiFn = null;
    this.verbose = verbose;

    if (!this.pluginName && !this.rootUrl) {
      throw new Error(
        'Either pluginName or rootUrl must be passed in as a parameter'
      );
    }

    if (openaiApiKey) {
      process.env.OPENAI_API_KEY = openaiApiKey;
    } else {
      throw new Error(
        'openaiApiKey not found. You can pass in the parameter openaiApiKey. You can also set the environment variable openaiApiKey=<API-KEY>.'
      );
    }
  }

  async init() {
    // fetch plugins from github
    if (!this.rootUrl) {
      const plugins_url =
        'https://raw.githubusercontent.com/CakeCrusher/openplugin/main/migrations/plugin_store/openplugins.json';

      let plugins: { [key: string]: string };
      try {
        const response = await fetch(plugins_url);
        if (!response.ok) {
          throw new Error(
            `Unable to fetch plugins from github url '${plugins_url}'`
          );
        }
        plugins = await response.json();
      } catch (error) {
        throw new Error(
          `Unable to fetch plugins from github url '${plugins_url}'`
        );
      }

      const pluginUrl = plugins[this.pluginName!];
      if (pluginUrl === undefined) {
        throw new Error('Plugin not found');
      }
      this.rootUrl = pluginUrl;
    }

    this.manifest = await this.fetchManifest(this.rootUrl);
    if (!this.manifest?.description_for_model) {
      throw new Error('Manifest does not contain a description_for_model');
    }
    this.description = this.manifest?.description_for_model;
    [this.functions, this.callApiFn] = await this.openapiToFunctionsAndAllApiFn(
      this.manifest
    );
    if (!this.functions || this.functions.length === 0) {
      throw new Error('No plugin functions');
    }
    if (!this.callApiFn) {
      throw new Error('No api call function');
    }
  }

  async fetchManifest(rootUrl: string) {
    const manifestUrl = rootUrl + '/.well-known/ai-plugin.json';
    const response = await fetch(manifestUrl);
    if (!response.ok) {
      throw new Error('Failed to fetch the manifest');
    }
    const manifest = await response.json();

    if (!this.pluginName) {
      this.pluginName = manifest.name_for_model;
    }

    if (this.verbose) {
      console.log(
        `"${this.pluginName}" manifest: `,
        JSON.stringify(manifest, null, 2)
      );
    }

    return manifest;
  }

  async openapiToFunctionsAndAllApiFn(
    manifest: any
  ): Promise<[OpenAPIFunction[], Callable]> {
    let openapi_url: OpenAPISpecType | undefined = manifest.api.url;
    if (!openapi_url) {
      throw new Error('Manifest does not contain an api.url');
    }

    if (this.verbose) {
      console.log(`"${this.pluginName}" openapi_url: `, openapi_url);
    }

    let convertedSpec;
    if (typeof openapi_url === 'string') {
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

    const { openAIFunctions: openai_fns, defaultExecutionMethod: callApiFn } =
      convertOpenAPISpecToOpenAIFunctions(convertedSpec);

    if (this.verbose) {
      console.log(
        `"${this.pluginName}" functions: `,
        JSON.stringify(openai_fns, null, 2)
      );
    }
    return [openai_fns, callApiFn as Callable];
  }
  async fetch_plugin(args: any = {}): Promise<ChatgptFunctionMessage> {
    const { prompt, ...chatgpt_args } = args;
    const model = chatgpt_args['model'];
    if (model !== 'gpt-3.5-turbo-0613' && model !== 'gpt-4-0613') {
      throw new Error('Model must be either gpt-3.5-turbo-0613 or gpt-4-0613');
    }

    let llm = new ChatOpenAI(chatgpt_args);
    const prompt_template = ChatPromptTemplate.fromPromptMessages([
      HumanMessagePromptTemplate.fromTemplate('{query}'),
    ]);
    let llm_chain = new LLMChain({
      llm,
      prompt: prompt_template,
      outputParser: new JsonOutputFunctionsParser({ argsOnly: false }),
      outputKey: 'function',
      llmKwargs: { functions: this.functions } as any,
      verbose: this.verbose,
    });

    let llm_chain_out: LlmChainOutput;
    llm_chain_out = (await llm_chain.run(prompt)) as unknown as LlmChainOutput;
    if (this.verbose) {
      console.log('Using plugin: ' + this.pluginName);
    }

    if (
      !this.functions!.some(function (elem) {
        return elem['name'] === llm_chain_out['name'];
      })
    ) {
      throw new Error('Not a plugin function');
    }

    let removeEmptyFromDict = (input_dict: any) => {
      let cleaned_dict: any = {};
      for (let k in input_dict) {
        let v = input_dict[k];
        if (typeof v === 'object') {
          v = removeEmptyFromDict(v);
        }
        if (v && v !== 'none') {
          cleaned_dict[k] = v;
        }
      }
      return cleaned_dict;
    };

    llm_chain_out['arguments'] = removeEmptyFromDict(
      llm_chain_out['arguments']
    );
    if (this.verbose) {
      console.log(
        `${this.pluginName} llm_chain_out: `,
        JSON.stringify(llm_chain_out, null, 2)
      );
    }

    let requestChain = async (name: string, args: any) => {
      try {
        let res = await this.callApiFn!(name, args, null, null); // Assuming callApiFn is defined in the class
        return res;
      } catch (e) {
        throw new Error(`Failed to call api: ${e}`);
      }
    };

    let request_out = await requestChain(
      llm_chain_out['name'],
      llm_chain_out['arguments']
    );
    let json_response = await JSON.parse(request_out);

    if (this.verbose) {
      console.log(
        `${this.pluginName} json_response: `,
        JSON.stringify(json_response, null, 2)
      );
    }

    return {
      role: 'function',
      name: llm_chain_out['name'],
      content: JSON.stringify(json_response),
    };
  }
}
