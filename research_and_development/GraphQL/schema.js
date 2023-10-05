export const typeDefs = `#graphql

enum OrderByChannelField {
    channel_name
  }
  enum OrderByGuildField {
    guild_name
  }
  enum OrderByMessageField {
    timestamp
  }
  enum OrderByAttachmentField {
  	attachment_filename
  	fileSizeBytes
  }
  enum OrderByAuthorField {
  	name
  	nickname
  }
  enum OrderByDirection {
    asc
    desc
  }
  input OrderByChannelInput {
    field: OrderByChannelField!
    direction: OrderByDirection!
  }
  input OrderByGuildInput {
    field: OrderByGuildField!
    direction: OrderByDirection!
  }
  input OrderByMessageInput {
    field: OrderByMessageField!
    direction: OrderByDirection!
  }
  input OrderByAttachmentInput {
    field: OrderByAttachmentField!
    direction: OrderByDirection!
  }
  input OrderByAuthorInput {
    field: OrderByAuthorField!
    direction: OrderByDirection!
  }

  type Query {
    channel(orderBy: OrderByChannelInput): [Channel]
    guild(orderBy: OrderByGuildInput): [Guild]
    message(orderBy: OrderByMessageInput): [Message],
    attachment(orderBy: OrderByAttachmentInput): [Attachment]
    author(orderBy: OrderByAuthorInput): [Author]
  }
  

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

  type Author {
    id:        Int!,
    author_id: String,
    name:      String,
    nickname:  String,
    color:     String,
    isBot:     Boolean,
    avatarUrl: String
  }
`