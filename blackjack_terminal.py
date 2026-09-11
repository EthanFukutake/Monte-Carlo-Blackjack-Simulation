import random


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

# Calculate if User has blackjack from the start
def is_blackjack(hand):
    return len(hand) == 2 and calculate_hand(hand) == 21


def user_draw_card(user_hand, shoe, shoe_index):
    current_card = shoe[shoe_index]
    shoe_index += 1
    user_hand.append(current_card)
    user_total = calculate_hand(user_hand)
    print("Your hand: ", user_hand)
    print("Your total: ", user_total)
    print()

    return user_total, shoe_index


def play_game(shoe, shoe_index, money):
    # Initialize lists and totals for user and dealer hands
    dealer_hand = []
    user_hand = []
    user_total = 0
    dealer_total = 0

    # Shuffle Shoe if count is less than 75 (Casinos typicaly shuffle when there are only 1-2 decks remaining in the shoe)
    if len(shoe) - shoe_index < 75:
        shoe, shoe_index = shuffle_deck()
        print("Shoe Shuffled!")

    if money < 50:
        print("You are out of bettable money.")
        return (shoe, money)

    # Get user bet amount
    bet_amount = int(input("How much would you like to bet?: "))
    while (bet_amount < 50 or bet_amount > 5000) or bet_amount % 50 != 0 or bet_amount > money:
        bet_amount = int(input("Bet amount must be between 50-5000, in $50 increments, and not exceed your balance. Try again: "))

    # Subtract bet amount from money
    money -= bet_amount

    # Pop top card of the shoe for the user
    current_card = shoe[shoe_index]
    user_hand.append(current_card)
    shoe_index += 1

    # Pop top card of the shoe for the dealer
    current_card = shoe[shoe_index]
    dealer_hand.append(current_card)
    shoe_index += 1

    # Pop top card of the shoe for the user
    current_card = shoe[shoe_index]
    user_hand.append(current_card)
    shoe_index += 1

    # Pop top card of the shoe for the user and save it to dealer_face_down_card so the user cannot see it
    dealer_face_down_card = shoe[shoe_index]

    # Append X as a place holder for dealer_face_down_card
    dealer_hand.append('X')

    print("Dealer's hand:", dealer_hand)
    print("Your hand:", user_hand)
    print()

    # Calculate total for user
    user_total = calculate_hand(user_hand)

    # Calculate whether user and/or dealer have blackjack from the start
    user_blackjack = is_blackjack(user_hand)
    dealer_blackjack = is_blackjack(dealer_hand[:1] + [dealer_face_down_card])

    # Both have BlackJack: Tie
    # Only user has Blackjack: User wins
    # Only dealer has Blackjack: Dealer wins
    if user_blackjack and dealer_blackjack:
        print("Both have BlackJack! Push.")
        money += bet_amount
        print("Your money: ", money)
    elif user_blackjack:
        print("BlackJack! You Win!")
        money += (bet_amount * 2.5)
        print("Your money: ", money)
    elif dealer_blackjack:
        dealer_hand[1] = dealer_face_down_card
        print("Dealer has BlackJack. Dealer Wins!")
        print("Dealer's hand:", dealer_hand)
        print("Your money: ", money)
    else:

        # Check if the user can split
        hands = [user_hand]
        bets = [bet_amount]
        hand_number = 0

        if user_hand[0] == user_hand[1]:
            split = input("Split? (Y/N): ")

            if split.upper() == "Y":
                # Make sure the user has enough money for the additional bet
                if money < bet_amount:
                    print("Insufficient funds to Split!")
                else:
                    money -= bet_amount

                    # Create the second hand
                    second_hand = [user_hand.pop()]
                    hands.append(second_hand)

                    # Add one card to each hand
                    hands[0].append(shoe[shoe_index])
                    shoe_index += 1
                    hands[1].append(shoe[shoe_index])
                    shoe_index += 1

                    # Add another bet for the second hand
                    bets.append(bet_amount)

                    print()
                    print("Hand 1:", hands[0])
                    print("Hand 1 Total:", calculate_hand(hands[0]))
                    print()
                    print("Hand 2:", hands[1])
                    print("Hand 2 Total:", calculate_hand(hands[1]))
                    print()

        # Play each hand
        while hand_number < len(hands):

            current_hand = hands[hand_number]
            current_bet = bets[hand_number]

            print("Playing Hand", hand_number + 1)
            print("Your hand:", current_hand)
            print("Your total:", calculate_hand(current_hand))
            print()

            # Allow additional splitting up to 4 total hands
            while len(hands) < 4 and len(current_hand) == 2 and current_hand[0] == current_hand[1]:

                split = input("Split this hand? (Y/N): ")

                if split.upper() != "Y":
                    break

                # Make sure the user has enough money for the additional bet
                if money < current_bet:
                    print("Insufficient funds to Split!")
                    break

                money -= current_bet

                # Remove one card from the current hand
                split_card = current_hand.pop()

                # Create the new hand
                new_hand = [split_card]

                # Add one card to each hand
                current_hand.append(shoe[shoe_index])
                shoe_index += 1
                new_hand.append(shoe[shoe_index])
                shoe_index += 1

                # Add the new hand and bet
                hands.append(new_hand)
                bets.append(current_bet)

                print()
                print("Hand", hand_number + 1, ":", current_hand)
                print("Hand", hand_number + 1, "Total:",calculate_hand(current_hand))
                print()
                print("New Hand", len(hands), ":", new_hand)
                print("New Hand", len(hands), "Total:", calculate_hand(new_hand))
                print()

            # Check if this hand can still be split after receiving its card
            # Then continue playing the current hand normally

            user_total = calculate_hand(current_hand)

            # Double Down
            double_down = str(input("Double Down? (Y/N): "))

            if double_down.upper() == "Y":
                if money < current_bet:
                    print("Insufficient funds to Double Down! ")

                    while True:
                        hit = input("Hit? (Y/N): ")

                        if hit.upper() == "Y":
                            user_total, shoe_index = user_draw_card(current_hand, shoe, shoe_index)

                            # Bust if user's hand is greater than 21
                            if user_total > 21:
                                print("Bust! Dealer Wins")
                                print("Your money: ", money)
                                break
                        else:
                            break

                else:
                    money -= current_bet
                    bets[hand_number] *= 2
                    current_bet = bets[hand_number]

                    user_total, shoe_index = user_draw_card(current_hand, shoe, shoe_index)

                    if user_total > 21:
                        print("Bust! Dealer Wins")
                        print("Your money: ", money)

            else:
                # Ask if the user wants to keep hitting
                while True:
                    hit = input("Hit? (Y/N): ")

                    if hit.upper() == "Y":
                        user_total, shoe_index = user_draw_card(current_hand, shoe, shoe_index)

                        # Bust if user's hand is greater than 21
                        if user_total > 21:
                            print("Bust! Dealer Wins")
                            print("Your money: ", money)
                            break
                    else:
                        break

            hand_number += 1

        # Once all user hands are finished, swap out placeholder 'X'
        # with dealer_face_down_card
        dealer_hand[1] = dealer_face_down_card

        print()
        print("Dealer's hand:", dealer_hand)
        print()

        dealer_total = calculate_hand(dealer_hand)

        # Dealer keeps hitting until their hand is 17 or greater
        while dealer_total < 17:
            current_card = shoe[shoe_index]
            shoe_index += 1
            dealer_hand.append(current_card)
            dealer_total = calculate_hand(dealer_hand)

            print("Dealer's hand:", dealer_hand)
            print("Dealer's total:", dealer_total)
            print()

        print("Final hands:")
        print("Dealer:", dealer_hand, "- Total:", dealer_total)

        for i in range(len(hands)):
            print("Hand", i + 1, ":", hands[i], "- Total:", calculate_hand(hands[i]))

        print()

        # Settle each hand separately
        for i in range(len(hands)):

            current_hand = hands[i]
            current_bet = bets[i]
            current_total = calculate_hand(current_hand)

            # Player already busted
            if current_total > 21:
                print("Hand", i + 1, ": Bust. Dealer Wins.")
                print("Your money:", money)
                print()

            # Dealer busts, player wins
            elif dealer_total > 21:
                print("Hand", i + 1, ": Dealer Busts! You Win!")
                money += (current_bet * 2)
                print("Your money:", money)
                print()

            # Player has higher total
            elif current_total > dealer_total:
                print("Hand", i + 1, ": You Win!")
                money += (current_bet * 2)
                print("Your money:", money)
                print()

            # Dealer has higher total
            elif dealer_total > current_total:
                print("Hand", i + 1, ": Dealer Wins")
                print("Your money:", money)
                print()

            # Same total
            else:
                print("Hand", i + 1, ": Push. It's a Tie")
                money += current_bet
                print("Your money:", money)
                print()

    return shoe, shoe_index, money


shoe, shoe_index = shuffle_deck()
money = 10000

shoe, shoe_index, money = play_game(shoe, shoe_index, money)

while True:
    if money < 50:
        print("Game Over!")
        break

    play = input("Play Again? (Y/N): ")

    if play.upper() == "Y":
        shoe, shoe_index, money = play_game(shoe, shoe_index, money)
    else:
        break
