from bs4 import BeautifulSoup
import requests
import csv

# Get the league
code = input("Please enter your league's code (i.e. Premier League's code is GB1): ")
link = "https://www.transfermarkt.com/super-lig/startseite/wettbewerb/" + code

# Send a request to the league's page in Transfermarkt
super_lig = requests.get(link)
league_soup = BeautifulSoup(super_lig.text, "html.parser")

# Find all teams on the page
team_elements = league_soup.findAll("td", attrs={"class": "no-border-links hauptlink"})

# Create and open the CSV file
f = open("rotations.csv", "w", newline='', encoding='utf-8')
position_row = csv.writer(f)

# Write the headers in the CSV file
position_row.writerow(["TEAM", "PLAYER", "POSITION"])

# Loop through each team element
for team in team_elements:
    team_name = team.find("a").text.strip()
    team_link = team.find("a")["href"]
    full_link = "https://www.transfermarkt.com" + team_link

    # Request the team page to extract players
    team_request = requests.get(full_link)
    team_soup = BeautifulSoup(team_request.text, "html.parser")
    
    # Adjust this selector based on the structure on the team page
    player_elements = team_soup.findAll("a", class_="hauptlink")  # Update this class if different
    
    for player in player_elements:
        player_name = player.text.strip()
        player_link = player["href"]
        player_full_link = "https://www.transfermarkt.com" + player_link

        # Request the player's page to extract the position
        player_request = requests.get(player_full_link)
        player_soup = BeautifulSoup(player_request.text, "html.parser")
        
        # Extract player's position(s)
        positions = player_soup.findAll("dd", class_="detail-position__position")  # Use correct class here
        
        # If a player has multiple positions, handle all of them
        if positions:
            for position in positions:
                position_row.writerow([team_name, player_name, position.text.strip()])
        else:
            # In case the position isn't found (edge case handling)
            position_row.writerow([team_name, player_name, "Position not found"])

# Close the file
f.close()
