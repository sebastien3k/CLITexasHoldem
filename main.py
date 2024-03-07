import random
import time
import os

def print_red(text):
    print(f"\033[91m{text}\033[0m")

def print_green(text):
    print(f"\033[92m{text}\033[0m")

def print_yellow(text):
    print(f"\033[93m{text}\033[0m")

def print_blue(text):
    print(f"\033[94m{text}\033[0m")

def print_magenta(text):
    print(f"\033[95m{text}\033[0m")

def print_cyan(text):
    print(f"\033[96m{text}\033[0m")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def loading_animation(duration):
    animation = ['-', '\\', '|', '/']
    end_time = time.time() + duration
    while time.time() < end_time:
        for frame in animation:
            print(f"\rLoading {frame}", end='', flush=True)
            time.sleep(0.1)
    print("\rLoading complete!")

loading_animation(2)  # Display loading animation for 2 seconds

print_red("Hello World")
# Define the suits and values
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Create the deck of cards
deck = [{'suit': suit, 'value': value} for suit in suits for value in values]

class Pot:
    def __init__(self):
        self.amount = 0

    def add_bet(self, amount):
        self.amount += amount

    def deposit_winnings(self, player):
        player.add_winnings(self.amount)
        self.amount = 0

    def split_winnings(self, player1, player2):
        player1.add_winnings(self.amount // 2)
        player2.add_winnings(self.amount // 2)
        self.amount = 0


class Player:
    def __init__(self, name, total_amount):
        self.name = name
        self.total_amount = total_amount
        # KEEP TRACK OF TOTAL BETTED EACH ROUND FOR CALLING LOGIC
        self.total_betted = 0
        self.raise_counter = 0

    def place_bet(self, amount):
        if amount <= self.total_amount:
            self.total_amount -= amount
            self.total_betted += amount
            return amount
        else:
            print(f"{self.name} does not have enough funds to place the bet.")
            return 0

    def add_to_raise_counter(self):
        self.raise_counter += 1

    def add_winnings(self, amount):
        self.total_amount += amount
        return amount

    def assign_cards(self, cards):
        self.cards = cards

    def reset_total_betted(self):
        self.total_betted = 0

    def reset_raise_counter(self):
        self.raise_counter = 0
        return 0 

def draw_cards(num_cards):
    """
    Draws a specified number of cards from the deck without replacement.
    Returns a list of dictionaries representing the drawn cards.
    """
    drawn_cards = random.sample(deck, num_cards)
    for card in drawn_cards:
        deck.remove(card)
    return drawn_cards

def determine_winner(player1, player2, community_cards):
    # Concatenate the player's hole cards with the community cards
    player1_hand = player1.cards + community_cards
    player2_hand = player2.cards + community_cards

    print(player1_hand)
    print(player2_hand)
    # Determine the best hand for each player using a poker hand evaluation function
    player1_best_hand = evaluate_hand(player1_hand)
    player2_best_hand = evaluate_hand(player2_hand)

    # Compare the hands and declare the winner
    if player1_best_hand > player2_best_hand:
        print(player1_best_hand)
        print(player2_best_hand)
        return player1.name
    elif player1_best_hand < player2_best_hand:
        print(player1_best_hand)
        print(player2_best_hand)
        return player2.name
    elif player1_best_hand == 2 and player2_best_hand == 2:
        p1_pair_card = get_pair_value(player1_hand)
        p2_pair_card = get_pair_value(player2_hand)
        if p1_pair_card > p2_pair_card:
            return player1.name
        elif p2_pair_card > p1_pair_card:
            return player2.name
        else:
            return "Tie"
    else:
        print(player1_best_hand)
        print(player2_best_hand)
        # Get the high card for each player
        player1_high_card = get_high_card(player1.cards)
        player2_high_card = get_high_card(player2.cards)
        print(player1_high_card)
        print(player2_high_card)
        # Compare high cards
        if player1_high_card > player2_high_card:
            return player1.name
        elif player1_high_card < player2_high_card:
            return player2.name
        else:
            return "Tie"

def evaluate_hand(hand):
    # Separate the hand into values and suits
    values = [card['value'] for card in hand]
    suits = [card['suit'] for card in hand]

    print(values)
    print(suits)
    # Check for specific hand types in decreasing order of strength
    if is_straight_flush(values, suits):
        return 9  # Straight Flush
    elif is_four_of_a_kind(values):
        return 8  # Four of a Kind
    elif is_full_house(values):
        return 7  # Full House
    elif is_flush(suits):
        return 6  # Flush
    elif is_straight(values):
        return 5  # Straight
    elif is_three_of_a_kind(values):
        return 4  # Three of a Kind
    elif is_two_pair(values):
        return 3  # Two Pair
    elif is_pair(values):
        return 2  # One Pair
    else:
        return 1  # High Card

# Example helper functions for checking hand types (you need to implement these): # PROBABLY NEED TO UPDATE / TEST STRAIGHT FLUSH 
def is_straight_flush(values, suits):
    # Check if the hand is a straight flush
    # ...
    for suit in suits:
        if suits.count(suit) == 5:
            # Define the order of card values
            card_order = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

            # Convert the card values to their corresponding indices in the card_order list
            indices = [card_order.index(card) for card in values]

            # Remove duplicate indices
            unique_indices = list(set(indices))

            # Sort the unique indices in ascending order
            unique_indices.sort()

            # Check for consecutive indices
            for i in range(len(unique_indices) - 4):
                if unique_indices[i+4] - unique_indices[i] == 4:
                    return True

            # Check for the special case of 'A', '2', '3', '4', '5'
            if set(values) >= set(['A', '2', '3', '4', '5']):
                return True

            return False
        else:
            return False

def is_four_of_a_kind(values):
    # Check if the hand is four of a kind
    # ...
    for value in values:
        if values.count(value) == 4:
            return True
    return False

def is_full_house(values):
    # Check if the hand is a full house

    for value in values:
        if values.count(value) == 3:
            for value in values:
                if values.count(value) == 2:
                    return True

    return False

def is_flush(suits):
    # Check if the hand is a flush

    for suit in suits:
        if suits.count(suit) == 5:
            return True

    return False

def is_straight(values):
    # Check if the hand is a straight

    # Define the order of card values
    card_order = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    # Convert the card values to their corresponding indices in the card_order list
    indices = [card_order.index(card) for card in values]

    # Remove duplicate indices
    unique_indices = list(set(indices))

    # Sort the unique indices in ascending order
    unique_indices.sort()

    # Check for consecutive indices
    for i in range(len(unique_indices) - 4):
        if unique_indices[i+4] - unique_indices[i] == 4:
            return True

    # Check for the special case of 'A', '2', '3', '4', '5'
    if set(values) >= set(['A', '2', '3', '4', '5']):
        return True

    return False

def is_three_of_a_kind(values):
    # Check if the hand has three of a kind
    for value in values:
        if values.count(value) == 3:
            return True
    return False

def is_two_pair(values):
    # Check if the hand is two pair

    unique_values = set(values)
    if len(unique_values) == 5 or len(unique_values) == 4:
        return True

    return False

def is_pair(values):
    # Check if the hand is a pair

    unique_values = set(values)
    if len(unique_values) == 6:
        return True

    return False

def get_pair_value(values):
    # Extract the 'value' field from each card dictionary
    card_values = [card['value'] for card in values]

    # Map face cards to corresponding numeric values
    value_map = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}

    # Convert non-numeric values to integers using the value_map
    converted_values = [value_map.get(value, value) for value in card_values]

    # Filter out numeric values to prevent conversion errors
    converted_values = [int(value) if isinstance(value, str) else value for value in converted_values]

    # Count occurrences of each number
    counts = {num: converted_values.count(num) for num in set(converted_values)}

    # Check for a pair
    pair_value = None
    for num, count in counts.items():
        if count == 2:
            pair_value = num
            break

    if pair_value is not None:
        return pair_value
    else:
        # If no pair is found, return the highest number
        return max(converted_values)

def get_high_card(values):
    # Get the high card from the values in the hand

    # Extract the 'value' field from each card dictionary
    card_values = [card['value'] for card in values]

    # Map face cards to corresponding numeric values
    value_map = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}

    # Convert non-numeric values to integers using the value_map
    converted_values = [value_map.get(value, value) for value in card_values]

    # Filter out numeric values to prevent conversion errors
    converted_values = [int(value) if isinstance(value, str) else value for value in converted_values]

    # Return the maximum value in the hand
    return max(converted_values)



