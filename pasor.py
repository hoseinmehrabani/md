import random
import json
import os

# تعریف کارت‌ها
suits = ['دل', 'خشت', 'پیک', 'رامی']
ranks = ['۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹', '۱۰', 'جک', 'ملکه', 'شاه', 'آس']
rank_values = {rank: index for index, rank in enumerate(ranks, start=2)}


# ایجاد لیست کارت‌ها
def create_deck(include_jokers=False):
    deck = [f"{rank} {suit}" for suit in suits for rank in ranks]
    if include_jokers:
        deck += ['جوکر'] * 2  # اضافه کردن دو جوکر
    return deck


# تقسیم کارت‌ها
def deal_cards(deck, num_players):
    hands = [[] for _ in range(num_players)]
    while deck:
        for i in range(num_players):
            if deck:
                hands[i].append(deck.pop())
    return hands


# نمایش دست‌ها
def display_hands(hands, player_names):
    for i, hand in enumerate(hands):
        print(f"{player_names[i]}: {', '.join(hand)}")


# بازی
def play_game(hands, player_names, score_rules):
    num_players = len(hands)
    scores = [0] * num_players
    history = []
    rounds = min(len(hand) for hand in hands)

    for round_num in range(rounds):
        print(f"\nدور {round_num + 1}:")
        played_cards = []

        for player in range(num_players):
            card = hands[player].pop(0)  # اولین کارت را بازی می‌کند
            played_cards.append((card, player))
            print(f"{player_names[player]} کارت {card} را بازی کرد.")

        winner = max(played_cards, key=lambda x: rank_values.get(x[0].split()[0], 0))[1]
        scores[winner] += score_rules.get(played_cards[winner][0].split()[0], 1)  # امتیاز خاص
        history.append((round_num + 1, player_names[winner], played_cards))
        print(f"{player_names[winner]} این دور را برد.")

    return scores, history


# محاسبه برنده نهایی
def determine_winner(scores, player_names):
    max_score = max(scores)
    winners = [i for i, score in enumerate(scores) if score == max_score]
    return winners


# ذخیره وضعیت بازی
def save_game(player_names, hands, scores, history):
    game_data = {
        'player_names': player_names,
        'hands': hands,
        'scores': scores,
        'history': history
    }
    with open('saved_game.json', 'w') as f:
        json.dump(game_data, f)
    print("وضعیت بازی ذخیره شد.")


# بارگذاری وضعیت بازی
def load_game():
    if os.path.exists('saved_game.json'):
        with open('saved_game.json', 'r') as f:
            game_data = json.load(f)
        return game_data['player_names'], game_data['hands'], game_data['scores'], game_data['history']
    else:
        print("هیچ بازی ذخیره‌شده‌ای وجود ندارد.")
        return None, None, None, None


# نمایش تاریخچه
def display_history(history):
    print("\nتاریخچه دورها:")
    for round_num, winner, played_cards in history:
        cards = ', '.join([f"{name}: {card}" for card, name in played_cards])
        print(f"دور {round_num}: {winner} با کارت‌ها: {cards} برنده شد.")


# نمایش راهنما
def show_help():
    print("""
راهنمای بازی:
1. هر بازیکن در نوبت خود یک کارت را بازی می‌کند.
2. کارت‌های خاص مانند آس و شاه امتیاز بیشتری دارند.
3. جوکرها می‌توانند به عنوان هر کارتی استفاده شوند.
4. پس از اتمام دورها، برنده بازی مشخص می‌شود.
5. شما می‌توانید بازی را ذخیره کنید و در زمان دیگر ادامه دهید.
""")


# اجرا
def main():
    print("خوش آمدید به بازی پاسور!")
    show_help()  # نمایش راهنما

    player_names = input("نام بازیکن‌ها را با ',' وارد کنید: ").split(',')
    player_names = [name.strip() for name in player_names]
    num_players = len(player_names)

    include_jokers = input("آیا می‌خواهید از جوکرها استفاده کنید؟ (بله/خیر): ").strip().lower() == 'بله'
    deck = create_deck(include_jokers)
    random.shuffle(deck)
    hands = deal_cards(deck, num_players)

    score_rules = {
        'آس': 5,
        'شاه': 4,
        'ملکه': 3,
        'جک': 2
    }

    display_hands(hands, player_names)

    total_rounds = int(input("تعداد دورهای بازی را وارد کنید: "))

    while True:
        action = input(
            "\nآیا می‌خواهید بازی کنید (1)، بازی را ذخیره کنید (2) یا بازی را بارگذاری کنید (3)؟ (برای خروج، 'خروج' را تایپ کنید): ")
        if action == '1':
            scores, history = play_game(hands, player_names, score_rules)
            winners = determine_winner(scores, player_names)
            print("\nنتایج نهایی:")
            for i, score in enumerate(scores):
                print(f"{player_names[i]}: {score} امتیاز")
            if len(winners) > 1:
                print(f"بازیکنان {', '.join(map(lambda x: player_names[x], winners))} برنده شدند!")
            else:
                print(f"{player_names[winners[0]]} برنده شد!")
            display_history(history)
            break
        elif action == '2':
            save_game(player_names, hands, scores, [])
        elif action == '3':
            loaded_names, loaded_hands, loaded_scores, loaded_history = load_game()
            if loaded_names:
                player_names, hands, scores, history = loaded_names, loaded_hands, loaded_scores, loaded_history
                display_hands(hands, player_names)
        elif action.lower() == 'خروج':
            print("خداحافظ!")
            break
        else:
            print("لطفا گزینه معتبر را انتخاب کنید.")


if __name__ == "__main__":
    main()
