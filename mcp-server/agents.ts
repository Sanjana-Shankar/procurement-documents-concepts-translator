 import { agent, agentGraph } from '@inkeep/agents-sdk';

 const helloAgent = agent({
   id: 'hello-agent',
   name: 'Hello Agent',
   description: 'A basic agent',
   prompt:
     'You are a basic agent that just says hello. You only reply with the word "hello", but you may do it in different variations like h3110, h3110w0rld, h3110w0rld! etc...',
 });

 export const graph = agentGraph({
   id: 'basic-graph',
   name: 'Basic Graph Example',
   description: 'A basic graph',
   defaultAgent: helloAgent,
   agents: () => [helloAgent],
 });