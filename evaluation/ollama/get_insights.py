import json
import numpy as np

def calculate_statistics_from_jsonl(input_jsonl, output_txt):
    facial_feature_consistency_scores = []
    skin_texture_clarity_scores = []
    edge_naturalness_scores = []
    artifacts_scores = []
    overall_quality_scores = []
    results = []

    with open(input_jsonl, 'r') as f:
        for line in f:
            data = json.loads(line)
            facial_feature_consistency_scores.append(data['Facial Feature Consistency'])
            skin_texture_clarity_scores.append(data['Skin Texture Clarity'])
            edge_naturalness_scores.append(data['Edge Naturalness'])
            artifacts_scores.append(data['Artifacts'])
            overall_quality_scores.append(data['Overall Quality'])
            results.append(data)

    # Calculate averages
    avg_facial_feature_consistency = np.mean(facial_feature_consistency_scores)
    avg_skin_texture_clarity = np.mean(skin_texture_clarity_scores)
    avg_edge_naturalness = np.mean(edge_naturalness_scores)
    avg_artifacts = np.mean(artifacts_scores)
    avg_overall = np.mean(overall_quality_scores)


    # Calculate overall quality statistics
    max_overall_quality = np.max(overall_quality_scores)
    min_overall_quality = np.min(overall_quality_scores)
    median_overall_quality = np.median(overall_quality_scores)

    # Find the corresponding JSONL elements
    max_overall_quality_element = next(item for item in results if item['Overall Quality'] == max_overall_quality)
    min_overall_quality_element = next(item for item in results if item['Overall Quality'] == min_overall_quality)

    # Handling the median element
    try:
        median_overall_quality_element = next(item for item in results if item['Overall Quality'] == median_overall_quality)
    except StopIteration:
        # If no exact match is found, find the closest element to the median
        closest_to_median = min(results, key=lambda x: abs(x['Overall Quality'] - median_overall_quality))
        median_overall_quality_element = closest_to_median

    # Write results to output file
    with open(output_txt, 'w') as f:
        f.write(f"Average Facial Feature Consistency: {avg_facial_feature_consistency}\n")
        f.write(f"Average Skin Texture Clarity: {avg_skin_texture_clarity}\n")
        f.write(f"Average Edge Naturalness: {avg_edge_naturalness}\n")
        f.write(f"Average Artifacts: {avg_artifacts}\n")
        f.write(f"Average Overall Quality Scores: {avg_overall}\n")
        f.write("\n")
        f.write(f"Max Overall Quality: {max_overall_quality}\n")
        f.write(json.dumps(max_overall_quality_element, ensure_ascii=False) + '\n')
        f.write("\n")
        f.write(f"Min Overall Quality: {min_overall_quality}\n")
        f.write(json.dumps(min_overall_quality_element, ensure_ascii=False) + '\n')
        f.write("\n")
        f.write(f"Median Overall Quality: {median_overall_quality}\n")
        f.write(json.dumps(median_overall_quality_element, ensure_ascii=False) + '\n')

# 示例调用
input_jsonl = 'results_1.jsonl'
output_txt = 'statistics_llava_evaluation_generated_deepfake.txt'
calculate_statistics_from_jsonl(input_jsonl, output_txt)
