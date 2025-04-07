import os
import json

a = 0 # positive/positive
b = 0 # positive/negative
c = 0 # negative/positive
e = 0 # also counting positive/positive, needs to be same as a, else there is an error somewhere

first_participant = "participant4"
second_participant = "crosscheck"

# find the right pairs of files
files_participant_1 = [f for f in os.listdir(first_participant) if os.path.join(first_participant, f) and f != '.DS_Store']
files_participant_3 = [f for f in os.listdir(second_participant) if os.path.join(second_participant, f) and f != '.DS_Store']

for file in files_participant_1:
    with open(f'{first_participant}/{file}', 'r') as f:
        data = json.load(f)

    try:
        with open(f'{second_participant}/textID-{str(5 - (int(file[-6]) + 1))}.json', 'r') as f: # makes sure that the same example is opened as for the other annotator
            data_2 = json.load(f)

    except FileNotFoundError:
        data_2 = None
        continue
        
    annotator_1_before = data['Annotation']
    annotator_2_before = data_2['Annotation']
    print(f"file: {file}")

    # remove DUMMY tags
    annotator_1 = {}
    for key, value in annotator_1_before.items():
        if isinstance(value, dict) and value.get('tag') != 'DUMMY':
            annotator_1[key] = value

    # remove DUMMY tags
    annotator_2 = {}
    for key, value in annotator_2_before.items():
        if isinstance(value, dict) and value.get('tag') != 'DUMMY':
            annotator_2[key] = value


    for item in annotator_1.values():
            start = item['start']
            end = item['end']
            text = item['text']
            element = item['textElementId']

            found = False

            for item2 in annotator_2.values():
                    start_2 = item2['start']
                    end_2 = item2['end']
                    text_2 = item2['text']
                    element2 = item2['textElementId']
                    if element == element2:
                        if (max(start, start_2) - min(end, end_2)) <= 0:
                            found = True
                            print(f"found overlap: {text} and {text_2}")
                            a += 1
            
            if not found:
                b += 1

    for item in annotator_2.values():
        start = item['start']
        end = item['end']
        text = item['text']
        element = item['textElementId']

        for item2 in annotator_1.values():
                start_2 = item2['start']
                end_2 = item2['end']
                text_2 = item2['text']
                element2 = item2['textElementId']
                if element == element2:
                    if (max(start, start_2) - min(end, end_2)) <= 0:
                        print(f"found overlap: {text} and {text_2}")
                        e += 1
                        break
        
        c += 1

print(f"positive/positive: {a}")
print(f"positive/negative: {b}")
print(f"negative/positive: {c}")
print(f"positive/positive check: {e}")


print(f"balanced F-measure: {(2 * a) / ( (2 * a) + b + c) }")