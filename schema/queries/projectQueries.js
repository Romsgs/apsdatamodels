const { GraphQLList } = require('graphql');
const ProjectType = require('../types/ProjectType');
const apiService = require('../../services/apiService');

const projectQueries = {
  projects: {
    type: new GraphQLList(ProjectType),
    resolve: async () => {
      const projects = await apiService.getProjects();
      return projects;
    },
  },
};

module.exports = projectQueries;
