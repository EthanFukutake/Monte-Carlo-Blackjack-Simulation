import random
import pandas as pd
import time


def shuffle_deck():
    # Initialize card numbers
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]

    # Muliply by 24 (4 for each suit then 6 for six decks)
    shoe = deck * 24

    # shuffle the shoe of decks
    random.shuffle(shoe)
    return shoe, 0


# Calculate the sum of a hand as well as account for going over with aces and changing them to 1
def calculate_hand(hand):
    total = sum(hand)
    aces = hand.count(11)

    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total


def is_soft_hand(hand):
    if 11 not in hand:
        return False

    total = sum(hand)
    aces = hand.count(11)

    # Convert aces to 1 until under 21
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    # If we still have an ace left as 11, it's soft
    return aces > 0

# Calculate if User has blackjack from the start
def is_blackjack(hand):
    return len(hand) == 2 and calculate_hand(hand) == 21


BASIC_STRATEGY = {
    # SOFT HANDS (negative to differentiate between HARD hands)
    (-13, 2): "HIT", (-13, 3): "HIT", (-13, 4): "DOUBLE", (-13, 5): "DOUBLE", (-13, 6): "DOUBLE", (-13, 7): "HIT", (-13, 8): "HIT", (-13, 9): "HIT", (-13, 10): "HIT", (-13, 11): "HIT",
    (-14, 2): "HIT", (-14, 3): "HIT", (-14, 4): "DOUBLE", (-14, 5): "DOUBLE", (-14, 6): "DOUBLE", (-14, 7): "HIT", (-14, 8): "HIT", (-14, 9): "HIT", (-14, 10): "HIT", (-14, 11): "HIT",
    (-15, 2): "HIT", (-15, 3): "HIT", (-15, 4): "DOUBLE", (-15, 5): "DOUBLE", (-15, 6): "DOUBLE", (-15, 7): "HIT", (-15, 8): "HIT", (-15, 9): "HIT", (-15, 10): "HIT", (-15, 11): "HIT",
    (-16, 2): "HIT", (-16, 3): "HIT", (-16, 4): "DOUBLE", (-16, 5): "DOUBLE", (-16, 6): "DOUBLE", (-16, 7): "HIT", (-16, 8): "HIT", (-16, 9): "HIT", (-16, 10): "HIT", (-16, 11): "HIT",
    (-17, 2): "DOUBLE", (-17, 3): "DOUBLE", (-17, 4): "DOUBLE", (-17, 5): "DOUBLE", (-17, 6): "DOUBLE", (-17, 7): "HIT", (-17, 8): "HIT", (-17, 9): "HIT", (-17, 10): "HIT", (-17, 11): "HIT",
    (-18, 2): "STAND", (-18, 3): "DOUBLE", (-18, 4): "DOUBLE", (-18, 5): "DOUBLE", (-18, 6): "DOUBLE", (-18, 7): "STAND", (-18, 8): "STAND", (-18, 9): "HIT", (-18, 10): "HIT", (-18, 11): "HIT",
    (-19, 2): "STAND", (-19, 3): "STAND", (-19, 4): "STAND", (-19, 5): "STAND", (-19, 6): "DOUBLE", (-19, 7): "STAND", (-19, 8): "STAND", (-19, 9): "STAND", (-19, 10): "STAND", (-19, 11): "STAND",
    (-20, 2): "STAND", (-20, 3): "STAND", (-20, 4): "STAND", (-20, 5): "STAND", (-20, 6): "STAND", (-20, 7): "STAND", (-20, 8): "STAND", (-20, 9): "STAND", (-20, 10): "STAND", (-20, 11): "STAND",

    # HARD HANDS
    (5, 2): "HIT", (5, 3): "HIT", (5, 4): "HIT", (5, 5): "HIT", (5, 6): "HIT", (5, 7): "HIT", (5, 8): "HIT", (5, 9): "HIT", (5, 10): "HIT", (5, 11): "HIT",
    (6, 2): "HIT", (6, 3): "HIT", (6, 4): "HIT", (6, 5): "HIT", (6, 6): "HIT", (6, 7): "HIT", (6, 8): "HIT", (6, 9): "HIT", (6, 10): "HIT", (6, 11): "HIT",
    (7, 2): "HIT", (7, 3): "HIT", (7, 4): "HIT", (7, 5): "HIT", (7, 6): "HIT", (7, 7): "HIT", (7, 8): "HIT", (7, 9): "HIT", (7, 10): "HIT", (7, 11): "HIT",
    (8, 2): "HIT", (8, 3): "HIT", (8, 4): "HIT", (8, 5): "DOUBLE", (8, 6): "DOUBLE", (8, 7): "HIT", (8, 8): "HIT", (8, 9): "HIT", (8, 10): "HIT", (8, 11): "HIT",
    (9, 2): "DOUBLE", (9, 3): "DOUBLE", (9, 4): "DOUBLE", (9, 5): "DOUBLE", (9, 6): "DOUBLE", (9, 7): "HIT", (9, 8): "HIT", (9, 9): "HIT", (9, 10): "HIT", (9, 11): "HIT",
    (10, 2): "DOUBLE", (10, 3): "DOUBLE", (10, 4): "DOUBLE", (10, 5): "DOUBLE", (10, 6): "DOUBLE", (10, 7): "DOUBLE", (10, 8): "DOUBLE", (10, 9): "DOUBLE", (10, 10): "HIT", (10, 11): "HIT",
    (11, 2): "DOUBLE", (11, 3): "DOUBLE", (11, 4): "DOUBLE", (11, 5): "DOUBLE", (11, 6): "DOUBLE", (11, 7): "DOUBLE", (11, 8): "DOUBLE", (11, 9): "DOUBLE", (11, 10): "DOUBLE", (11, 11): "DOUBLE",
    (12, 2): "HIT", (12, 3): "HIT", (12, 4): "STAND", (12, 5): "STAND", (12, 6): "STAND", (12, 7): "HIT", (12, 8): "HIT", (12, 9): "HIT", (12, 10): "HIT", (12, 11): "HIT",
    (13, 2): "STAND", (13, 3): "STAND", (13, 4): "STAND", (13, 5): "STAND", (13, 6): "STAND", (13, 7): "HIT", (13, 8): "HIT", (13, 9): "HIT", (13, 10): "HIT", (13, 11): "HIT",
    (14, 2): "STAND", (14, 3): "STAND", (14, 4): "STAND", (14, 5): "STAND", (14, 6): "STAND", (14, 7): "HIT", (14, 8): "HIT", (14, 9): "HIT", (14, 10): "HIT", (14, 11): "HIT",
    (15, 2): "STAND", (15, 3): "STAND", (15, 4): "STAND", (15, 5): "STAND", (15, 6): "STAND", (15, 7): "HIT", (15, 8): "HIT", (15, 9): "HIT", (15, 10): "HIT", (15, 11): "HIT",
    (16, 2): "STAND", (16, 3): "STAND", (16, 4): "STAND", (16, 5): "STAND", (16, 6): "STAND", (16, 7): "HIT", (16, 8): "HIT", (16, 9): "HIT", (16, 10): "HIT", (16, 11): "HIT",
    (17, 2): "STAND", (17, 3): "STAND", (17, 4): "STAND", (17, 5): "STAND", (17, 6): "STAND", (17, 7): "STAND", (17, 8): "STAND", (17, 9): "STAND", (17, 10): "STAND", (17, 11): "STAND",
    (18, 2): "STAND", (18, 3): "STAND", (18, 4): "STAND", (18, 5): "STAND", (18, 6): "STAND", (18, 7): "STAND", (18, 8): "STAND", (18, 9): "STAND", (18, 10): "STAND", (18, 11): "STAND",
    (19, 2): "STAND", (19, 3): "STAND", (19, 4): "STAND", (19, 5): "STAND", (19, 6): "STAND", (19, 7): "STAND", (19, 8): "STAND", (19, 9): "STAND", (19, 10): "STAND", (19, 11): "STAND",
    (20, 2): "STAND", (20, 3): "STAND", (20, 4): "STAND", (20, 5): "STAND", (20, 6): "STAND", (20, 7): "STAND", (20, 8): "STAND", (20, 9): "STAND", (20, 10): "STAND", (20, 11): "STAND",
    (21, 2): "STAND", (21, 3): "STAND", (21, 4): "STAND", (21, 5): "STAND", (21, 6): "STAND", (21, 7): "STAND", (21, 8): "STAND", (21, 9): "STAND", (21, 10): "STAND", (21, 11): "STAND",
}


