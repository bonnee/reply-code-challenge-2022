#!/usr/bin/pyton

#file_name = "00-example.txt"
#file_name = "01-the-cloud-abyss.txt"
#file_name = "02-iot-island-of-terror.txt"
file_name = "03-etheryum.txt"  # da fare in up
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
DF_turns = DS_up_idx + 1  # demon fragments

demons = []

for i in range(0, numb_demons):
    demons.append(list(map(int, f.readline().strip().split())))
    demons[i].insert(0, i)

    # remove unusable fragments

    if(demons[i][DF_turns] > TURNS):
        ##demons[i] = list(demons[i][DF_turns:DF_turns+TURNS-1])
        list_of_obtainable_fragments = list(
            demons[i][DF_turns+1:DF_turns+1+TURNS])
    else:
        list_of_obtainable_fragments = demons[i][DF_turns+1:]

        ##tot_obtainable_fragments = sum(demons[DF_turns:])
    tot_obtainable_fragments = sum(list_of_obtainable_fragments)
    demons[i].append(tot_obtainable_fragments)
#demons = sorted(demons, key=lambda x: (x[DS_dwn_idx]))
#demons = sorted(demons, key=lambda x: (x[DS_up_idx]))

# sort by total obtainable fragments
demons = list(sorted(demons, key=lambda x: (x[-1])))
demons.reverse()

take_demon_order = []

for turn in range(0, TURNS):
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
            # print("HO UCCISO QUALCOSA")
            break
        else:
            if(stamina < 5):
                break
            # print(
            #    f"demon {dem} with stamina {demons[dem][DS_dwn_idx]} too strong current stamina {stamina}")
            pass

print(take_demon_order)
with open(file_name+"_result.txt", "w") as f:
    for demon in take_demon_order:
        f.write(str(demon)+"\n")
