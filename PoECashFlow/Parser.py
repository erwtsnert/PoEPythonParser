import requests
import pickle


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
        self.item_database += [[item for item in stash["items"] if "note" in item and item["league"] == league]
                               for stash in self.current_stashes["stashes"]]

    def cycle(self):
        self.get_new_stashes()
        self.update_change_id()
        self.update_item_database()

    def database_size(self):
        return len(self.item_database)

    def pickle_database(self):
        with open("./items/item_database.pickle", "wb") as file:
            pickle.dump(self.item_database, file)

if __name__ == "__main__":
    new_parser = ItemParser()
    while len(new_parser.item_database) < 100000:
        new_parser.cycle()
        print(new_parser.database_size())
    new_parser.pickle_database()
    print("Done!")
