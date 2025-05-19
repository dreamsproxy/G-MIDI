import mido
import numpy as np
from matplotlib import pyplot as plt
from glob import glob
import json

# Note names for reference
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def note_to_name(note_number):
    key = note_number % 12  # Determine key
    octave = (note_number // 12) - 1  # Determine octave
    note_name = NOTE_NAMES[key]  # Get the note name
    return f"{note_name}{octave}"

def parse_midi(file_path, encode:bool = True):
    # Load the MIDI file
    midi_file = mido.MidiFile(file_path)

    note_cache = []
    times = []
    notes = []
    # Iterate through tracks and messages
    for i, track in enumerate(midi_file.tracks):
        for msg in track:
            if isinstance(msg, mido.messages.messages.Message):
                msg_dict = msg.dict()
                if 'note' in msg_dict:
                    note_cache.append(msg_dict)
                    print(msg_dict)
                    times.append(msg_dict['time'])
                    notes.append(msg_dict['note'])

    notes = list(set(notes))
    times = sorted(list(set(times)))
    if encode:
        max_t = 128
    else:
        max_t = times[-1]//2
    post_dict = dict()
    for n in notes:
        post_dict[n] = dict()

    for n in note_cache:
        # Get the note as the new dict key
        k = int(n['note'])
        n_type = n['type']
        t = n['time']
        if 'on' in n_type:
            post_dict[k]['start'] = int(t)
            post_dict[k]['v'] = int(n['velocity'])
        elif 'off' in n_type:
            if encode:
                post_dict[k]['end'] = int(max_t)
            else:
                post_dict[k]['end'] = int(t)

    sequence = np.zeros((128, max_t), dtype=np.int8)  # Create sequence array

    for k in list(post_dict.keys()):
        # Get the note name and print it
        #note_name = note_to_name(k)
        #print(f"Note {k}: {note_name}")
        
        if encode:
            t_range = (post_dict[k]['start'], max_t)
            sequence[k, t_range[0]:t_range[1]] = 1
        else:
            t_range = (post_dict[k]['start'], post_dict[k]['end'])
            sequence[k, t_range[0]:t_range[1]] = post_dict[k]['v']

    return sequence

chord_subdirs = []
for sub_dir in [i.replace('\\', '/') for i in sorted(glob('./midi/full/*/'))]:
    #if len(sub_dir.split('/')[-2]) > 1:
        chord_subdirs.append(sub_dir)

chords_db = dict()
for sdir in chord_subdirs:
    files = [i.replace('\\', '/') for i in sorted(glob(sdir+'*.mid'))]
    g_k = sdir.split('/')[-2]
    group_chords = dict()
    for path in files:
        chord_type, root = path.replace('.mid', '').split('/')[-2:]
        root = root.split(' ')[-1]
        sequence = parse_midi(path)
        enc = sequence[:, 0].tolist()
        group_chords[root] = enc
    chords_db[g_k] = group_chords


with open('chords.json', 'w') as fp:
    json.dump(chords_db, fp)
