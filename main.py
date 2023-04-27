import requests
from bs4 import BeautifulSoup
import random
import re

def listPopular(num):
    if num == None:
        num = 1
    url = "https://www.backloggd.com/games/lib/popular?page="
    num = str(num).strip()
    url += num
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    games = []

    gameElements = soup.findAll('div', class_='game-text-centered')
    [games.append(game.text.lstrip()) for game in gameElements]
    
    return games

def findRandom():
    randNum = random.randint(1, 3500)
    games = listPopular(randNum)
    randGame = games[randNum % len(games)-1]

    #DELETE. FOR TESTING
    print("Before: " + randGame)

    randGame = randGame.lower()
    re.sub(r"[^a-zA-Z0-9\s]", '', randGame)

    #THIS sucks
    randGame = randGame.replace(" ", '-')
    randGame = randGame.replace(':', '')
    randGame = randGame.replace('/', '')
    randGame = randGame.replace('&', "and")
    randGame = randGame.replace('!', '')
    randGame = randGame.replace('.', '')

    #DELETE. FOR TESTING
    print("after: " + randGame)

    findGame(randGame)

def findGame(gameTitle):
    # URL of the page to scrape
    url = "https://www.backloggd.com/games/"
    url += gameTitle

    #DELETE. FOR TESTING
    print(url)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the title of the game
    titleElement = soup.find('div', attrs={'id': 'title'}).find('h1', attrs={'class' : 'mb-0'})
    title = titleElement.text.strip()

    #Find release date of the game
    releaseDateElement = soup.find('div', attrs={'id':'title'}).find('span', attrs={'class':'sub-title'}).find('a')
    releaseDate = releaseDateElement.text.strip()

    #Find developers
    studio = []
    studioElement = soup.find('div', attrs={'class':'col-auto pl-lg-1 sub-title'})
    if studioElement is not None:
        studioElement = soup.find('div', attrs={'class':'col-auto pl-lg-1 sub-title'}).findAll('a')
        [studio.append(text.text) for text in studioElement]

    #Find summary and score
    score = soup.find('div', attrs={'id':'score'}).find('h1').text
    summary = soup.find('div', attrs={'id':'collapseSummary'}).find('p').text

    #Find platforms
    platformElements = soup.findAll('a', class_='game-page-platform')
    platforms = []
    [platforms.append(platform.text.lstrip()) for platform in platformElements]

    #Find genres
    genreElements = soup.findAll('p', class_='genre-tag')
    genres = []
    [genres.append(genre.text.lstrip()) for genre in genreElements]

    # Print the game details
    print('\n')
    print("Title:", title)
    print("Released on:", releaseDate)


    #Print studio / producers
    if len(studio) == 0:
        print("By: N/A")
    elif len(studio) == 1:
        print("By:", studio[0])
    else:
        print("By:", end=" ")
        for _ in range(0, len(studio)-1):
            print(studio[_] + ',', end=" ")
        print(studio[-1])

    print("Average score:", score)
    #Print genres
    if len(genres) == 0:
        print("Genres: N/A")
    elif len(genres)==1:
        print("Genres:", genres[0])
    else:
        print("Genres:", end=" ")
        for _ in range(0, len(genres)-1):
            print(genres[_] + ",", end=" ")
        print(genres[-1])

    print("\nSummary:", summary)

    #Print platforms
    if len(platforms) == 1:
        print("\nPlatforms:", platforms[0])
    else:
        print("\nPlatforms:", end=" ")
        for _ in range(0, len(platforms)-1):
            print(platforms[_] + ',', end=" ")
        print(platforms[-1])
    print("\n")


#Main loop
while True:
    
    userInput = input("Enter a command ('h' for help or 'exit' to quit)\n")
    userInput = userInput.lower()

    if userInput == "exit" or userInput == "quit":
        break
    elif userInput == "h" or userInput == "help":
        print("\nCommands:")
        print("h or help: Brings up this menu")
        print("'quit' or 'exit': Exits the program")
        print("'search <game-title>': Searches for the game with the title inputed")
        print("'list <page-number>': Prints list of 36 games ranked by popularity. Pages range from 1 to 3644")
        print("If title is incorrect, make sure that you are ommitting special characters and check spelling for correctness.")
        print("Some games, especially installments in a series will have sub-titles that must be entered as well.\n")
        print("An example input for a title: 'search Elden Ring' or 'search marvels spider man miles morales\n")
    elif userInput[:6] == "search":
        title = userInput[7:]
        title = title.lower()
        title = title.strip()
        title = title.replace(" ", '-')
        title += '/'
        try:
            findGame(title)
        except Exception:
            print("Something went wrong, please check spelling and omit special characters from game title.")
    elif userInput == "random":
        findRandom()
    elif userInput[:4] == "list":
        num = 1
        try:
            num = userInput[5:]
            num = int(num)
            if(num < 1 or num > 3644):
                print("Number must be in range 1 - 3644")
                continue
        except Exception:
            print("Please enter input as 'list <number>'. Number must be in range 1 - 3644.")
        try:
            games = listPopular(num)
            i = 1 if int(num) == 1 else 36*(int(num)-1)+1
            for game in games:
                print(str(i) + ".", end=" ")
                print(game)
                i += 1
        except Exception:
            print("Something went wrong")

    else:
        print("Not a command")


print("Exiting...")