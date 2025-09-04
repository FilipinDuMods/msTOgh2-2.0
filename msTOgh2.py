from mido import MidiFile, MidiTrack, MetaMessage, Message
import os
import glob

# --------------------------------------------
# Funções básicas de manipulação de MIDI
# --------------------------------------------

def get_track_by_name(midi, track_name):
# Retorna a primeira track com o nome especificado.
    for track in midi.tracks:
        for msg in track:
            if msg.type == "track_name" and msg.name == track_name:
                return track
    return None

def delete_track(midi, track_name):
# Deleta a primeira track usando o nome especificado.
    for i, track in enumerate(midi.tracks):
        for msg in track:
            if msg.type == "track_name" and msg.name == track_name:
                del midi.tracks[i]
                print(f"Track '{track_name}' deletada")
                return True
    print(f"Track '{track_name}' não encontrada")
    return False

def copy_events_only(midi, source_name, target_name):
    #Copia apenas os eventos que não sejam notas (note_on/note_off) e nem track_name.
    source = get_track_by_name(midi, source_name)
    if not source:
        print(f"Track '{source_name}' não encontrada")
        return None
    target = get_track_by_name(midi, target_name)
    if not target:
        target = MidiTrack([MetaMessage("track_name", name=target_name)])
        midi.tracks.append(target)
    # acumulador de delta relativo
    cumulative_time = 0
    for msg in source:
        cumulative_time += msg.time
        if msg.type not in ["track_name", "note_on", "note_off"]:
            # copia o evento mantendo o delta correto
            target.append(msg.copy(time=cumulative_time))
            cumulative_time = 0
    return target


def rename_track_by_name(midi, old_name, new_name):
# Renomeia a track que tem o nome old_name para new_name.
    track = get_track_by_name(midi, old_name)
    if track:
        for msg in track:
            if msg.type == "track_name" and msg.name == old_name:
                msg.name = new_name
        print(f"Track '{old_name}' renomeada para '{new_name}'")
        return True
    print(f"Track '{old_name}' não encontrada")
    return False

def copy_notes_only(midi, source_name, target_name, note_map):
# Copia somente notas de uma track para outra
    source = get_track_by_name(midi, source_name)
    target = get_track_by_name(midi, target_name)
    if not source:
        print(f"Track '{source_name}' não encontrada")
        return
    if not target:
        target = MidiTrack([MetaMessage("track_name", name=target_name)])
        midi.tracks.append(target)
    cumulative_time = 0
    for msg in source:
        cumulative_time += msg.time
        if msg.type in ["note_on", "note_off"]:
            if msg.note in note_map:
                # transforma em lista pra aceitar tanto int quanto lista
                destinos = note_map[msg.note]
                if not isinstance(destinos, (list, tuple)):
                    destinos = [destinos]
                # pra cada pitch de destino, grava um evento com o mesmo time
                for i, new_note in enumerate(destinos):
                    target.append(Message( msg.type, note=new_note, velocity=msg.velocity, time=cumulative_time if i == 0 else 0))
                cumulative_time = 0

def merge_tracks(midi, name_a, name_b, merged_name="MERGED"):
# Junta duas tracks pelo nome e cria uma nova track com todos os eventos ordenados.
    track_a = get_track_by_name(midi, name_a)
    track_b = get_track_by_name(midi, name_b)
    if not track_a or not track_b:
        print(f"Não foi possível encontrar '{name_a}' ou '{name_b}' para merge")
        return None
    merged = MidiTrack([MetaMessage("track_name", name=merged_name)])
    events_a = []
    events_b = []
    cumulative_time = 0
    for msg in track_a:
        cumulative_time += msg.time
        if msg.type != "track_name":
            events_a.append((cumulative_time, msg))
    cumulative_time = 0
    for msg in track_b:
        cumulative_time += msg.time
        if msg.type != "track_name":
            events_b.append((cumulative_time, msg))
    combined = sorted(events_a + events_b, key=lambda x: x[0])
    prev_time = 0
    for abs_time, msg in combined:
        rel_time = abs_time - prev_time
        merged.append(msg.copy(time=rel_time))
        prev_time = abs_time
    midi.tracks.append(merged)
    print(f"Tracks '{name_a}' e '{name_b}' mescladas em '{merged_name}'")

