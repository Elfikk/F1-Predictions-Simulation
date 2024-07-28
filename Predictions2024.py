from BoolPrediction import bool_pred_instances
from Championships import DriverChampionship, ConstructorChampionship, NAfterN
from H2HPrediction import h2h_predictions_instances
from RankedPrediction import ranked_pred_instances
from RacePickPrediction import pick_prediction_instances

def get_all_preds_2024():

    all_preds = {}

    # Bool Preds
    # [Podiums, Poles, FLs, Q1s, Monaco]

    bool_preds = bool_pred_instances()
    all_preds["Podiums"] = bool_preds[0]
    all_preds["Poles"] = bool_preds[1]
    all_preds["FLs"] = bool_preds[2]
    all_preds["Q1"] = bool_preds[3]
    all_preds["Monaco"] = bool_preds[4]

    # Championship Preds
    all_preds["CChamp"] = ConstructorChampionship()
    all_preds["DChamp"] = DriverChampionship()
    all_preds["NAfterN"] = NAfterN()

    # H2H Preds
    h2h_preds = h2h_predictions_instances()
    all_preds["RH2H"] = h2h_preds[0]
    all_preds["QH2H"] = h2h_preds[1]

    # Superlative Preds
    # [MaxDNFs, MinLaps, PositionImprover, ChampImprover, MaxPitStops, \
    # SlowStarter, EngineComponents, FastestPitStop, QualiAverageTeam]
    ranked_preds = ranked_pred_instances()
    all_preds["MaxDNF"] = ranked_preds[0]
    all_preds["MinLaps"] = ranked_preds[1]
    all_preds["DeltaPos"] = ranked_preds[2]
    all_preds["DeltaPts"] = ranked_preds[3]
    all_preds["MaxPS"] = ranked_preds[4]
    all_preds["SlowStarter"] = ranked_preds[5]
    all_preds["EngineComps"] = ranked_preds[6]
    all_preds["FastestPS"] = ranked_preds[7]
    all_preds["QCons"] = ranked_preds[8]

    # Pick 5 Racess
    # [HulkQuali, GaslyRace, BlowyEngines]
    race_pick_preds = pick_prediction_instances()
    all_preds["Hulk"] = race_pick_preds[0]
    all_preds["Gasly"] = race_pick_preds[1]
    all_preds["BlowyEngines"] = race_pick_preds[2]

    return all_preds