### GAMEPLAY FUNCTIONS ###


def player_turn(check_count, still_playing, minimum_bet):
    print("Your turn...")
    # print(player1.raise_counter)
    if player1.raise_counter == 0:
        round1 = input("Enter c to check or call, r to raise and f to fold")
    elif player1.raise_counter >= 1:
        round1 = input("Enter c to check or call and f to fold")
    if round1.lower() == 'f':
        print("You folded!")
        print(f"Player 2 won ${pot.amount}!")
        pot.deposit_winnings(player2)
        still_playing = False
        return check_count, still_playing, minimum_bet
    elif round1.lower() == 'c':
        # VERIFY PLAYER 2 TOTAL_BETTED IS LESS THAN MINIMUM BET (LATEST RAISE) THEN AUTO-CALL
        if player1.total_betted < player2.total_betted:
            current_call = player2.total_betted - player1.total_betted
            player1.place_bet(current_call)
            print("You called.")
            print(f"Player 1 remaining balance: ${player1.total_amount}")
            pot.add_bet(current_call)
            print(f"Pot amount: {pot.amount}")
            time.sleep(1)
            return check_count, still_playing, minimum_bet
        elif player1.total_betted >= player2.total_betted:
            print("You checked")
            check_count = check_count + 1
            print(check_count)
            return check_count, still_playing, minimum_bet
    elif round1.lower() == 'r' and player1.raise_counter == 0:
        raise_amount = input(f"How much would you like to raise? The minimum bet is ${minimum_bet}: \n")
        print(f"Raising {raise_amount}.")
        player1.add_to_raise_counter()
        integer_raise = int(raise_amount)
        minimum_bet = integer_raise
        latest_raise = integer_raise
        player1.place_bet(integer_raise)
        print(f"Player 1 remaining balance: ${player1.total_amount}")
        pot.add_bet(integer_raise)
        print(f"Pot amount: {pot.amount}")
        return check_count, still_playing, minimum_bet
    # Add a default return statement for other inputs
    print("Invalid input. Please enter 'c', 'r', or 'f'.")
    return check_count, still_playing, minimum_bet

