#!/usr/bin/env python3
"""
Fugue Generator - Creates a fugue based on a given melody (subject)
"""

import sys
import os
from midiutil import MIDIFile


class Note:
    """Represents a musical note with pitch and duration"""
    
    NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    def __init__(self, name, duration=1.0):
        """
        Initialize a note
        name: Note name like 'C4', 'D#5', or 'REST'
        duration: Duration in beats (1.0 = quarter note)
        """
        self.duration = duration
        if name.upper() == 'REST':
            self.is_rest = True
            self.midi_note = None
            self.name = 'REST'
        else:
            self.is_rest = False
            self.name = name
            self.midi_note = self._parse_note(name)
    
    def _parse_note(self, name):
        """Convert note name to MIDI note number"""
        # Handle both formats: C4 or C-4
        name = name.replace('-', '')
        
        # Extract note name and octave
        note_name = name[:-1]
        octave = int(name[-1])
        
        # Find the note in the chromatic scale
        if note_name not in self.NOTE_NAMES:
            raise ValueError(f"Invalid note name: {note_name}")
        
        # MIDI note number calculation: C4 = 60
        note_index = self.NOTE_NAMES.index(note_name)
        midi_note = (octave + 1) * 12 + note_index
        
        return midi_note
    
    def transpose(self, semitones):
        """Return a new note transposed by the given number of semitones"""
        if self.is_rest:
            return Note('REST', self.duration)
        
        new_midi = self.midi_note + semitones
        
        # Convert back to note name
        octave = (new_midi // 12) - 1
        note_index = new_midi % 12
        note_name = self.NOTE_NAMES[note_index]
        
        return Note(f"{note_name}{octave}", self.duration)
    
    def __str__(self):
        return f"{self.name}({self.duration})"
    
    def __repr__(self):
        return self.__str__()


class Voice:
    """Represents a musical voice (sequence of notes)"""
    
    def __init__(self, notes, start_time=0.0):
        self.notes = notes
        self.start_time = start_time
    
    def transpose(self, semitones):
        """Return a new voice transposed by the given number of semitones"""
        transposed_notes = [note.transpose(semitones) for note in self.notes]
        return Voice(transposed_notes, self.start_time)
    
    def get_duration(self):
        """Get total duration of the voice"""
        return sum(note.duration for note in self.notes)
    
    def __str__(self):
        return " ".join(str(note) for note in self.notes)


class FugueGenerator:
    """Generates a fugue based on a subject melody"""
    
    def __init__(self, subject_notes):
        self.subject = Voice(subject_notes)
        self.voices = []
    
    def generate_fugue(self):
        """
        Generate a basic fugue structure:
        - Voice 1: Subject
        - Voice 2: Answer (subject transposed up a perfect 5th = 7 semitones)
        - Voice 3: Subject again (entry after answer)
        """
        # Voice 1: Subject starts at beginning
        voice1_notes = []
        # Add subject
        for note in self.subject.notes:
            voice1_notes.append(note)
        # Add some accompaniment after subject
        subject_duration = self.subject.get_duration()
        # Add rests during answer
        for _ in range(int(subject_duration)):
            voice1_notes.append(Note('REST', 1.0))
        # Repeat subject for episode
        for note in self.subject.notes:
            voice1_notes.append(note)
        
        voice1 = Voice(voice1_notes, start_time=0.0)
        
        # Voice 2: Answer (starts after subject, transposed up a 5th)
        answer = self.subject.transpose(7)  # 7 semitones = perfect 5th
        voice2_notes = []
        # Add rests while subject plays
        for _ in range(int(subject_duration)):
            voice2_notes.append(Note('REST', 1.0))
        # Add answer
        for note in answer.notes:
            voice2_notes.append(note)
        # Continue with counter-melody (simple descending pattern)
        for note in answer.notes:
            voice2_notes.append(note.transpose(-2))
        
        voice2 = Voice(voice2_notes, start_time=0.0)
        
        # Voice 3: Subject again (starts after answer begins)
        voice3_notes = []
        # Add rests while subject and part of answer play
        rest_duration = subject_duration + subject_duration / 2
        for _ in range(int(rest_duration)):
            voice3_notes.append(Note('REST', 1.0))
        # Add subject
        for note in self.subject.notes:
            voice3_notes.append(note)
        
        voice3 = Voice(voice3_notes, start_time=0.0)
        
        self.voices = [voice1, voice2, voice3]
        
        return self.voices
    
    def to_text(self):
        """Generate text representation of the fugue"""
        lines = []
        lines.append("=" * 60)
        lines.append("FUGUE COMPOSITION")
        lines.append("=" * 60)
        lines.append("")
        lines.append("Subject (Original Melody):")
        lines.append(str(self.subject))
        lines.append("")
        lines.append("=" * 60)
        lines.append("")
        
        for i, voice in enumerate(self.voices, 1):
            lines.append(f"Voice {i}:")
            lines.append(str(voice))
            lines.append("")
        
        lines.append("=" * 60)
        return "\n".join(lines)
    
    def to_midi(self, filename):
        """Generate MIDI file of the fugue"""
        # Create MIDI file with 3 tracks
        midi = MIDIFile(len(self.voices))
        
        tempo = 120  # BPM
        
        for track_num, voice in enumerate(self.voices):
            midi.addTempo(track_num, 0, tempo)
            
            current_time = voice.start_time
            
            for note in voice.notes:
                if not note.is_rest:
                    midi.addNote(
                        track=track_num,
                        channel=track_num,
                        pitch=note.midi_note,
                        time=current_time,
                        duration=note.duration,
                        volume=100
                    )
                current_time += note.duration
        
        with open(filename, 'wb') as output_file:
            midi.writeFile(output_file)


def parse_input_file(filename):
    """
    Parse input file containing notes
    Format: Each line contains a note name and optional duration
    Examples:
        C4 1.0
        D4 0.5
        E4 1.0
        REST 0.5
    """
    notes = []
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            parts = line.split()
            if len(parts) == 1:
                # Just note name, default duration
                notes.append(Note(parts[0], 1.0))
            elif len(parts) == 2:
                # Note name and duration
                notes.append(Note(parts[0], float(parts[1])))
    
    return notes


def main():
    if len(sys.argv) < 2:
        print("Usage: python fuga.py <input_file> [output_prefix]")
        print("  input_file: Text file containing notes for the subject")
        print("  output_prefix: Optional prefix for output files (default: 'fugue')")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_prefix = sys.argv[2] if len(sys.argv) > 2 else 'fugue'
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    
    # Parse input
    print(f"Reading subject from {input_file}...")
    subject_notes = parse_input_file(input_file)
    
    if not subject_notes:
        print("Error: No notes found in input file")
        sys.exit(1)
    
    print(f"Subject contains {len(subject_notes)} notes")
    
    # Generate fugue
    print("Generating fugue...")
    generator = FugueGenerator(subject_notes)
    generator.generate_fugue()
    
    # Generate text output
    text_output = generator.to_text()
    text_filename = f"{output_prefix}.txt"
    with open(text_filename, 'w') as f:
        f.write(text_output)
    print(f"Text output written to {text_filename}")
    
    # Print to console
    print("\n" + text_output)
    
    # Generate MIDI output
    midi_filename = f"{output_prefix}.mid"
    generator.to_midi(midi_filename)
    print(f"MIDI output written to {midi_filename}")
    
    print("\nFugue generation complete!")


if __name__ == '__main__':
    main()
