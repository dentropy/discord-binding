import { ApolloServer } from '@apollo/server'
import { startStandaloneServer } from '@apollo/server/standalone'
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()
import { typeDefs } from './schema.js'


// resolvers
const resolvers = {
  Query: {
    async channel(_, { orderBy }) {
      let prisma_table = prisma.channels_t
      if(orderBy){
        let query_input = {
          orderBy: [
            {
              [orderBy.field] : orderBy.direction
            }
          ]
        }
        const query_result = await prisma_table.findMany(query_input)
        return query_result
      }
      const query_result = await prisma_table.findMany()
      return query_result
    },
    async guild(_, { orderBy }) {
      let prisma_table = prisma.guilds_t
      if(orderBy){
        let query_input = {
          orderBy: [
            {
              [orderBy.field] : orderBy.direction
            }
          ],
          where: {},
          distinct: ['guild_id'],
        }
        const query_result = await prisma_table.findMany(query_input)
        return query_result
      }
      const query_result = await prisma_table.findMany({
        where: {},
        distinct: ['guild_id'],
      })
      return query_result
    },
    async message(_, { orderBy }) {
      let prisma_table = prisma.messages_t
      if(orderBy){
        let query_input = {
          orderBy: [
            {
              [orderBy.field] : orderBy.direction
            }
          ]
        }
        const query_result = await prisma_table.findMany(query_input)
        return query_result
      }
      const query_result = await prisma_table.findMany()
      return query_result
    },
    async attachment(_, { orderBy }) {
      let prisma_table = prisma.attachments_t
      if(orderBy){
        let query_input = {
          orderBy: [
            {
              [orderBy.field] : orderBy.direction
            }
          ]
        }
        const query_result = await prisma_table.findMany(query_input)
        return query_result
      }
      const query_result = await prisma_table.findMany()
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