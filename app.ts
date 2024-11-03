// app.ts
import express from 'express';
import { Request, Response } from 'express-serve-static-core';
import session from 'express-session';

declare module 'express-session' {
  interface SessionData {
    accessToken: string;
  }
}

import axios from 'axios';
import { createGraphQLClient, getHubs, getProjects } from './graphql_client.js';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const PORT = 8080;

// Updated redirect URI
const REDIRECT_URI = 'http://localhost:8080/api/auth/callback';
const SCOPES = ['data:read', 'account:read', 'viewables:read'];


// Load CLIENT_ID and CLIENT_SECRET from environment variables
const CLIENT_ID = process.env.CLIENT_ID;
const CLIENT_SECRET = process.env.CLIENT_SECRET;

if (!CLIENT_ID || !CLIENT_SECRET) {
  console.error('Please set CLIENT_ID and CLIENT_SECRET in your environment variables.');
  process.exit(1);
}

// Configure session middleware
app.use(
  session({
    secret: 'your_session_secret',
    resave: false,
    saveUninitialized: true,
  })
);

// Root route to initiate OAuth flow
app.get('/', (req: Request, res: Response) => {
  const authUrl = 'https://developer.api.autodesk.com/authentication/v2/authorize';
  const params = new URLSearchParams({
    response_type: 'code',
    client_id: CLIENT_ID!,
    redirect_uri: REDIRECT_URI,
    scope: SCOPES.join(' '),
  });
  res.redirect(`${authUrl}?${params.toString()}`);
});

// Callback route to handle OAuth redirect
app.get('/api/auth/callback', async (req: Request, res: Response): Promise<any> => {
  const code = req.query.code as string;
  if (!code) {
    return res.status(400).json({ error: 'Authorization code not found' });
  }

  try {
    // Exchange code for access token
    const tokenUrl = 'https://developer.api.autodesk.com/authentication/v2/token';
    const data = new URLSearchParams({
      client_id: CLIENT_ID!,
      client_secret: CLIENT_SECRET!,
      grant_type: 'authorization_code',
      code,
      redirect_uri: REDIRECT_URI,
    });

    const response = await axios.post(tokenUrl, data.toString(), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });

    const tokens = response.data;
    const accessToken = tokens.access_token;
    req.session.accessToken = accessToken;

    // Perform GraphQL query
    const result = await performGraphQLQuery(accessToken);
    res.json(result);
  } catch (error: any) {
    console.error('Error during OAuth callback:', error);
    res.status(500).json({ error: 'Failed to obtain access token', details: error.message });
  }
});

async function performGraphQLQuery(accessToken: string): Promise<any> {
  try {
    const client = createGraphQLClient(accessToken);

    // Step 1: Retrieve hubs
    const hubsResult = await getHubs(client);
    const hubs = hubsResult.hubs?.results;

    if (!hubs || hubs.length === 0) {
      return { error: 'No hubs found or access denied.' };
    }

    // Print available hubs
    console.log('Available Hubs:');
    hubs.forEach((hub: any, index: number) => {
      console.log(`${index + 1}. Hub ID: ${hub.id}, Name: ${hub.name}`);
    });

    // Step 2: Select a hub ID (using the first hub)
    const hubId = hubs[0].id;
    console.log(`Using Hub ID: ${hubId}`);

    // Step 3: Query projects using the selected hub ID
    const projectsResult = await getProjects(client, hubId);
    const projects = projectsResult.hub?.projects?.results;

    if (!projects || projects.length === 0) {
      return { error: `No projects found in hub ${hubId}.` };
    }

    return projectsResult;
  } catch (error: any) {
    console.error('Error during GraphQL query:', error);
    return { error: 'An error occurred during the GraphQL query', details: error.message };
  }
}

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
