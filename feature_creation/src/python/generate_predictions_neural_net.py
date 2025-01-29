import pandas as pd
import torch
import torch.nn as nn
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.metrics import brier_score_loss
from torch.utils.data import TensorDataset, DataLoader


class SymmetricNNWithoutEmbeddings(nn.Module):
    def __init__(self, player_feature_size, env_feature_size, hidden_sizes, dropout):
        super(SymmetricNNWithoutEmbeddings, self).__init__()

        input_size = 2 * player_feature_size + env_feature_size

        layers = []
        for hidden_size in hidden_sizes:
            layers.append(nn.Linear(input_size, hidden_size))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout))
            input_size = hidden_size

        layers.append(nn.Linear(input_size, 1))
        layers.append(nn.Sigmoid())

        self.network = nn.Sequential(*layers)

    def forward(self, p1_features, p2_features, env_features):
        input_1 = torch.cat([p1_features, p2_features, env_features], dim=1)

        input_2 = torch.cat([p2_features, p1_features, env_features], dim=1)

        prob_1 = self.network(input_1)
        prob_2 = self.network(input_2)

        return (prob_1 + 1 - prob_2) / 2


def prepare_dataloaders(
        test_fold,
        player1_cols,
        player2_cols,
        env_cols,
        batch_size=64,
):
    player_scaler = MinMaxScaler()
    env_scaler = MinMaxScaler()

    p1_test = test_fold[player1_cols].values
    p2_test = test_fold[player2_cols].values
    env_test = test_fold[env_cols].values
    y_test = test_fold["target"].values
    unc_test = test_fold['CO_uncertainty'].values
    player1_rank_test = test_fold['player1_rank'].values
    player2_rank_test = test_fold['player2_rank'].values
    player1_bet_odds_test = test_fold['player1_bet_odds'].values
    player2_bet_odds_test = test_fold['player2_bet_odds'].values
    match_id_test = test_fold["match_id"].values
    match_id_test_key = np.arange(len(test_fold))

    player_scaler.fit(np.vstack([p1_test, p2_test]))
    env_scaler.fit(env_test)
    p1_test = player_scaler.transform(p1_test)
    p2_test = player_scaler.transform(p2_test)
    env_test = env_scaler.transform(env_test)

    test_dataset = TensorDataset(
        torch.tensor(p1_test, dtype=torch.float32),
        torch.tensor(p2_test, dtype=torch.float32),
        torch.tensor(env_test, dtype=torch.float32),
        torch.tensor(y_test, dtype=torch.float32).unsqueeze(-1),
        torch.tensor(unc_test, dtype=torch.float32),
        torch.tensor(player1_rank_test, dtype=torch.float32),
        torch.tensor(player2_rank_test, dtype=torch.float32),
        torch.tensor(player1_bet_odds_test, dtype=torch.float32),
        torch.tensor(player2_bet_odds_test, dtype=torch.float32),
        torch.tensor(match_id_test_key, dtype=torch.int32),
    )
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, drop_last=False)

    return test_loader, match_id_test


def generate_predictions(
        test_data,
        model,
        player1_cols,
        player2_cols,
        env_cols,
        batch_size
):
    test_loader, match_ids = prepare_dataloaders(
        test_data,
        player1_cols,
        player2_cols,
        env_cols,
        batch_size=batch_size,
    )

    model.eval()
    with torch.no_grad():
        test_preds = []
        test_labels = []
        odds1_list = []
        odds2_list = []
        test_uncs = []
        match_id_keys = []
        player1_ranks = []
        player2_ranks = []
        for p1, p2, env, labels, unc, p1_rank, p2_rank, odds1, odds2, match_id_key in test_loader:
            preds = model(p1, p2, env).squeeze(-1).tolist()
            test_preds.extend(preds)

            test_labels.extend(labels.squeeze(-1).tolist())

            odds1_list.extend(odds1.tolist())
            odds2_list.extend(odds2.tolist())

            test_uncs.extend(unc.tolist())

            player1_ranks.extend(p1_rank.tolist())
            player2_ranks.extend(p2_rank.tolist())

            match_id_keys.extend(match_id_key.tolist())

    match_ids = [match_ids[i] for i in match_id_keys]
    test_preds = np.array(test_preds)
    test_labels = np.array(test_labels)
    odds1_list = np.array(odds1_list)
    odds2_list = np.array(odds2_list)
    test_uncs = np.array(test_uncs)
    match_ids = np.array(match_ids)
    player1_ranks = np.array(player1_ranks)
    player2_ranks = np.array(player2_ranks)

    probW = 1.0 / odds1_list
    probL = 1.0 / odds2_list
    total_prob = probW + probL
    probW = np.divide(probW, total_prob, out=np.full_like(probW, 0.5), where=(total_prob != 0))
    probW = np.where(np.isnan(probW), 0.5, probW)

    unc_threshold = np.percentile(test_uncs, 50)
    is_uncertain = test_uncs > unc_threshold
    results_df = pd.DataFrame({
        "match_id": match_ids,
        "true_label": test_labels,
        "model_prediction": test_preds,
        "odds_prediction": probW,
        "uncertain": is_uncertain
    })

    unc_mask = test_uncs <= unc_threshold
    rank_mask = (player1_ranks < 50) & (player2_ranks < 50)
    combined_mask = unc_mask & rank_mask
    filtered_preds = test_preds[combined_mask]
    filtered_labels = test_labels[combined_mask]
    filtered_odds1 = odds1_list[combined_mask]
    filtered_odds2 = odds2_list[combined_mask]

    filtered_model_brier = brier_score_loss(filtered_labels, filtered_preds)

    f_probW = 1.0 / filtered_odds1
    f_probL = 1.0 / filtered_odds2
    f_total = f_probW + f_probL
    f_probW = np.divide(f_probW, f_total, out=np.full_like(f_probW, 0.5), where=(f_total != 0))
    f_probW = np.where(np.isnan(f_probW), 0.5, f_probW)

    filtered_odds_brier = brier_score_loss(filtered_labels, f_probW)

    return {
        "test_model_brier": filtered_model_brier,
        "test_odds_brier": filtered_odds_brier,
    }, results_df


def generate_predictions_neural_net(matches: pd.DataFrame) -> pd.DataFrame:
    weather_cols = ['temperature_2m', 'relative_humidity_2m', 'windspeed_10m', 'apparent_temperature']
    player1_cols = [col for col in matches.columns if col.startswith('player1_') and "bet" not in col]
    player2_cols = [col for col in matches.columns if col.startswith('player2_') and "bet" not in col]
    env_cols = [col for col in matches.columns if not col.startswith(
        'player') and col not in player1_cols and col not in player2_cols and "diff" not in col and "target" not in col and "bet" not in col and col not in weather_cols and "avg" not in col and 'match_id' not in col]

    model = SymmetricNNWithoutEmbeddings(player_feature_size=len(player1_cols),
                                         env_feature_size=len(env_cols),
                                         hidden_sizes=[1024],
                                         dropout=0.08895897011795562)

    model.load_state_dict(
        torch.load("models/neural_net/best_models/currently_best_model_weights.pth", weights_only=True))
    results, match_predictions_df = generate_predictions(
        test_data=matches,
        model=model,
        player1_cols=player1_cols,
        player2_cols=player2_cols,
        env_cols=env_cols,
        batch_size=64
    )
    return match_predictions_df
