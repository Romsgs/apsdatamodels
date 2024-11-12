const {
  GraphQLObjectType,
  GraphQLID,
  GraphQLString,
} = require('graphql');

const ProjectType = new GraphQLObjectType({
  name: 'Project',
  fields: () => ({
    id: { type: GraphQLID },
    name: { type: GraphQLString },
    // Adicione outros campos conforme necessário
  }),
});

module.exports = ProjectType;
