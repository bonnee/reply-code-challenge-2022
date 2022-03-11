#!/usr/bin/pyton

#file_name = "00-example.txt"
file_name = "01-the-cloud-abyss.txt"
#file_name = "02-iot-island-of-terror.txt"
# file_name = "03-etheryum.txt"  # da fare in up
#file_name = "04-the-desert-of-autonomous-machines.txt"
#file_name = "05-androids-armageddon.txt"
f = open(file_name, "r")
firstline = f.readline().strip().split()

stamina = int(firstline[0])
max_stamina = int(firstline[1])
TURNS = int(firstline[2])
numb_demons = int(firstline[3])

stamina_timeline = [0]*TURNS

# Demon Stamina i
D_idx = 0
DS_dwn_idx = D_idx+1
DS_delay_idx = DS_dwn_idx+1
DS_up_idx = DS_delay_idx+1
DF_turns_idx = DS_up_idx + 1  # demon fragments

demons = []
for i in range(0, numb_demons):
    # this block must be copied
    demons.append(list(map(int, f.readline().strip().split())))
    demons[i].insert(0, i)
    # this block must be copied

    # remove unusable fragments

    if(demons[i][DF_turns_idx] > TURNS):
        # demons[i] = list(demons[i][DF_turns_idx:DF_turns_idx+TURNS-1])
        list_of_obtainable_fragments = list(
            demons[i][DF_turns_idx+1:DF_turns_idx+1+TURNS])
        # the number of fragments obtainable by this demon is not its default but turns
        demons[i][DF_turns_idx] = TURNS
    else:
        list_of_obtainable_fragments = demons[i][DF_turns_idx+1:]

        # tot_obtainable_fragments = sum(demons[DF_turns_idx:])
    tot_obtainable_fragments = sum(list_of_obtainable_fragments)
    # weight = demons[i][DS_dwn_idx]/
    demons[i].append(tot_obtainable_fragments)
# demons = sorted(demons, key=lambda x: (x[DS_dwn_idx]))
# demons = sorted(demons, key=lambda x: (x[DS_up_idx]))

# sort by total obtainable fragments
demons = list(sorted(demons, key=lambda x: (x[-1])))
demons.reverse()

take_demon_order = []

# for i in demons:
#    print(i)
for turn in range(0, TURNS):
    print(f"{turn}/{TURNS}\n")
    # Increment stamina
    stamina = min(max_stamina, stamina+stamina_timeline[turn])

    # print(f"[{turn}] stamina: {stamina} stamina_timeline: {stamina_timeline}")

    for dem in range(0, len(demons)):

        if(stamina > demons[dem][DS_dwn_idx]):
            # ok I take the demon

            # where to put the next stamina power up
            next_stamina_up_idx = turn+demons[dem][DS_delay_idx]
            # schedule stamina increase

            # can I insert a new stamina power up
            if(next_stamina_up_idx < TURNS):
                stamina_timeline[next_stamina_up_idx] += demons[dem][DS_up_idx]

            stamina -= demons[dem][DS_dwn_idx]

            # take monster
            take_demon_order.append(demons[dem][D_idx])
            del demons[dem]

            # Max gettable fragments of all demons get reduced
            for upd_demon in demons:

                # the number of truns obtainable fragments of this demon is decremented
                number_of_turns_to_collect_fragments = upd_demon[DF_turns_idx]

                # If number of turns to collect fragments of this demon is greater to the number of remaining turns, then we need to decrease it
                if(number_of_turns_to_collect_fragments > TURNS-turn-1):
                    # number_of_turns_to_collect_fragments
                    #  |
                    #  V
                    # [3 . . . ] but we have 10 turns
                    not_obtainable_fragment_value = upd_demon[DF_turns_idx +
                                                              number_of_turns_to_collect_fragments]
                    upd_demon[-1] -= not_obtainable_fragment_value

                    # decrease the number of ubtainable fragments (turns) from this demon
                    upd_demon[DF_turns_idx] -= 1

            # sort another time for the total obtainable fragments

            demons = list(sorted(demons, key=lambda x: (x[-1])))
            demons.reverse()
            # print("updated demons after take")
            # for i in demons:
            #    print(i)
            break
        else:
            if(stamina < 2):
                break
            # print(
            #    f"demon {dem} with stamina {demons[dem][DS_dwn_idx]} too strong current stamina {stamina}")
            pass

print(take_demon_order)
with open(file_name+"_result.txt", "w") as f:
    for demon in take_demon_order:
        f.write(str(demon)+"\n")
