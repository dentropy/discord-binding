import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

async function main() {
  const channels = await prisma.attachments_t.findMany()
  console.log(channels)

}

main()
  .then(async () => {
    await prisma.$disconnect()
  })
  .catch(async (e) => {
    console.error(e)
    await prisma.$disconnect()
    process.exit(1)
  })