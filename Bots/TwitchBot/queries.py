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
