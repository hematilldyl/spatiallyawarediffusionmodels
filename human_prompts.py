import csv

# Room Types
styles = ["", "modern ", "traditional ", "farmhouse ", "luxury "]
rooms = {"kitchen": ["refrigerator", "sink", "stove", "island", "table", "stool"],
         "bedroom": ["bed", "dresser", "nightstand", "mirror"],
         "living room": ["sofa", "armchair", "TV stand", "lamp"],
         "bathroom": ["sink", "shower", "towel rack", "toilet"]}

# 1: Simple location prompts
positions = ["left side of the room", "right side of the room", "back of the room", "foreground"]
position_input = "A STYLEROOM_TYPE with a FURNITURE_ITEM_1 in the POSITION_1"
position_edit = "Move the FURNITURE_ITEM_1 to the POSITION_2"
position_output = "A STYLEROOM_TYPE with a FURNITURE_ITEM_1 in the POSITION_2"

# 2: Relative position prompts
rel_positions = {"next to": "closer to", "across from": "away from"}

rel_pos_input = ["A STYLEROOM_TYPE with a FURNITURE_ITEM_1 and a FURNITURE_ITEM_2",
                 "A STYLEROOM_TYPE with a FURNITURE_ITEM_1 REL_POSITION_1 a FURNITURE_ITEM_2"]
rel_pos_edit = "Move the FURNITURE_ITEM_1 REL_POSITION_2 the FURNITURE_ITEM_2"
rel_pos_output = "A STYLEROOM_TYPE with a FURNITURE_ITEM_1 REL_POSITION_2 a FURNITURE_ITEM_2"

# 3: Swap positions
swap_pos_edit = "Swap the position of the FURNITURE_ITEM_1 and the FURNITURE_ITEM_2"

swap_positions = {"on the left side of the room": "on the right side of the room",
                  "in the front of the room": "in the back of the room"}
swap_pos_input = "A STYLEROOM_TYPE with a FURNITURE_ITEM_1 SWAP_POSITION_1 and a FURNITURE_ITEM_2 SWAP_POSITION_2"
swap_pos_output = "A STYLEROOM_TYPE with a FURNITURE_ITEM_1 SWAP_POSITION_2 and a FURNITURE_ITEM_2 SWAP_POSITION_1"

rel_swap_positions = {"to the left of": "to the right of"}
rel_swap_input = "A STYLE ROOM_TYPE with a FURNITURE_ITEM_1 SWAP_POSITION_1 a FURNITURE_ITEM_2"
rel_swap_output = "A STYLE ROOM_TYPE with a FURNITURE_ITEM_1 SWAP_POSITION_2 a FURNITURE_ITEM_2"


def swap_position_prompts(i, trios):
    for room in rooms:
        for style in styles:
            for furniture1 in rooms[room]:
                for furniture2 in rooms[room]:
                    if furniture1 != furniture2:
                        edit_str = swap_pos_edit.replace("FURNITURE_ITEM_1", furniture1)
                        edit_str = edit_str.replace("FURNITURE_ITEM_2", furniture2)

                        for position in swap_positions:
                            in_str = swap_pos_input.replace("STYLE", style)
                            in_str = in_str.replace("ROOM_TYPE", room)
                            in_str = in_str.replace("FURNITURE_ITEM_1", furniture1)
                            in_str = in_str.replace("FURNITURE_ITEM_2", furniture2)
                            in_str = in_str.replace("SWAP_POSITION_1", position)
                            in_str = in_str.replace("SWAP_POSITION_2", swap_positions[position])

                            out_str = swap_pos_output.replace("STYLE", style)
                            out_str = out_str.replace("ROOM_TYPE", room)
                            out_str = out_str.replace("FURNITURE_ITEM_1", furniture1)
                            out_str = out_str.replace("FURNITURE_ITEM_2", furniture2)
                            out_str = out_str.replace("SWAP_POSITION_1", position)
                            out_str = out_str.replace("SWAP_POSITION_2", swap_positions[position])

                            i += 1
                            trio = [in_str, edit_str, out_str]
                            trios.append(trio)

                        for position in rel_swap_positions:
                            in_str = rel_swap_input.replace("STYLE", style)
                            in_str = in_str.replace("ROOM_TYPE", room)
                            in_str = in_str.replace("FURNITURE_ITEM_1", furniture1)
                            in_str = in_str.replace("FURNITURE_ITEM_2", furniture2)
                            in_str = in_str.replace("SWAP_POSITION_1", position)

                            out_str = rel_swap_output.replace("STYLE", style)
                            out_str = out_str.replace("ROOM_TYPE", room)
                            out_str = out_str.replace("FURNITURE_ITEM_1", furniture1)
                            out_str = out_str.replace("FURNITURE_ITEM_2", furniture2)
                            out_str = out_str.replace("SWAP_POSITION_2", rel_swap_positions[position])

                            i += 1
                            trio = [in_str, edit_str, out_str]
                            trios.append(trio)
    return i