# --------------------------------------------
# Perguntas para alterar a funcionalidade
# Remova os inputs para deixar automático
# --------------------------------------------
exit = 0 # Coloque 1 para fechar sozinho
click = 1
instrument = 1
metal = 1
print("@ ------------------------------------------------------------------- @")
print("@  IF YOUR CHART IS LEAD/RHYTHM, DON'T FORGET THE GUITAR COOP CHART!  @")
print("@             (you can copy and paste from guitar chart)              @")
print("@ ------------------------------------------------------------------- @")
print("")
print("")
print ("Do you want the drums click in practice mode? (recommended if you are using multitracks)")
print ("Type 1 if yes, 2 if not")
click = input("Please enter 1 or 2: ")
print("")
print ("Is your chart GUITAR/BASS or LEAD/RHYTHM?")
print ("Type 1 if BASS, 2 if RHYTHM")
instrument = input("Please enter 1 or 2: ")
print("")
print("Is your chart 'metal_singer' or 'metal_keys'?")
print("Type 1 if SINGER, 2 if KEYS")
metal = input("Please enter 1 or 2: ")
print("")

# --------------------------------------------
# Processamento em batch
# --------------------------------------------

if __name__ == "__main__":
    midi_files = [f for f in glob.glob("*.mid") if not f.endswith("_gh2.mid")]

    if not midi_files:
        print("No MIDI Files Found in This Folder.")
    else:
        for input_path in midi_files:
            print(f"Processing: {input_path}")
            midi = MidiFile(input_path)


            # --------------------------------------------
            # Exemplos para construir scripts MIDI
            # --------------------------------------------
            '''
            # Exemplo 1 Deletar Tracks
            delete_track(midi, "TRACK NAME")

            # Exemplo 2: Renomear track
            rename_track_by_name(midi, "TRACK OLD NAME", "TRACK NEW NAME")

            # Exemplo 3: Copiar apenas eventos de uma track para outra (sem copiar as notas)
            copy_events_only(midi, "PART DRUMS", "BAND DRUMS EVENTS")

            # Exemplo 4: Copiar apenas notas de uma track para outra (sem copiar eventos)
            copy_notes_only(midi, "PART DRUMS", "BAND DRUMS NOTES", note_map={96: 36, 100: 37})

            # Exemplo 5: Mesclar tracks
            merge_tracks(midi, "TRACK 1", "TRACK 2", merged_name="NEW TRACK")
            '''

            # --------------------------------------------
            # Mapeamentos MIDI
            # --------------------------------------------

            # -----------
            # PART GUITAR
            # -----------
            # Copiar eventos do PART GUITAR para PART GUITAR EVENTS
            copy_events_only(midi, "PART GUITAR", "PART GUITAR EVENTS")
            # Copiar notas de PART GUITAR para PART GUITAR NOTES
            copy_notes_only(midi, "PART GUITAR", "PART GUITAR NOTES", note_map=
            {60:60, 61:61, 62:62, 63:63, 64:64, # easy
            72:72, 73:73, 74:74, 75:75, 76:76, # medium
            84:84, 85:85, 86:86, 87:87, 88:88, # hard
            96:96, 97:97, 98:98, 99:99, 100:100, # expert
            116: [67, 79, 91, 103]}) #star power
            # Deletar o PART GUITAR
            delete_track(midi, "PART GUITAR")
            # Mesclar os PART GUITAR temporários
            merge_tracks(midi, "PART GUITAR EVENTS", "PART GUITAR NOTES", merged_name="PART GUITAR")
            # Deletar os PART GUITAR temporários
            delete_track(midi, "PART GUITAR EVENTS")
            delete_track(midi, "PART GUITAR NOTES")


            # -----------
            # BAND BASS
            # -----------
            # Copiar eventos do PART BASS para BAND BASS EVENTS
            copy_events_only(midi, "PART BASS", "BAND BASS EVENTS")
            # Copiar notas de PART BASS para BAND BASS NOTES
            copy_notes_only(midi, "PART BASS", "BAND BASS NOTES", note_map={96: 36})
            # Mesclar os BAND BASS temporários
            merge_tracks(midi, "BAND BASS EVENTS", "BAND BASS NOTES", merged_name="BAND BASS")
            # Deletar os BAND BASS temporários
            delete_track(midi, "BAND BASS EVENTS")
            delete_track(midi, "BAND BASS NOTES")
            # Deletar o PART BASS
            delete_track(midi, "PART BASS")

            # -----------
            # BAND DRUMS
            # -----------
            # Copiar eventos do PART DRUMS para BAND DRUMS EVENTS
            copy_events_only(midi, "PART DRUMS", "BAND DRUMS EVENTS")
            # Copiar notas de PART DRUMS para BAND DRUMS NOTES
            copy_notes_only(midi, "PART DRUMS", "BAND DRUMS NOTES", note_map={96: 36, 100: 37})
            # Mesclar os BAND DRUMS temporários
            merge_tracks(midi, "BAND DRUMS EVENTS", "BAND DRUMS NOTES", merged_name="BAND DRUMS")
            # Deletar os BAND DRUMS temporários
            delete_track(midi, "BAND DRUMS EVENTS")
            delete_track(midi, "BAND DRUMS NOTES")

            # -----------
            # BAND SINGER/KEYS
            # -----------
            # Copiar eventos do PART KEYS para BAND SINGER/KEYS
            if (metal == '1'): # Se for BAND SINGER
                copy_events_only(midi, "PART KEYS", "BAND SINGER")
            if (metal == '2'): # se for BAND KEYS
                copy_events_only(midi, "PART KEYS", "BAND KEYS")

            # -----------
            # TRIGGERS TRACK
            # -----------
            if (click == '1'): # Com drums no practice
                # Copiar notas de DRUMS e KEYFRAMES para tracks TRIGGER temporárias
                copy_notes_only(midi, "PART KEYS", "TRIGGER KEYFRAMES", note_map={96: 48, 97: 49, 98: 50, 99: 52})
                copy_notes_only(midi, "PART DRUMS", "TRIGGER DRUMS", note_map={96: 24, 97: 25, 98: 26, 100: 26})
                # Mesclar os TRIGGER temporários
                merge_tracks(midi, "TRIGGER KEYFRAMES", "TRIGGER DRUMS", merged_name="TRIGGERS")
                # Deletar os TRIGGER temporários
                delete_track(midi, "TRIGGER KEYFRAMES")
                delete_track(midi, "TRIGGER DRUMS")
                # Deletar PART DRUMS
                delete_track(midi, "PART DRUMS")
                # Deletar PART KEYS
                delete_track(midi, "PART KEYS")
            if (click == '2'): # Sem drums no practice
                # Copiar notas de PART KEYS para TRIGGERS
                copy_notes_only(midi, "PART KEYS", "TRIGGERS", note_map={96: 48, 97: 49, 98: 50, 99: 52})
                # Deletar PART DRUMS
                delete_track(midi, "PART DRUMS")
                # Deletar PART KEYS
                delete_track(midi, "PART KEYS")



            # --------------------------------------------
            # Finalização
            # --------------------------------------------

            # Salvar arquivo processado
            base, ext = os.path.splitext(input_path)
            output_path = f"{base}_gh2.mid"
            midi.save(output_path)
            print(f"Saved as: {output_path}\n")

            # Pause de arquivo batch, mas no python (gambiarra)
            if (exit == 0):
                print("Press Enter to Exit")
                exit = input()