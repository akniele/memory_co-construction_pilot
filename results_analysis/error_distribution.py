import os
import json
import matplotlib.pyplot as plt


error_count = dict()

my_labels = ["category boundaries", "importance", "implied information", "hallucinations", "ordering", "reference", "repetition"]

files_participant_1 = [f"participant1_with_categorization/{f}" for f in os.listdir("participant1") if os.path.join("participant1", f) and f != '.DS_Store']
files_participant_3 = [f"participant3_with_categorization/{f}" for f in os.listdir("participant3") if os.path.join("participant3", f) and f != '.DS_Store']
files_participant_2 = [f"participant2_with_categorization/{f}" for f in os.listdir("participant2") if os.path.join("participant2", f) and f != '.DS_Store']
files_participant_4 = [f"participant4_with_categorization/{f}" for f in os.listdir("participant4") if os.path.join("participant4", f) and f != '.DS_Store']

files = files_participant_1 + files_participant_3 + files_participant_2 + files_participant_4

for file in files:
    with open(f'{file}', 'r') as f:
        data = json.load(f)

    print(file)

    annotations = data['Annotation']

    for item in annotations.values():
        if "error_type" in item.keys():
            if item["error_type"] in error_count.keys():
                error_count[item["error_type"]] += 1
            else:
                error_count[item["error_type"]] = 1

print(error_count)


colors = [(255, 255, 109), (50,196,196), (255,119,192), (36,255,36), (20,129,239), (192,119,255), (109,182,255)] #, (255,182,219), (182,219,255), (249,139,30), (196,123,40)]

colors = [(r/255, g/255, b/255) for r, g, b in colors]


plt.bar(range(len(error_count)), list(error_count.values()), align='center', label=list(error_count.keys()), color=colors)

plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off

plt.legend(labels=my_labels, loc="upper right", ncol=2, fontsize='small')

plt.ylim(top=40)

plt.xlabel("Error Type")

plt.ylabel("Number of Occurrences")

plt.savefig('error_types_graph.svg', format='svg') 

plt.show()