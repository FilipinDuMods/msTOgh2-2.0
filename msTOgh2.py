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
                print(f"'{track_name}' deleted")
                return True
    print(f"'{track_name}' not found")
    return False

def rename_track_by_name(midi, old_name, new_name):
# Renomeia a track que tem o nome old_name para new_name.
    track = get_track_by_name(midi, old_name)
    if track:
        for msg in track:
            if msg.type == "track_name" and msg.name == old_name:
                msg.name = new_name
        print(f"'{old_name}' renamed to '{new_name}'")
        return True
    print(f"'{old_name}' not found")
    return False

def ensure_track(midi, track_name):
    # garante que a track exista, criando vazia se não existir
    track = get_track_by_name(midi, track_name)
    if track is None:
        track = MidiTrack([MetaMessage("track_name", name=track_name)])
        midi.tracks.append(track)
    return track


def copy_events_only(midi, source_name, target_name):
    # copia apenas eventos que não sejam nota, cria destino vazio se origem não existir
    target = ensure_track(midi, target_name)
    source = get_track_by_name(midi, source_name)
    if source is None:
        print(f"Track '{source_name}' not found, '{target_name}' stays empty.")
        return target
    cumulative_time = 0
    for msg in source:
        cumulative_time += msg.time
        if msg.type not in ["track_name", "note_on", "note_off"]:
            target.append(msg.copy(time=cumulative_time))
            cumulative_time = 0
    print(f"'{source_name}' events copied to '{target_name}'")
    return target


def copy_notes_only(midi, source_name, target_name, note_map):
    # copia apenas notas, cria destino vazio se origem não existir
    target = ensure_track(midi, target_name)
    source = get_track_by_name(midi, source_name)
    if source is None:
        print(f"Track '{source_name}' not found, '{target_name}' stays empty.")
        return target
    cumulative_time = 0
    for msg in source:
        cumulative_time += msg.time
        if msg.type in ["note_on", "note_off"] and msg.note in note_map:
            destinos = note_map[msg.note]
            if not isinstance(destinos, (list, tuple)):
                destinos = [destinos]
            for i, new_note in enumerate(destinos):
                target.append(Message(msg.type,
                                      note=new_note,
                                      velocity=msg.velocity,
                                      time=cumulative_time if i == 0 else 0))
            cumulative_time = 0
    print(f"'{source_name}' notes copied to '{target_name}'")
    return target


def merge_tracks(midi, name_a, name_b, merged_name="MERGED"):
    # mescla mesmo se uma ou ambas as tracks faltarem (gera vazia se preciso)
    track_a = get_track_by_name(midi, name_a)
    track_b = get_track_by_name(midi, name_b)
    if track_a is None and track_b is None:
        merged = MidiTrack([MetaMessage("track_name", name=merged_name)])
        midi.tracks.append(merged)
        print(f"No '{name_a}' or '{name_b}' to merge; created empty '{merged_name}'.")
        return merged
    events = []
    for track in (track_a, track_b):
        if track is None:
            continue
        abs_time = 0
        for msg in track:
            abs_time += msg.time
            if msg.type != "track_name":
                events.append((abs_time, msg))
    merged = MidiTrack([MetaMessage("track_name", name=merged_name)])
    prev = 0
    for t, msg in sorted(events, key=lambda x: x[0]):
        merged.append(msg.copy(time=t - prev))
        prev = t
    midi.tracks.append(merged)
    print(f"Merged '{name_a}' + '{name_b}' into '{merged_name}'")
    return merged

#########################################################################################################

# --------------------------------------------
# Perguntas para alterar a funcionalidade
# Editar 'exit' e 'auto' para remover.
# --------------------------------------------
exit = 1 # Coloque 1 para fechar sozinho
auto = 1 # Coloque 1 para remover as perguntas

click = '2' # 1 practice drums / 2 no practice drums
instrument = '1' # 1 guitar/bass / 2 lead/rhythm
metal = '1' # 1 band singer / 2 band keys

if (auto == 0):
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

#########################################################################################################

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

#########################################################################################################

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