def rel_position_prompts(i, trios):
    for room in rooms:
        for style in styles:
            for furniture1 in rooms[room]:
                for furniture2 in rooms[room]:
                    for position1 in rel_positions:
                        for position2 in rel_positions:
                            if position1 != position2 and furniture1 != furniture2:
                                for input_str in rel_pos_input:
                                    in_str = input_str.replace("STYLE", style)
                                    in_str = in_str.replace("ROOM_TYPE", room)
                                    in_str = in_str.replace("FURNITURE_ITEM_1", furniture1)
                                    in_str = in_str.replace("FURNITURE_ITEM_2", furniture2)
                                    in_str = in_str.replace("REL_POSITION_1", position1)

                                    edit_str = rel_pos_edit.replace("FURNITURE_ITEM_1", furniture1)
                                    edit_str = edit_str.replace("FURNITURE_ITEM_2", furniture2)
                                    edit_str = edit_str.replace("REL_POSITION_2", rel_positions[position2])

                                    out_str = rel_pos_output.replace("STYLE", style)
                                    out_str = out_str.replace("ROOM_TYPE", room)
                                    out_str = out_str.replace("FURNITURE_ITEM_1", furniture1)
                                    out_str = out_str.replace("FURNITURE_ITEM_2", furniture2)
                                    out_str = out_str.replace("REL_POSITION_2", position2)

                                    i += 1
                                    trio = [in_str, edit_str, out_str]
                                    trios.append(trio)

    return i


def position_prompts(i, trios):
    for room in rooms:
        for style in styles:
            for furniture in rooms[room]:
                for position1 in positions:
                    for position2 in positions:
                        if position1 != position2:
                            in_str = position_input.replace("STYLE", style)
                            in_str = in_str.replace("ROOM_TYPE", room)
                            in_str = in_str.replace("FURNITURE_ITEM_1", furniture)
                            in_str = in_str.replace("POSITION_1", position1)

                            edit_str = position_edit.replace("FURNITURE_ITEM_1", furniture)
                            edit_str = edit_str.replace("POSITION_2", position2)

                            out_str = position_output.replace("STYLE", style)
                            out_str = out_str.replace("ROOM_TYPE", room)
                            out_str = out_str.replace("FURNITURE_ITEM_1", furniture)
                            out_str = out_str.replace("POSITION_2", position2)

                            if "side" in position1:
                                in_str = in_str.replace(" in ", " on ")

                            if "side" in position2:
                                out_str = out_str.replace(" in ", " on ")

                            i += 1
                            trio = [in_str, edit_str, out_str]
                            trios.append(trio)

    return i


# Run functions and count total
i = 0
prompt_trios = []
i = position_prompts(i, prompt_trios)
i = rel_position_prompts(i, prompt_trios)
i = swap_position_prompts(i, prompt_trios)

print(i)
print(len(prompt_trios))

# writing to csv file
with open("./human_prompts.csv", 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)
    # writing the data rows
    csvwriter.writerows(prompt_trios)

