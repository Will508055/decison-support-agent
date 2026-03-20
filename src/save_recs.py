from . import prompts
import csv


def save_recs(conditions: prompts.ConditionsResponse, scene: prompts.SceneResponse, rec: prompts.RecommendationResponse) -> None:
    while True:
        try:
            decision = input('Would you like to save these recommendations for future reference? (y/n): ').strip().lower()
            if decision == 'y':
                break
            elif decision == 'n':
                print('Recommendation not saved.')
                return None
            else:
                print('Please enter "y" for yes or "n" for no.')
        except ValueError:
            print('Invalid input. Please enter "y" for yes or "n" for no.')
    
    new_row = {
        'traction': conditions.traction,
        'visibility': conditions.visibility,
        'traffic': conditions.traffic,
        'curve_sharpness': scene.curve_sharpness,
        'curve_visibility': scene.visible_curve_length,
        'oncoming_traffic': scene.oncoming_traffic,
        'entry_speed': rec.entry_speed,
        'braking': rec.braking,
        'lean_angle': rec.lean_angle,
        'lane_position': rec.lane_position
    }

    with open('recommendations.csv', 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=new_row.keys())
        writer.writerow(new_row)

    print("Recommendation added to recommendations.csv")