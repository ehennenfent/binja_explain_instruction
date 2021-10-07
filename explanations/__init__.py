import json
from pathlib import Path

current_directory = Path(__file__).parent

with open(current_directory.joinpath("generic_en.json"), "r") as explanation_file:
    il_explanations = json.load(explanation_file)

with open(current_directory.joinpath("native", "x86_en.json"), "r") as explanation_file:
    x86_explanations = json.load(explanation_file)
