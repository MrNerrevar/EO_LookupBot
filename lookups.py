import requests


def fetch_all_players():
    url = 'https://eodash.com/api/players'
    response = requests.get(url)

    # Ensure response is valid
    if response.status_code == 200:
        data = response.json()
        return data.get('players', [])
    else:
        print(f'Failed to fetch data. Status code: {response.status_code}')
        return None


def find_player_by_name(players, player_name):
    for player in players:
        if player.get('name', '').lower() == player_name.lower():
            return player
    print(f'Player "{player_name}" not found.')
    return None


def compare_players(player_name1, player_name2):
    players = fetch_all_players()

    if players:
        player1 = find_player_by_name(players, player_name1)
        player2 = find_player_by_name(players, player_name2)

        player1_name = player1["name"]
        player2_name = player2["name"]

        if player1 and player2:
            exp1 = player1.get('exp', 0)
            exp2 = player2.get('exp', 0)

        return player1_name, exp1, player2_name, exp2


def print_player_info(player_name):
    players = fetch_all_players()

    if players:
        player = find_player_by_name(players, player_name)
        if player:
            name = player['name']
            level = player['level']
            exp = player['exp']
            rank = player['rank']
            return name, level, exp, rank
