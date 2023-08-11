from flask import Flask, request, jsonify
from fuzzywuzzy import fuzz

app = Flask(__name__)

def count_matched_words(a, b):
    a_words = set(a.lower().split())
    b_words = set(b.lower().split())
    return len(a_words.intersection(b_words))

def similarity(a, b):
    return fuzz.token_set_ratio(a, b)

def best_match(input_list, word_list):
    results = {}
    for input_word in input_list:
        filtered_matches = [(word, similarity(input_word, word)) for word in word_list]
        best_match_word, best_match_score = max(filtered_matches, key=lambda x: (count_matched_words(input_word, x[0]), x[1]))
        results[input_word] = (best_match_word, best_match_score)
    return results

@app.route('/match', methods=['POST'])
def match():
    input_list = request.json.get('input_list', [])
    word_list = request.json.get('word_list', [])
    results = best_match(input_list, word_list)
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)
