const { GraphQLObjectType, GraphQLSchema } = require('graphql');
const projectQueries = require('./queries/projectQueries');

const RootQuery = new GraphQLObjectType({
  name: 'RootQueryType',
  fields: {
    ...projectQueries,
  },
});

module.exports = new GraphQLSchema({
  query: RootQuery,
});
