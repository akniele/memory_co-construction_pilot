import os
import json
import copy
import matplotlib.pyplot as plt

results = {}

results_relations = {}

tags = {
    "SHOULDBEOVERLAP": 0,
    "SHOULDBECOMP1": 0,
    "SHOULDBECOMP2": 0,
    "SHOULDBECONFL": 0,
    "MISSINGOVERLAP": 0,
    "MISSINGCOMP1": 0,
    "MISSINGCOMP2": 0,
    "MISSINGCONFL": 0,
    "HALLUCINATION": 0,
    "OTHER": 0
}


tags_mapping = {
    "SHOULDBEOVERLAP": "should be overlap",
    "SHOULDBECOMP1": "should be complementary 1",
    "SHOULDBECOMP2": "should be complementary 2",
    "SHOULDBECONFL": "should be conflict",
    "MISSINGOVERLAP": "missing in overlap",
    "MISSINGCOMP1": "missing in complementary 1",
    "MISSINGCOMP2": "missing in complementary 2",
    "MISSINGCONFL": "missing in conflict",
    "HALLUCINATION": "hallucination",
    "OTHER": "other"
}

my_labels = ["should be overlap", "should be complementary 1", "should be complementary 2", "should be conflict", "missing in overlap", "missing in complementary 1", "missing in complementary 2", "missing in conflict", "hallucination", "other"]


# get all folders in the current directory
folders = [f for f in os.listdir() if os.path.isdir(f)]

# get all files in each folder
files = {}
for folder in folders:
    files[folder] = [f for f in os.listdir(folder) if os.path.join(f"{folder}", f) and f != '.DS_Store']

print(files)

# iterate through each file

for folder in files:
    results[folder] = {}
    results_relations[folder] = {}

    for file in files[folder]:
        with open(f'{folder}/{file}', 'r') as f:
            data = json.load(f)

        copied_tags = copy.deepcopy(tags)
        copied_tags_for_relation = copy.deepcopy(tags)
        
        results[folder][file] = copied_tags
        results_relations[folder][file] = copied_tags_for_relation

        test_data = data['Annotation']

        for item in test_data.values():
            number = item['tag']
            if number == "DUMMY":
                continue
            results[folder][file][number] += 1

        relation_data = data['Relations']

        for item in relation_data.values():
            number = item[0]['tag']
            results_relations[folder][file][number] += 1

        
for folder in files:
     for file in files[folder]:
        for tag, number in results_relations[folder][file].items():
                    if number != 0:
                        print(f"folder: {folder}, file: {file}, tag: {tag}, number: {number}")
                        results[folder][file][tag] -= number

 # annotator created a relation with between spans with two different labels (shouldn't happen)
results["participant4"]["textID-2.json"]["SHOULDBECONFL"] += 1
results["participant4"]["textID-2.json"]["OTHER"] += 1


print(type(results))
print(type(results["participant4"]))


print("results\n")
print(results["participant2"]["textID-1.json"])

print("results_relations\n")
print(results_relations["participant2"]["textID-1.json"])


full = {"participant1": ["textID-0.json", "textID-2.json", "textID-4.json"], "participant2": ["textID-1.json", "textID-3.json"], "participant3" : ["textID-0.json", "textID-2.json", "textID-4.json"], "participant4" : ["textID-1.json", "textID-3.json"]} 
partial = {"participant1": ["textID-1.json", "textID-3.json"], "participant2": ["textID-0.json", "textID-2.json", "textID-4.json"], "participant3" : ["textID-3.json"], "participant4" : ["textID-0.json", "textID-2.json", "textID-4.json"]}

overall_count_full = copy.deepcopy(tags)

for participant in full:
    for file in full[participant]:
        for tag in tags:
            overall_count_full[tag] += results[participant][file][tag]

print(f"overall count full:\n {overall_count_full}")

overall_count_partial = copy.deepcopy(tags)

for participant in partial:
    for file in partial[participant]:
        for tag in tags:
            overall_count_partial[tag] += results[participant][file][tag]


print(f"overall count partial:\n {overall_count_partial}")

colors = [(255, 255, 109), (50,196,196), (255,119,192), (36,255,36), (20,129,239), (192,119,255), (109,182,255), (255,182,219), (182,219,255), (249,139,30), (196,123,40)]

colors = [(r/255, g/255, b/255) for r, g, b in colors]


plt.bar(range(len(overall_count_full)), list(overall_count_full.values()), align='center', label=list(overall_count_full.keys()), color=colors)

plt.xticks(range(len(overall_count_full)), range(1, len(overall_count_full) + 1)) 


plt.ylim(top=18)

plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=True,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off

plt.xlabel("Label")

plt.ylabel("Number of Occurrences")


plt.legend(labels=my_labels, loc="upper left", ncol=2, fontsize='small')

plt.savefig('label_distribution_full_data.svg', format='svg') 

plt.show()


plt.bar(range(len(overall_count_partial)), list(overall_count_partial.values()), align='center', label=list(overall_count_partial.keys()), color=colors)

plt.xticks(range(len(overall_count_partial)), range(1, len(overall_count_partial) + 1)) 

plt.ylim(top=18)

plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=True,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off

plt.xlabel("Label")

plt.ylabel("Number of Occurrences")

plt.legend(labels=my_labels, loc="upper left", ncol=2, fontsize='small')


plt.savefig('label_distribution_partial_data.svg', format='svg') 

plt.show()