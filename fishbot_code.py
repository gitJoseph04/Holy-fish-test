import json

class PlayerScore:
    def __init__(self, username):
        self.username = username
        self.col_points = 0
        self.quest_points = 319  # max as requested
        self.diary_points = 600  # max as requested
        self.combat_points = 0
        self.total_score = 0

    def load_json(self, filepath):
        try:
            with open(filepath, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return None

    def score_collection_log(self, col_data, col_dict):
     tabs = col_data.get('tabs', {})
     for tab_group in tabs.values():  # e.g., "Raids"
         for sub_tab in tab_group.values():  # e.g., "Tombs of Amascut"
             for item in sub_tab.get('items', []):
                 if item.get('obtained', False):
                     item_id = str(item.get('id'))
                     self.col_points += col_dict.get(item_id, 0)
 
    def score_combat_achievements(self, combat_data):
        ca_raw = combat_data.get('points', 0)
        self.combat_points = ca_raw * 0.5

    def calculate_total_score(self):
        self.total_score = (
            self.col_points +
            self.quest_points +
            self.diary_points +
            self.combat_points
        )

    def summary(self):
        return (
            f"Player: {self.username}\n"
            f"Collection Log Points: {self.col_points}\n"
            f"Quest Points (Capped at 319): {self.quest_points}\n"
            f"Diary Points (Capped at 600): {self.diary_points}\n"
            f"Combat Achievement Score: {self.combat_points}\n"
            f"Total Score: {self.total_score}"
        )


# ----------- Manual Execution ----------- #

player = PlayerScore("USERNAME")

# Load collection log and dictionary
collection_log = player.load_json("collectionlog-USERNAME.json")
collection_dict = player.load_json("coll_log_dictionary.json")

# Load combat data (optional but expected to have {"points": ...})
combat_data = player.load_json("USERNAME_combat.json")

# Score collection log
if collection_log and collection_dict:
    player.score_collection_log(collection_log, collection_dict)
else:
    print("Missing or unreadable collection log or dictionary!")

# Score combat achievements
if combat_data:
    player.score_combat_achievements(combat_data)

# Calculate final score
player.calculate_total_score()

# Print the score summary
print(player.summary())
