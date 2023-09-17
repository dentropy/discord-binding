export const typeDefs = `#graphql
  type Query {
    channel: [Channel]
    guild: [Guild]
    message: [Message],
    attachment: [Attachment]
  }
  
  type Channel {
    id:           Int!,
    channel_id:   String,
    channel_name: String,
    channel_type: String,
    categoryId:   String,
    category:     String,
    guild_id:     String,
    topic:        String
  }

  type Guild {
    id:         Int!,
    guild_id:   String,
    guild_name: String,
    iconUrl:    String,
  }

  type Message {
    id:              Int!,
    message_id:      String,
    attachments:     String,
    author:          String,
    channel_id:      String,
    content:         String,
    interaction:     String,
    isBot:           Boolean,
    isPinned:        Boolean,
    mentions:        Boolean,
    msg_type:        String,
    timestamp:       Int,
    timestampEdited: Int
  }

  type Attachment {
    id:                  Int!,
    attachment_id:       String,
    attachment_url:      String,
    attachment_filename: String,
    fileSizeBytes:       Int,
    message_id:          String
  }
`