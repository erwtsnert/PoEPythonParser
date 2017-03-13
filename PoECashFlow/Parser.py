import requests
import pickle
import datetime
import os


class ItemParser:

    def __init__(self):
        self.change_id = "49762236-52802001-49345826-57418159-53407658"
        self.path_url = "http://www.pathofexile.com/api/public-stash-tabs"
        self.current_stashes = None
        # Dictionary of items as key and price as value
        self.item_database = []
        self.price_database = {}

    def get_new_stashes(self):
        new_stashes = requests.get(
            self.path_url, params={"id": self.change_id})
        self.current_stashes = new_stashes.json()

    def update_change_id(self):
        self.change_id = self.current_stashes["next_change_id"]

    def update_item_database(self, league="Legacy"):
        self.item_database += [[item for item in stash["items"] if "note" in item and item[
            "league"] == league] for stash in self.current_stashes["stashes"]]

    def cycle_stashes(self):
        self.get_new_stashes()
        self.update_change_id()
        self.update_item_database()

    def database_size(self):
        return len(self.item_database)

    def pickle_database(self):
        pickle_num = max([0] +
                         [int(file.partition(".")[0]) for file in os.listdir("./items") if file.partition(".")[0].isdigit()]) + 1
        with open("./items/" + str(pickle_num) + ".pickle", "wb") as file:
            pickle.dump(self.item_database, file)

    def populate_item_database(self, size=100000):
        while self.database_size() < size:
            try:
                self.cycle_stashes()
                print(self.database_size())
            except:
                self.pickle_database()
        print("Done!")

    def reset_database(self):
        self.item_database = []

if __name__ == "__main__":
    new_parser = ItemParser()
    while True:
        new_parser.populate_item_database(10000)
        new_parser.pickle_database()
        new_parser.reset_database()
