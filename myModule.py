import httpx

def postGameResults(gameResult):

    try:
        req = httpx.post("the url leaderboard serice ir running goes here", data=gameResult)
    except Exception as e:
        print("error occured posting result to the leaderboard service")
    
    return 0

    # json={'username': gameResult["username"], "gameStatus": gameResult["gamestatus"], "guesscount": gameResult["guesscount"]}