def play_game(shoe, shoe_index, money, bet_amount):
    # Subtract bet
    money -= bet_amount

    # Initialize hands
    dealer_hand = []
    user_hand = []

    # Shuffle Shoe if count is less than 75 (Casinos typicaly shuffle when there are only 1-2 decks remaining in the shoe)
    if len(shoe) - shoe_index < 75:
        shoe, shoe_index = shuffle_deck()

    # Deal cards
    user_hand.append(shoe[shoe_index])
    shoe_index += 1

    dealer_hand.append(shoe[shoe_index])
    shoe_index += 1

    user_hand.append(shoe[shoe_index])
    shoe_index += 1

    dealer_face_down_card = shoe[shoe_index]
    shoe_index += 1
    dealer_hand.append('X')

    # Check for blackjack
    user_blackjack = is_blackjack(user_hand)
    dealer_blackjack = is_blackjack(dealer_hand[:1] + [dealer_face_down_card])

    if user_blackjack and dealer_blackjack:
        money += bet_amount
        return shoe, shoe_index, money, "push"
    elif user_blackjack:
        money += int(bet_amount * 2.5)
        return shoe, shoe_index, money, "blackjack"
    elif dealer_blackjack:
        return shoe, shoe_index, money, "loss"

    # Check if we should split
    hands = [user_hand]
    bets = [bet_amount]
    dealer_upcard = dealer_hand[0]

    if user_hand[0] == user_hand[1]:
        should_split = should_split_hand(user_hand[0], dealer_upcard, money, bet_amount)

        if should_split:
            money -= bet_amount  # Subtract bet amount for split

            # Create second hand
            second_hand = [user_hand.pop()]
            hands.append(second_hand)
            bets.append(bet_amount)

            # Deal one card to each hand
            hands[0].append(shoe[shoe_index])
            shoe_index += 1
            hands[1].append(shoe[shoe_index])
            shoe_index += 1

    # Play each hand
    hand_results = []

    for hand_idx in range(len(hands)):
        current_hand = hands[hand_idx]
        current_bet = bets[hand_idx]
        current_total = calculate_hand(current_hand)
        doubled = False

        # Play this hand
        while current_total < 21:
            # Use negative total if soft hand
            if is_soft_hand(current_hand):
                lookup_total = -current_total
            else:
                lookup_total = current_total
            action = BASIC_STRATEGY.get((lookup_total, dealer_upcard), "STAND")

            if action == "HIT":
                current_hand.append(shoe[shoe_index])
                shoe_index += 1
                current_total = calculate_hand(current_hand)

                if current_total > 21:
                    break

            elif action == "DOUBLE":
                money -= current_bet
                doubled = True
                current_hand.append(shoe[shoe_index])
                shoe_index += 1
                current_total = calculate_hand(current_hand)
                break
            else:  # STAND
                break

        # Store result for this hand
        hand_results.append({
            'hand': current_hand,
            'total': current_total,
            'bet': current_bet,
            'doubled': doubled,
            'busted': current_total > 21
        })

    # Dealer plays
    dealer_hand[1] = dealer_face_down_card
    dealer_total = calculate_hand(dealer_hand)

    while dealer_total < 17:
        dealer_hand.append(shoe[shoe_index])
        shoe_index += 1
        dealer_total = calculate_hand(dealer_hand)

    overall_result = None

    for hand_result in hand_results:
        current_total = hand_result['total']
        current_bet = hand_result['bet']
        doubled = hand_result['doubled']
        busted = hand_result['busted']

        if busted:
            # Loss, already subtracted
            pass
        elif dealer_total > 21:
            # Dealer bust, player wins
            if doubled:
                money += current_bet * 4
            else:
                money += current_bet * 2
            if overall_result != "loss":
                overall_result = "win"
        elif current_total > dealer_total:
            # Player wins
            if doubled:
                money += current_bet * 4
            else:
                money += current_bet * 2
            if overall_result != "loss":
                overall_result = "win"
        elif dealer_total > current_total:
            # Dealer wins (already subtracted)
            overall_result = "loss"
        else:
            # Push
            if doubled:
                money += current_bet * 2
            else:
                money += current_bet
            if overall_result is None:
                overall_result = "push"

    if overall_result is None:
        overall_result = "loss"

    return shoe, shoe_index, money, overall_result


