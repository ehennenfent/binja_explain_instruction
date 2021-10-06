import json
from pathlib import Path

# Using user_plugin_path doesn't work with plugins that have been installed from the repository manager,
# since it points to .binaryninja/plugins instead of .binaryninja/repositories
# path = user_plugin_path + '/binja_explain_instruction/explanations_en.json'
current_directory = Path(__file__).parent

with open(current_directory.joinpath("generic_en.json"), "r") as explanation_file:
    il_explanations = json.load(explanation_file)

with open(current_directory.joinpath("native", "x86_en.json"), "r") as explanation_file:
    x86_explanations = json.load(explanation_file)
