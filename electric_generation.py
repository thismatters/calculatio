class Generation:
    means = "BurnableFuel"
    fuel = "Coal"

    @property
    def generation_items_available(self):
        if self.means == "BurnableFuel":
            return ("Boiler", "SteamEngine", "OffshorePump")
        return ()

    def supply_pipeline(self, demand_kw):
        pass