def opponent_turn(check_count, still_playing, minimum_bet):
    print("Opponent's Turn...")
    if random.random() < call_freq_probability and player2.total_betted < player1.total_betted:
        current_call = player1.total_betted - player2.total_betted
        player2.place_bet(current_call)
        print("Opponent called")
        print(f"Player 2 remaining balance: ${player2.total_amount}")
        pot.add_bet(current_call)
        print(f"Pot amount: {pot.amount}")
        time.sleep(1)
        return check_count, still_playing, minimum_bet
    elif player2.total_betted >= player1.total_betted:
        print("Opponent checked")
        check_count = check_count + 1
        print(check_count)
        return check_count, still_playing, minimum_bet
    elif random.random() < raise_freq_probability and player2.total_betted == player1.total_betted and player2.raise_counter == 0:
        player2.place_bet(minimum_bet)
        print("Opponent raised")
        print(f"Player 2 total amount: {player2.total_amount}")
        pot.add_bet(minimum_bet)
        print(f"Pot amount: {pot.amount}")
        latest_raise = minimum_bet
        return check_count, still_playing, minimum_bet
    else:
        print("Opponent Folded!")
        print(f"Player 1 won ${pot.amount}!")
        pot.deposit_winnings(player1)
        still_playing = False
        return check_count, still_playing, minimum_bet

def preflop():
    # Logic for preflop betting round
    # RESET TOTAL BETTED COUNTERS FOR CALLING LOGIC
    player1.reset_total_betted()
    player2.reset_total_betted()

    # RANDOM DEALER COIN SELECT
    dealer_coin = random.choice(available_players)
    print("Randomly selecting dealer coin...")
    time.sleep(2)
    print(f"{dealer_coin.name} selected...")
    time.sleep(1)

    # BLIND ASSIGNMENT
    dealer_index = available_players.index(dealer_coin)
    big_blind_player = dealer_coin
    small_blind_player = available_players[(dealer_index + 1) % len(available_players)]

    # PLACE BLINDS
    print(f"{small_blind_player.name} is small blind...")
    time.sleep(1)
    print(f"{dealer_coin.name} is big blind...")
    time.sleep(1)
    small_blind_amount = small_blind_player.place_bet(small_blind)
    big_blind_amount = big_blind_player.place_bet(big_blind)
    pot.add_bet(big_blind_amount)
    pot.add_bet(small_blind_amount)

    # STATE CHECK (PREROUND STATUS)
    print(f"Player 1 total amount: {player1.total_amount}")
    print(f"Player 2 total amount: {player2.total_amount}")
    print(f"Pot amount: {pot.amount}")
    print()

    print("Initial deck size:", len(deck))

    # DEAL CARDS
    player_cards = draw_cards(2)
    player1.assign_cards(player_cards)
    print(player_cards)
    print("Player's cards:")
    for card in player_cards:
        print(f"{card['value']} of {card['suit']}")

    # print("Deck size after drawing:", len(deck))
    opponents_cards = draw_cards(2)
    player2.assign_cards(opponents_cards)
    print("Opponent dealt cards...")

    # RESET MINIMUM BET TO BIG BLIND EACH NEW ROUND
    return dealer_coin