def should_split_hand(card_value, dealer_upcard, money, bet_amount):
    # Can't afford to split
    if money < bet_amount:
        return False

    # Always split 8s and Aces
    if card_value == 8 or card_value == 11:
        return True

    # Split 2-7 on dealer 2-7
    if card_value in [2, 3, 4, 5, 6, 7]:
        if dealer_upcard in [2, 3, 4, 5, 6, 7]:
            return True

    # Split 9s on dealer 2-9 except 7
    if card_value == 9:
        if dealer_upcard in [2, 3, 4, 5, 6, 8, 9]:
            return True

    # Never split 10s

    return False


def run_simulation(num_rounds, bet_amount=50, starting_money=10000000, checkpoint_interval=100000):
    shoe, shoe_index = shuffle_deck()
    money = starting_money

    # Store round data
    round_data = []

    # Store checkpoint stats
    checkpoint_data = []

    for round_num in range(num_rounds):
        shoe, shoe_index, money, result = play_game(shoe, shoe_index, money, bet_amount)

        round_data.append({
            'round': round_num + 1,
            'result': result,
            'money': money,
            'profit': money - starting_money
        })

        # Every checkpoint_interval rounds, record stats
        if (round_num + 1) % checkpoint_interval == 0:
            rounds_so_far = round_num + 1
            df_so_far = pd.DataFrame(round_data)

            results_counts = df_so_far['result'].value_counts()

            checkpoint_data.append({
                'checkpoint_round': rounds_so_far,
                'wins': results_counts.get('win', 0),
                'losses': results_counts.get('loss', 0),
                'pushes': results_counts.get('push', 0),
                'blackjacks': results_counts.get('blackjack', 0),
                'money': money,
                'profit': money - starting_money,
                'roi': ((money - starting_money) / (rounds_so_far * bet_amount)) * 100,
            })

    # Create DataFrames
    df_rounds = pd.DataFrame(round_data)
    df_checkpoints = pd.DataFrame(checkpoint_data)

    # Calculate final stats
    results_counts = df_rounds['result'].value_counts()
    total_rounds = len(df_rounds)

    stats = {
        "num_rounds": total_rounds,
        "wins": results_counts.get('win', 0),
        "losses": results_counts.get('loss', 0),
        "pushes": results_counts.get('push', 0),
        "blackjacks": results_counts.get('blackjack', 0),
        "win_rate": (results_counts.get('win', 0) / total_rounds) * 100,
        "loss_rate": (results_counts.get('loss', 0) / total_rounds) * 100,
        "push_rate": (results_counts.get('push', 0) / total_rounds) * 100,
        "blackjack_rate": (results_counts.get('blackjack', 0) / total_rounds) * 100,
        "starting_money": starting_money,
        "final_money": money,
        "profit": money - starting_money,
        "roi": ((money - starting_money) / (total_rounds * bet_amount)) * 100,
        "df_rounds": df_rounds,
        "df_checkpoints": df_checkpoints
    }

    return stats


