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

def delete_track_by_name(midi, track_name):
# Deleta a primeira track usando o nome especificado.
    for i, track in enumerate(midi.tracks):
        for msg in track:
            if msg.type == "track_name" and msg.name == track_name:
                del midi.tracks[i]
                print(f"Track '{track_name}' deletada")
                return True
    print(f"Track '{track_name}' não encontrada")
    return False

def copy_events_only(source, target):
#Copia apenas os eventos que não sejam notas (note_on/note_off) e nem track_name.
    cumulative_time = 0
    for msg in source:
        cumulative_time += msg.time
        if msg.type not in ["track_name", "note_on", "note_off"]:
            target.append(msg.copy(time=cumulative_time))
            cumulative_time = 0

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

def copy_notes_by_name(midi, source_name, target_name, note_map):
# Copia notas de uma track para outra, mudando o pitch conforme note_map. Cria a target se não existir.
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
                new_note = note_map[msg.note]
                target.append(Message(msg.type, note=new_note, velocity=msg.velocity, time=cumulative_time))
                cumulative_time = 0

def merge_tracks_by_name(midi, name_a, name_b, merged_name="MERGED"):
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

# Perguntas
# setar o valor para cada variável caso queira conversão direta e remover os input
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

# Processamento em batch
if __name__ == "__main__":
    midi_files = [f for f in glob.glob("*.mid") if not f.endswith("_gh2.mid")]

    if not midi_files:
        print("No MIDI Files Found in This Folder.")
    else:
        for input_path in midi_files:
            print(f"Processing: {input_path}")
            midi = MidiFile(input_path)


            # EXEMPLOS DE USO
            '''
            # Exemplo 1 Deletar Tracks
            delete_track_by_name(midi, "TRACK NAME")

            # Exemplo 2: Renomear track
            rename_track_by_name(midi, "TRACK OLD NAME", "TRACK NEW NAME")

            # Exemplo 3: Copiar eventos de uma track para outra (sem copiar as notas)
            source_name = "PART KEYS"
            new_track_name = "BAND SINGER"
            source_track = get_track_by_name(midi, source_name)
            if source_track:
                new_track = MidiTrack([MetaMessage("track_name", name=new_track_name)])
                copy_events_only(source_track, new_track)
                midi.tracks.append(new_track)

            # Exemplo 4: Mesclar tracks
            merge_tracks_by_name(midi, "TRACK 1", "TRACK 2", merged_name="NEW TRACK")
            '''

            # TRIGGERS TRACK
            # Copiar eventos do PART KEYS para BAND SINGER
            source_name = "PART KEYS"
            new_track_name = "BAND SINGER"
            source_track = get_track_by_name(midi, source_name)
            if source_track:
                new_track = MidiTrack([MetaMessage("track_name", name=new_track_name)])
                copy_events_only(source_track, new_track)
                midi.tracks.append(new_track)
            
            # Copiar notas de DRUMS e KEYFRAMES para tracks TRIGGER temporárias
            copy_notes_by_name(midi, "PART KEYS", "TRIGGER KEYFRAMES", note_map={96: 48, 97: 49, 98: 50, 99: 52})
            copy_notes_by_name(midi, "PART DRUMS", "TRIGGER DRUMS", note_map={96: 24, 97: 25, 98: 26, 100: 26})
            
            # Mesclar os TRIGGER temporários
            merge_tracks_by_name(midi, "TRIGGER KEYFRAMES", "TRIGGER DRUMS", merged_name="TRIGGERS")
            
            # Deletar os TRIGGER temporários
            delete_track_by_name(midi, "TRIGGER KEYFRAMES")
            delete_track_by_name(midi, "TRIGGER DRUMS")
            
            # Deletar PART DRUMS
            delete_track_by_name(midi, "PART DRUMS")


            # Salvar arquivo processado
            base, ext = os.path.splitext(input_path)
            output_path = f"{base}_gh2.mid"
            midi.save(output_path)
            print(f"Saved as: {output_path}\n")

            # Pause de arquivo batch, mas no python
            # (gambiarra extrema)
            print("Press Enter to Exit")
            exit = input()