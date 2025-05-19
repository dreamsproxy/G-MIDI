import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from tqdm import trange
import mido

def parse_midi(file_path):
    # Load the MIDI file
    midi_file = mido.MidiFile(file_path)

    data = dict()
    times = []
    notes = []
    # Iterate through tracks and messages
    for i, track in enumerate(midi_file.tracks):
        note_cache = dict()
        for msg in track:
            if isinstance(msg, mido.messages.messages.Message):
                msg_dict = msg.dict()
                if 'note' in msg_dict:
                    note = msg_dict['note']
                    velo = msg_dict['velocity']
                    if 'on' in msg_dict['type']:
                        state = True
                    elif 'off' in msg_dict['type']:
                        state = False
                    time = msg_dict['time']
                    note_cache[note] = {'v':velo, 't':time, 's':state}
        #for k in list(note_cache.keys()):
        print(note_cache)
    raise
# Wave propagation function
def wave_propagation(input_wave):
    num_rows, input_length = input_wave.shape
    cols = input_length + 1  # Grid length will be one more than input length
    grid = np.zeros((num_rows, cols))  # Initialize the grid with zeros
    output = np.zeros((num_rows, cols))  # To store the output

    # Propagation loop over time steps
    for t in trange(input_length):
        # Inject input wave at the leftmost column for each row
        grid[:, 0] = input_wave[:, t]
        
        # Update the rest of the grid (propagate wave to the right)
        if t > 0:
            grid[:, 1:] = np.roll(grid[:, :-1], shift=1, axis=1)
        
        # Output collects the values at the last column
        output[:, t] = grid[:, -1]
    
    return output

# Example usage
rows = 128  # This can vary depending on the parsed MIDI data
input_sequences = []

# Process each MIDI file
for p in sorted(glob('./midi/progressions/*.mid')):
    seq = parse_midi(p)  # Assume this returns (rows, input_length)
    print(seq.shape)
    time_steps = seq.shape[1]  # Input length for the sequence
    plt.imshow(seq)
    plt.show()
    raise
    output = wave_propagation(seq)
    # Visualize the output
    plt.imshow(output, aspect='auto', cmap='viridis')
    plt.colorbar(label='Wave amplitude')
    plt.title(f'Wave Propagation Output for {p}')
    plt.xlabel('Time steps')
    plt.ylabel('Rows')
    plt.show()
    raise