#########################################################################################################

            # --------------------------------------------
            # Mapeamentos MIDI
            # --------------------------------------------

            # Fretmapping notes
            fretmapping_notes = {98:40, 99:42, 100:44, 95:46, 96:48, 97:50, 86:51, 87:52, 88:53, 83:54, 84:55, 85:56}
            # GUITAR/BASS/COOP/RHYTHM notes
            instrument_notes = {
            60:60, 61:61, 62:62, 63:63, 64:64, # easy
            72:72, 73:73, 74:74, 75:75, 76:76, # medium
            84:84, 85:85, 86:86, 87:87, 88:88, # hard
            96:96, 97:97, 98:98, 99:99, 100:100, # expert
            116: [67, 79, 91, 103] #star power
            }

            # -----------
            # PART GUITAR
            # -----------
            # Copiar eventos do PART GUITAR para PART GUITAR EVENTS
            copy_events_only(midi, "PART GUITAR", "PART GUITAR EVENTS")
            
            # Copiar notas de PART GUITAR para PART GUITAR NOTES
            copy_notes_only(midi, "PART GUITAR", "PART GUITAR NOTES", note_map= instrument_notes)
            
            # Copiar a nota BIG-NOTE (laranja) do PART KEYS para BIG-NOTE e depois PART GUITAR NOTES
            copy_notes_only(midi, "PART KEYS", "BIG-NOTE", note_map={100: 110})
            rename_track_by_name(midi, "PART GUITAR NOTES", "PART GUITAR TEMP")
            merge_tracks(midi, "BIG-NOTE", "PART GUITAR TEMP", merged_name="PART GUITAR NOTES")
            delete_track(midi, "PART GUITAR TEMP")
            delete_track(midi, "BIG-NOTE")
            
            # Copiar notas do PART GUITAR GHL para PART GUITAR NOTES
            copy_notes_only(midi, "PART GUITAR GHL", "GTR FRETMAP", note_map= fretmapping_notes)
            rename_track_by_name(midi, "PART GUITAR NOTES", "PART GUITAR TEMP")
            merge_tracks(midi, "GTR FRETMAP", "PART GUITAR TEMP", merged_name="PART GUITAR NOTES")
            delete_track(midi, "PART GUITAR TEMP")
            delete_track(midi, "GTR FRETMAP")
            delete_track(midi, "PART GUITAR GHL")
            
            # Deletar o PART GUITAR
            delete_track(midi, "PART GUITAR")
            # Mesclar os PART GUITAR temporários
            merge_tracks(midi, "PART GUITAR EVENTS", "PART GUITAR NOTES", merged_name="PART GUITAR")
            # Deletar os PART GUITAR temporários
            delete_track(midi, "PART GUITAR EVENTS")
            delete_track(midi, "PART GUITAR NOTES")

#########################################################################################################

            # -----------
            # PART BASS
            # -----------
            # Copiar eventos do PART BASS para PART BASS EVENTS
            copy_events_only(midi, "PART BASS", "PART BASS EVENTS")
            
            # Copiar notas de PART BASS para PART BASS NOTES
            copy_notes_only(midi, "PART BASS", "PART BASS NOTES", note_map= instrument_notes)
            
            # Copiar notas do PART BASS GHL para PART BASS NOTES
            copy_notes_only(midi, "PART BASS GHL", "BASS FRETMAP", note_map= fretmapping_notes)
            rename_track_by_name(midi, "PART BASS NOTES", "PART BASS TEMP")
            merge_tracks(midi, "BASS FRETMAP", "PART BASS TEMP", merged_name="PART BASS NOTES")
            delete_track(midi, "PART BASS TEMP")
            delete_track(midi, "BASS FRETMAP")
            delete_track(midi, "PART BASS GHL")
            
            # Deletar o PART BASS
            delete_track(midi, "PART BASS")
            # Mesclar os PART BASS temporários
            merge_tracks(midi, "PART BASS EVENTS", "PART BASS NOTES", merged_name="PART BASS")
            # Deletar os PART BASS temporários
            delete_track(midi, "PART BASS EVENTS")
            delete_track(midi, "PART BASS NOTES")

