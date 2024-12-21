def __calculate_kelly_fraction(p, odds):
    b = odds - 1  # Adjust odds to represent decimal profit
    f = (p * b - (1 - p)) / b
    return max(f, 0)  # Only bet if f > 0


def calculate_roi(predictions, avgW, avgL, y_true, max_bet=1.0):
    total_bet = 0
    net_profit = 0

    flat_predictions = [item[0] for item in predictions]  # Flatten predictions
    flat_avgW = [item[0] for item in avgW]  # Flatten avgW
    flat_avgL = [item[0] for item in avgL]  # Flatten avgL
    flat_y_true = [item[0] for item in y_true]  # Flatten y_true

    for prob, odds_w, odds_l, actual in zip(flat_predictions, flat_avgW, flat_avgL, flat_y_true):
        # Your logic here
        if odds_w is None or odds_l is None:
            continue
        # Decide the bet
        if prob >= 0.5:  # Predicted winner
            odds = odds_w
            kelly_fraction = __calculate_kelly_fraction(prob, odds)
            outcome = 1 if actual == 1 else -1
        else:  # Predicted loser
            odds = odds_l
            kelly_fraction = __calculate_kelly_fraction(1 - prob, odds)
            outcome = 1 if actual == 0 else -1

        # Fixed max bet
        bet_amount = kelly_fraction * max_bet
        if bet_amount > 0:
            total_bet += bet_amount
            if outcome == 1:  # Bet won
                net_profit += bet_amount * (odds - 1)
            else:  # Bet lost
                net_profit -= bet_amount
    roi = net_profit / total_bet if total_bet > 0 else 0
    return roi
