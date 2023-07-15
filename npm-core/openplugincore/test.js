'use strict'
import { convertOpenAPISpecToOpenAIFunctions, OpenAPISpec } from "oplangchain/chains/openai_functions"
import { ChatOpenAI } from "oplangchain/chat_models/openai"
import { LLMChain } from "oplangchain/chains"
import { ChatPromptTemplate, HumanMessagePromptTemplate } from "oplangchain/prompts"
import { JsonOutputFunctionsParser } from "oplangchain/output_parsers"

import dotenv from "dotenv"
dotenv.config()


const openapiToFunctionsAndCallApiFn = async (manifest) => {
  const spec = manifest.api.url

  let convertedSpec;
  if (typeof spec === "string") {
    try {
      convertedSpec = await OpenAPISpec.fromURL(spec);
    } catch (e) {
      try {
        convertedSpec = OpenAPISpec.fromString(spec);
      } catch (e) {
        throw new Error(`Unable to parse spec from source ${spec}.`);
      }
    }
  } else {
    convertedSpec = OpenAPISpec.fromObject(spec);
  }  

  const { openAIFunctions, defaultExecutionMethod } =
  convertOpenAPISpecToOpenAIFunctions(convertedSpec);

  if (defaultExecutionMethod === undefined) {
    throw new Error(
      `Could not parse any valid operations from the provided spec.`
    );
  }

  return {openAIFunctions, defaultExecutionMethod}
}

const { openAIFunctions, defaultExecutionMethod } = await openapiToFunctionsAndCallApiFn(
  {"api": {"url": "https://browserplugin.feednews.com/.well-known/openapi.yaml"}}
)
console.log(openAIFunctions, defaultExecutionMethod)

const fetchPlugin = async (args) => {
  const {
    model = "gpt-3.5-turbo-0613",
    prompt = null,
    verbose = false,
    ...rest
  } = args;
  const prompt_template = ChatPromptTemplate.fromPromptMessages([
    HumanMessagePromptTemplate.fromTemplate(
      "{query}"
    ),
  ])
  const llm = new ChatOpenAI({ modelName: model })
  const formatChain = new LLMChain({
    llm,
    prompt: prompt_template,
    outputParser: new JsonOutputFunctionsParser({ argsOnly: false }),
    outputKey: "function",
    llmKwargs: { functions: openAIFunctions }
  });
  
  const result = await formatChain.run(
    prompt
  );
  const requestChain = async (name, args) => {
    const res = await defaultExecutionMethod(name, args);
    return res;
  }

  let requestOut = await requestChain(result.name, result.arguments);
  let jsonResponse = JSON.parse(requestOut);

  return jsonResponse;
}

const jsonResponse = await fetchPlugin({
  model: "gpt-3.5-turbo-0613",
  prompt: "Analyse and understand the web page at https://github.com/ and provide suggestions for improvement.",
})
console.log(jsonResponse)

