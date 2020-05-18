from math import ceil
from scipy.optimize import linprog
import logging

import recipes as _recipes
from items import item_objects

logging.basicConfig(level=logging.DEBUG)


class AdvancedOilProcessing:
    def __init__(
        self,
        *,
        heavy_oil_demand=0,
        light_oil_demand=0,
        petroleum_gas_demand=0,
        module=None,
    ):
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
        adv_oil_recipe = _recipes.AdvancedOilRecipe()
        h2l_recipe = _recipes.HeavyOilToLightOilCrackingRecipe()
        l2p_recipe = _recipes.LightOilToPetroleumCrackingRecipe()

        heavy_output = adv_oil_recipe.outputs["HeavyOil"]
        light_output = adv_oil_recipe.outputs["LightOil"]
        petrol_output = adv_oil_recipe.outputs["PetroleumGas"]

        heavy_cracking_input = h2l_recipe.inputs["HeavyOil"]
        light_cracking_output = h2l_recipe.outputs["LightOil"]

        light_cracking_input = l2p_recipe.inputs["LightOil"]
        petrol_cracking_output = l2p_recipe.outputs["PetroleumGas"]
        A_ub = [
            [-1 * heavy_output, heavy_cracking_input, 0],
            [-1 * light_output, -1 * light_cracking_output, light_cracking_input],
            [-1 * petrol_output, 0, -1 * petrol_cracking_output]
        ]
        logging.debug(f"A_ub = {A_ub}")
        b_ub = [-1 * heavy_oil_demand, -1 * light_oil_demand, -1 * petroleum_gas_demand]
        logging.debug(f"b_ub = {b_ub}")
        c = [3, 1, 1]
        logging.debug(f"c = {c}")
        result = linprog(c, A_ub=A_ub, b_ub=b_ub)
        logging.debug(result.success)
        assert result.status == 0, "advanced oil recipe solution did not converge"
        refinery_ticks, heavy_cracking_ticks, light_cracking_ticks = result.x
        if refinery_ticks < 0.0001:
            refinery_ticks = 0
        if heavy_cracking_ticks < 0.0001:
            heavy_cracking_ticks = 0
        if light_cracking_ticks < 0.0001:
            light_cracking_ticks = 0
        logging.debug(
            f"refinery_ticks: {refinery_ticks}, "
            f"heavy_cracking_ticks: {heavy_cracking_ticks}, "
            f"light_cracking_ticks: {light_cracking_ticks}"
        )
        # convert to actual crafter counts using the adjusted crafting time
        self.refinery_count = self._crafter_count(
            recipe=adv_oil_recipe, module=module, ticks=refinery_ticks
        )
        self.heavy_cracker_count = self._crafter_count(
            recipe=h2l_recipe, module=module, ticks=heavy_cracking_ticks
        )
        self.light_cracker_count = self._crafter_count(
            recipe=l2p_recipe, module=module, ticks=light_cracking_ticks
        )
        logging.debug(
            "Using advanced oil processing and cracking to produce "
            f"{heavy_oil_demand}/s heavy oil, {light_oil_demand}/s light oil, and "
            f"{petroleum_gas_demand}/s petroleum gas requires {refinery_count} "
            f"refineries, {heavy_cracker_count} heavy oil cracking chemical plants, "
            f"and {light_cracker_count} light oil cracking chemical plants."
        )

    def _crafter_count(self, *, recipe, module, ticks):
        _crafter = recipe.made_in[0]
        crafter = item_objects[_crafter]
        logging.debug(f"recipe {recipe}, crafter {crafter}")
        if module:
            logging.debug(f"setting module {module}")
            crafter.module_selection = module
        logging.debug(
            f"crafter speed {crafter.speed}, productivity {crafter.productivity}")
        logging.debug(
            f"recipe crafting time {recipe.crafting_time}")
        craft_rate = crafter.speed * crafter.productivity / recipe.crafting_time
        logging.debug(
            f"craft_rate {craft_rate}")
        crafter_count = ceil(ticks / craft_rate)
        return crafter_count


if __name__ == '__main__':
    AdvancedOilProcessing(heavy_oil_demand=25, petroleum_gas_demand=100)
