from colorfight import Colorfight
import time
import random
from colorfight.constants import BLD_GOLD_MINE, BLD_ENERGY_WELL, BLD_FORTRESS, BUILDING_COST


class Agent:
    def __init__():
        pass

    def connect_room(self, room='public', username='SmallBrain', password=str(int(time.time())):
        self.game = Colorfight()
        self.game.connection(room=room)

        if not self.game.register(username=username, password=password):
            self.game.disconnect()

        self.map = self.game.game_map

        self.home = None


    def cell_danger(cell):
        for dx in range(-5, 5):
            for dy in range(-5, 5):
                cell_danger += 1 / (abs(dx) + abs(dy)) if self.map[cell.position + Position(dx, dy)]

        return cell_danger

    def home_dist(cell):
        for h in self.game.home

    def cell_desire(cell):
      cell_danger, cdw = self.cell_danger(cell), 1
      cell_gain, cgw = self.cell_gain(cell), 1
      delta_perim, dpw = self.delta_perim(cell), 1
      home_dist, hdw = self.home_dist(cell), 1


    def build_weight(cell):
        return (cell.gold * g_weight, cell.energy * e_weight)

    def play_game(self, game, room='public', username='SmallBrain', password=str(int(time.time()))):
        while True:
            # The command list we will send to the server
            cmd_list = []
            # The list of cells that we want to attack
            attack_list = []
            build_list = []
            # update_turn() is required to get the latest information from the
            # server. This will halt the program until it receives the updated
            # information.
            # After update_turn(), game object will be updated.
            # update_turn() returns a Boolean value indicating if it's still
            # the same game. If it's not, break out
            if not self.game.update_turn():
                break

            # Check if you exist in the game. If not, wait for the next round.
            # You may not appear immediately after you join. But you should be
            # in the game after one round.
            if self.game.me == None:
                continue

            me = self.game.me

            # Initialize all member variables necessary

            found_home = False
            for cell in game.me.cells.values():
                if cell.is_home:
                    self.home = cell
                    found_home = True
                    break

            # game.me.cells is a dict, where the keys are Position and the values
            # are MapCell. Get all my cells.
            for cell in game.me.cells.values():
                # Check the surrounding position
                for pos in cell.position.get_surrounding_cardinals():
                    # Get the MapCell object of that position
                    c = game.game_map[pos]
                    # Attack if the cost is less than what I have, and the owner
                    # is not mine, and I have not attacked it in this round already
                    # We also try to keep our cell number under 100 to avoid tax
                    if c.attack_cost < me.energy and c.owner != game.uid \
                            and c.position not in attack_list
                        # Add the attack command in the command list
                        # Subtract the attack cost manually so I can keep track
                        # of the energy I have.
                        # Add the position to the attack list so I won't attack
                        # the same cell
                        cmd_list.append(game.attack(pos, c.attack_cost))
                        print("We are attacking ({}, {}) with {} energy".format(
                            pos.x, pos.y, c.attack_cost))
                        game.me.energy -= c.attack_cost
                        attack_list.append(c.position)

                # If we can upgrade the building, upgrade it.
                # Notice can_update only checks for upper bound. You need to check
                # tech_level by yourself.
                if cell.building.can_upgrade and \
                        (cell.building.is_home or cell.building.level < me.tech_level):

                    weight = None
                    if cell.building.name == BLD_ENERGY_WELL:
                        weight = self.g_weight * cell.gold
                    elif cell.building.name == BLD_GOLD_MINE:
                        weight = self.e_weight * cell.energy

                    build_list.append((None, 1, weight, cell))

                # Build a random building if we have enough gold
                if cell.owner == me.uid and cell.building.is_empty and me.gold >= BUILDING_COST[0]:

                    # Find the more preferable between gold mine and energy well
                    weights = build_weight(cell)
                    pref_building = BLD_ENERGY_WELL
                    pref_weight = weights[1]
                    if weights[0] > weights[1]:
                        pref_building = BLD_GOLD_MINE
                        pref_weight = weights[0]

                    build_list.append((pref_building, 0, pref_weight, cell))

                def sortBuildOps(buildOp):
                    return buildOp[2]

                build_list.sort(key=sortBuildOps)
                for i in build_list:
                    if me.gold < g_threshold or me.energy < e_threshold:
                        break

                    if i[1]:
                        cmd_list.append(game.upgrade(i[3]))

                        temp_g = me.gold - cell.building.upgrade_gold
                        temp_e = me.energy - cell.building.upgrade_energy
                        if temp_g >= g_threshold:
                            me.gold = temp_g
                        else:
                            break
                        if temp_e >= e_threshold:
                            me.energy = temp_e
                        else:
                            break

                        print("We upgraded ({}, {})".format(
                            cell.position.x, cell.position.y))
                    else:
                        temp_g = me.gold - 100
                        if temp_g >= g_threshold:
                            me.gold = temp_g
                        cmd_list.append(game.build(i[3], i[0]))
                        me.gold -= 100
                        print("We build {} on ({}, {})".format(
                            i[0], cell.position.x, cell.position.y))

            # Send the command list to the server
            result = game.send_cmd(cmd_list)
            print(result)

if __name__ == '__main__':
    # Create a Colorfight Instance. This will be the object that you interact
    # with.
    game = Colorfight()

    # ================== Find a random non-full rank room ==================
    # room_list = game.get_gameroom_list()
    # rank_room = [room for room in room_list if room["rank"] and room["player_number"] < room["max_player"]]
    # room = random.choice(rank_room)["name"]
    # ======================================================================
    room = 'public'  # Delete this line if you have a room from above

    # ==========================  Play game once ===========================
    Agent.play_game(
        game=game,
        room=room,
        username='ExampleAI' + str(random.randint(1, 100)),
        password=str(int(time.time()))
    )
    # ======================================================================

    # ========================= Run my bot forever =========================
    # while True:
    #    try:
    #        play_game(
    #            game     = game, \
    #            room     = room, \
    #            username = 'ExampleAI' + str(random.randint(1, 100)), \
    #            password = str(int(time.time()))
    #        )
    #    except Exception as e:
    #        print(e)
    #        time.sleep(2)
