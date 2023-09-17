import { ApolloServer } from '@apollo/server'
import { startStandaloneServer } from '@apollo/server/standalone'
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()
import { typeDefs } from './schema.js'


// resolvers
const resolvers = {
  Query: {
    async channel() {
      const query_result = await prisma.channels_t.findMany()
      return query_result
    },
    async guild() {
      const query_result = await prisma.guilds_t.findMany()
      return query_result
    },
    async message() {
      const query_result = await prisma.messages_t.findMany()
      return query_result
    },
    async attachment() {
      const query_result = await prisma.attachments_t.findMany()
      return query_result
    },
  }
  // Channel : {
  //   async channels() {
  //     const query_result = await prisma.channels_t.findMany()
  //     return query_result
  //   },
  // },
  // Guild : {
  //   async guilds(parent) {
  //     const query_result = await prisma.guilds_t.findMany()
  //     return query_result
  //   },
  // },
  // Message : {
  //   async messages() {
  //     const query_result = await prisma.messages_t.findMany()
  //     return query_result
  //   },
  // },
  // Attachment : {
  //   async attachments() {
  //     const query_result = await prisma.attachments_t.findMany()
  //     return query_result
  //   },
}

// server setup
const server = new ApolloServer({
  typeDefs,
  resolvers
})

const { url } = await startStandaloneServer(server, {
  listen: { port: 4000 }
})

console.log(`Server ready at: ${url}`)