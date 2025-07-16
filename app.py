from flask import Flask, render_template, request, jsonify
import json
import random

app = Flask(__name__)

with open('data/flight_plans.json') as f:
    flight_plans = json.load(f)

@app.route('/')
def index():
    selected_plan = random.choice(flight_plans)
    return render_template('index.html',
                           plan=selected_plan['incorrect'],
                           correct=selected_plan['correct'])

def normalize(s):
    return ' '.join(s.upper().strip().split())

@app.route('/check', methods=['POST'])
def check():
    user_input = request.json
    aid = user_input['aid']
    submitted_rte = normalize(user_input['rte'])
    submitted_alt = user_input['alt'].strip()

    correct_plan = next((p['correct'] for p in flight_plans if p['incorrect']['aid'] == aid), None)
    
    # Normalize and check if multiple altitudes/routes exist
    correct_alts = correct_plan['alt'] if isinstance(correct_plan['alt'], list) else [correct_plan['alt']]
    correct_rtes = [normalize(r) for r in (correct_plan['rte'] if isinstance(correct_plan['rte'], list) else [correct_plan['rte']])]

    result = {
        'rte_correct': submitted_rte in correct_rtes,
        'alt_correct': submitted_alt in correct_alts
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)