if __name__ == "__main__":
    print("Simulating 1,000,000 rounds...")
    start_time = time.time()
    stats = run_simulation(1000000, bet_amount=50, checkpoint_interval=100000)

    stats["df_rounds"].assign(strategy="Basic Strategy").to_csv("blackjack_basic_rounds.csv", index=False)
    stats["df_checkpoints"].assign(strategy="Basic Strategy").to_csv("blackjack_basic_checkpoints.csv", index=False)

    elapsed = time.time() - start_time

    print(f"\n       CHECKPOINTS       ")
    print("-------------------------")
    print(stats['df_checkpoints'][['checkpoint_round', 'profit', 'roi']])

    print(f"\n       SIMULATION RESULTS       ")
    print("-------------------------------")
    print(f"Rounds played: {stats['num_rounds']}")
    print(f"Wins: {stats['wins']} ({stats['win_rate']:.2f}%)")
    print(f"Losses: {stats['losses']} ({stats['loss_rate']:.2f}%)")
    print(f"Pushes: {stats['pushes']} ({stats['push_rate']:.2f}%)")
    print(f"Blackjacks: {stats['blackjacks']} ({stats['blackjack_rate']:.2f}%)")
    print(f"\nStarting money: ${stats['starting_money']}")
    print(f"Final money: ${stats['final_money']}")
    print(f"Profit/Loss: ${stats['profit']}")
    print(f"ROI: {stats['roi']:.2f}%")
    print(f"\nTime elapsed: {elapsed:.2f} seconds")


