import { agent, agentGraph, mcpTool, agentMcp } from '@inkeep/agents-sdk';
import { contextConfig, fetchDefinition } from "@inkeep/agents-core";
import { z } from "zod";
import { weatherMcpTool } from '../tools/weather-mcp';

/**
 * Intermediate Weather Graph with Time Context
 * 
 * This agent extends the basic weather graph with a time context. To use this agent, you must have a timezone in the request context.
 * 
 * By passing in the timezone, the agent will fetch the current time and date and have it available when answering questions.
 * 
 * This enables the agent to answer more advanced questions about the weather, such as "what is the weather in Tokyo a week from now?"
 */

// 1. Create the request schema
// You can find a timezone list here: https://github.com/davidayalas/current-time?tab=readme-ov-file
// Example: US/Pacific, US/Eastern, etc.
const requestSchema = z.object({
  tz: z.string(),
});

// 2. Create the fetcher
const timeFetcher = fetchDefinition({
  id: "time-info",
  name: "Time Information",
  trigger: "invocation",
  fetchConfig: {
    url: "https://world-time-api3.p.rapidapi.com/timezone/{{requestContext.tz}}",
    method: "GET",
    headers: {
      "x-rapidapi-key": "590c52974dmsh0da44377420ef4bp1c64ebjsnf8d55149e28d",
    },
  },
  responseSchema: z.object({
    datetime: z.string(),
    timezone: z.string().optional(),
  }),
  defaultValue: "Unable to fetch time information",
});

// 3. Configure context
const timeContext = contextConfig({
  id: "time-context",
  name: "Time Context",
  description: "Fetches time information for personalization",
  requestContextSchema: requestSchema,
  contextVariables: {
    time: timeFetcher,
  },
});

// Agents
const weatherAssistant = agent({
  id: 'weather-assistant',
  name: 'Weather assistant',
  description: 'Responsible for routing between the coordinates agent and weather forecast agent',
  prompt:
    'You are a helpful assistant. The time is {{time}} in the timezone {{requestContext.tz}}.  When the user asks about the weather in a given location, first ask the coordinates agent for the coordinates, and then pass those coordinates to the weather forecast agent to get the weather forecast. Be sure to pass todays date to the weather forecaster.',
  canDelegateTo: () => [weatherForecaster, coordinatesAgent],
});

const weatherForecaster = agent({
  id: 'weather-forecaster-intermediate',
  name: 'Weather forecaster',
  description:
    'This agent is responsible for taking in coordinates and returning the forecast for the weather at that location',
  prompt:
    'You are a helpful assistant responsible for taking in coordinates and returning the forecast for that location using your forecasting tool. Pass in todays date as the start date if the user does not specify a date and 7 days from today as the end date.',
  canUse: () => [agentMcp({ server: weatherMcpTool, selectedTools: ["get_weather_forecast_for_date_range"] })],
});

const coordinatesAgent = agent({
  id: 'coordinates-agent-intermediate',
  name: 'Coordinates agent',
  description: 'Responsible for converting location or address into coordinates',
  prompt:
    'You are a helpful assistant responsible for converting location or address into coordinates using your coordinate converter tool',
  canUse: () => [agentMcp({ server: weatherMcpTool, selectedTools: ["get_coordinates"] })],
});

// Agent Graph
export const weatherIntermediateGraph = agentGraph({
  id: 'weather-graph-intermediate',
  name: 'Weather graph intermediate',
  description: 'Asks for the weather forecast for the given location with time context',
  defaultAgent: weatherAssistant,
  agents: () => [weatherAssistant, weatherForecaster, coordinatesAgent],
  contextConfig: timeContext
});