query_leaderboard = (
    '''
    query getLeaderboard($metric: String!){
        leaderboard(metric: $metric){
            displayName
            minutesWatched
            loyaltyPoints
            }
        }
    '''
)

query_twitch_user = (
    '''
    query GetTwitchUser($username: String!) {
        twitchUser(username: $username){
          twitchId
          login
          displayName
          type
          broadcasterType
          description
          profileImageUrl
          offlineImageUrl
          viewCount
          followerCount
          subscriberCount
          messagesCount
          loyaltyPoints
          minutesWatched
          bot
          dateModified
          dateCreated
        }
      }
    '''
)
