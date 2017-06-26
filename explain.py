import json, os

with open(os.path.expanduser("~") + '/.binaryninja/plugins/binja_explain_instruction/' + 'explanations_en.json', 'r') as explanation_file:
    explanations = json.load(explanation_file)

print(explanations)

def explain_llil(llil_instruction):
    return llil_instruction.operation.name
