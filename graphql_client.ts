// graphql_client.ts
import { GraphQLClient, gql } from 'graphql-request';

const GRAPHQL_URL = 'https://developer.api.autodesk.com/graphql';

export function createGraphQLClient(accessToken: string): GraphQLClient {
  return new GraphQLClient(GRAPHQL_URL, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
  });
}

export async function getHubs(client: GraphQLClient): Promise<any> {
  const query = gql`
    query GetHubs {
      hubs {
        pagination {
          cursor
        }
        results {
          id
          name
        }
      }
    }
  `;
  return client.request(query);
}

export async function getProjects(
  client: GraphQLClient,
  hubId: string
): Promise<any> {
  const query = gql`
    query GetProjects($hubId: ID!) {
      hub(id: $hubId) {
        projects {
          pagination {
            cursor
          }
          results {
            id
            name
          }
        }
      }
    }
  `;
  const variables = { hubId };
  return client.request(query, variables);
}
