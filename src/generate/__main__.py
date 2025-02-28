"""Generate lichess bot leaderboards for each time control and variant.

Process for generating the leaderboards:
 - Call the lichess `get online bots` API (https://lichess.org/api/bot/online)
 - Parse the response into collection of bots and ratings
 - Create leaderboards which are fun to look at
"""

if __name__ == "__main__":
  print("Generating...")