def deal_flop():
    community_cards = []
    flop_cards = draw_cards(3)
    for card in flop_cards:
        print(f"{card['value']} of {card['suit']}")
    community_cards.extend(flop_cards if flop_cards else [])
    # Logic to deal flop cards
    return community_cards

def deal_turn(community_cards):
    turn_card = draw_cards(1)
    for card in turn_card:
        print(f"{card['value']} of {card['suit']}")
    community_cards.extend(turn_card if turn_card else [])
    return community_cards
    # Logic to deal turn card  

def deal_river(community_cards):
    river_card = draw_cards(1)
    for card in river_card:
        print(f"{card['value']} of {card['suit']}")
    community_cards.extend(river_card if river_card else [])
    return community_cards
    # Logic to deal river card

def show_hands(player1, player2, community_cards):
    player_cards = player1.cards
    opponents_cards = player2.cards
    for card in player_cards:
        print(f"{card['value']} of {card['suit']}")
    print("Opponent's cards:")
    for card in opponents_cards:
        print(f"{card['value']} of {card['suit']}")
    print("Community cards:")
    for card in community_cards:
        print(f"{card['value']} of {card['suit']}")

def betting_round(dealer_coin, round_name):
    check_count = 0
    still_playing = True
    player1.reset_raise_counter()
    player2.reset_raise_counter()
    minimum_bet = big_blind
    # CURRENTLY MISSING MINIMUM BET LOGIC BELIEVE THIS SHOULD RAISE AND CARRY OVER INTO NEW ROUNDS INSTEAD OF RESETING TO BIG BLIND EVERY ROUND

    print(f"Starting {round_name} betting round...")

    while True:
        print("Starting left of dealer coin...")
        # print(f"{small_blind_player.name}'s Turn")
        if dealer_coin.name == "Player 1":
            check_count, still_playing, minimum_bet = opponent_turn(check_count, still_playing, minimum_bet)
            if check_count == 2 or still_playing == False:
                return check_count, still_playing
            check_count, still_playing, minimum_bet = player_turn(check_count, still_playing, minimum_bet)
            if check_count == 2 or still_playing == False:
                return check_count, still_playing
        elif dealer_coin.name == "Player 2":
            check_count, still_playing, minimum_bet = player_turn(check_count, still_playing, minimum_bet)
            if check_count == 2 or still_playing == False:
                return check_count, still_playing
            check_count, still_playing, minimum_bet = opponent_turn(check_count, still_playing, minimum_bet)
            if check_count == 2 or still_playing == False:
                return check_count, still_playing

# '♠️','♥️','♦️','♣️'
# TESTING A

# PREGAME SETUP
# Initialize the pot and players
pot = Pot()
player1 = Player("Player 1", 100)
player2 = Player("Player 2", 100)
available_players = [player1, player2]
community_cards = []
latest_raise = 0

# TEMP POT RESET UNTIL POT WINNING LOGIC IMPLEMENTED
pot.amount = 0

small_blind = 5
big_blind = 10

still_playing = True
flop_cards = False
turn_card = False
river_card = False

# GAME AI
call_freq_probability = 0.67
raise_freq_probability = 0.40

while True:
    if player1.total_amount < small_blind:
        print("Player 1 is out of funds!")
        break
    elif player2.total_amount < small_blind:
        print("Player 2 is out of funds!")
        break
    # "SHUFFLE" DECK (CREATE NEW DECK EACH ROUND)
    deck = [{'suit': suit, 'value': value} for suit in suits for value in values]

    dealer_coin = preflop()
    check_count, still_playing = betting_round(dealer_coin, "Preflop")
    if still_playing and check_count == 2:
        community_cards = deal_flop()
        check_count, still_playing = betting_round(dealer_coin, "Flop")
        if still_playing and check_count == 2:
            community_cards = deal_turn(community_cards)
            check_count, still_playing = betting_round(dealer_coin, "Turn")
            if still_playing and check_count == 2:
                community_cards = deal_river(community_cards)
                check_count, still_playing = betting_round(dealer_coin, "River")
                if check_count == 2:
                    # show_hands(player1, player2, community_cards)
                    winner = determine_winner(player1, player2, community_cards)
                    if winner != "Tie":
                        winner_player = player1 if winner == player1.name else player2
                        print(f"{winner_player.name} won ${pot.amount}")
                        pot.deposit_winnings(winner_player)
                    else:
                        # Handle tie scenario (if needed)
                        print("Tie, pot is split!")
                        pot.split_winnings(player1, player2)
                    choice = input("Enter 'c' to continue or any other key to exit: ")
                    if choice.lower() != 'c':
                        break
    else:
        choice = input("Enter 'c' to continue or any other key to exit: ")
        if choice.lower() != 'c':
            break

print("Game ended.")