#########################################################################################################

            # -----------
            # PART GUITAR COOP
            # -----------
            # Copiar eventos do PART GUITAR COOP para PART GUITAR COOP EVENTS
            copy_events_only(midi, "PART GUITAR COOP", "PART GUITAR COOP EVENTS")
            
            # Copiar notas de PART GUITAR COOP para PART GUITAR COOP NOTES
            copy_notes_only(midi, "PART GUITAR COOP", "PART GUITAR COOP NOTES", note_map= instrument_notes)
            
            # Copiar notas do PART GUITAR COOP GHL para PART GUITAR COOP NOTES
            copy_notes_only(midi, "PART GUITAR COOP GHL", "COOP FRETMAP", note_map= fretmapping_notes)
            rename_track_by_name(midi, "PART GUITAR COOP NOTES", "PART GUITAR COOP TEMP")
            merge_tracks(midi, "COOP FRETMAP", "PART GUITAR COOP TEMP", merged_name="PART GUITAR COOP NOTES")
            delete_track(midi, "PART GUITAR COOP TEMP")
            delete_track(midi, "COOP FRETMAP")
            delete_track(midi, "PART GUITAR COOP GHL")
            
            # Deletar o PART GUITAR COOP
            delete_track(midi, "PART GUITAR COOP")
            # Mesclar os PART GUITAR COOP temporários
            merge_tracks(midi, "PART GUITAR COOP EVENTS", "PART GUITAR COOP NOTES", merged_name="PART GUITAR COOP")
            # Deletar os PART GUITAR COOP temporários
            delete_track(midi, "PART GUITAR COOP EVENTS")
            delete_track(midi, "PART GUITAR COOP NOTES")

#########################################################################################################

            # -----------
            # PART RHYTHM
            # -----------
            # Copiar eventos do PART RHYTHM para PART RHYTHM EVENTS
            copy_events_only(midi, "PART RHYTHM", "PART RHYTHM EVENTS")
            
            # Copiar notas de PART RHYTHM para PART RHYTHM NOTES
            copy_notes_only(midi, "PART RHYTHM", "PART RHYTHM NOTES", note_map= instrument_notes)
            
            # Copiar notas do PART RHYTHM GHL para PART RHYTHM NOTES
            copy_notes_only(midi, "PART RHYTHM GHL", "RHYTHM FRETMAP", note_map= fretmapping_notes)
            rename_track_by_name(midi, "PART RHYTHM NOTES", "PART RHYTHM TEMP")
            merge_tracks(midi, "RHYTHM FRETMAP", "PART RHYTHM TEMP", merged_name="PART RHYTHM NOTES")
            delete_track(midi, "PART RHYTHM TEMP")
            delete_track(midi, "RHYTHM FRETMAP")
            delete_track(midi, "PART RHYTHM GHL")
            
            # Deletar o PART RHYTHM
            delete_track(midi, "PART RHYTHM")
            # Mesclar os PART RHYTHM temporários
            merge_tracks(midi, "PART RHYTHM EVENTS", "PART RHYTHM NOTES", merged_name="PART RHYTHM")
            # Deletar os PART RHYTHM temporários
            delete_track(midi, "PART RHYTHM EVENTS")
            delete_track(midi, "PART RHYTHM NOTES")

#########################################################################################################

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

#########################################################################################################

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

#########################################################################################################

            # -----------
            # BAND SINGER/KEYS
            # -----------
            # Copiar eventos do PART KEYS para BAND SINGER/KEYS
            if (metal == '1'): # Se for BAND SINGER
                copy_events_only(midi, "PART KEYS", "BAND SINGER")
            if (metal == '2'): # se for BAND KEYS
                copy_events_only(midi, "PART KEYS", "BAND KEYS")

#########################################################################################################

            # -----------
            # EVENTS TRACK
            # -----------
            # Copiar eventos do EVENTS para EVENTS (formatação)
            copy_events_only(midi, "EVENTS", "EVENTS FORMAT")
            delete_track(midi, "EVENTS")
            rename_track_by_name(midi, "EVENTS FORMAT", "EVENTS")

#########################################################################################################

            # -----------
            # TRIGGERS TRACK
            # -----------
            if (click == '1'): # Com drums no practice
                # Copiar notas de DRUMS e KEYFRAMES para tracks TRIGGER temporárias
                copy_notes_only(midi, "PART KEYS", "TRIGGER KEYFRAMES", note_map=
                {96: 48, 97: 49, 98: 50, 99: 52})
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

#########################################################################################################

            # Remoção de tracks por escolha
            if (instrument == '1'):
                delete_track(midi, "PART GUITAR COOP")
                delete_track(midi, "PART RHYTHM")
            if (instrument == '2'):
                delete_track(midi, "PART BASS")

#########################################################################################################

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