# Fuga - Fugue Generator

A Python program that generates a fugue (musical composition) based on a given melody (subject).

## Description

This program takes a simple melody as input and creates a three-voice fugue following traditional fugue structure:
- **Voice 1**: Presents the subject (original melody)
- **Voice 2**: Presents the answer (subject transposed up a perfect 5th)
- **Voice 3**: Re-enters with the subject

The program outputs both a text representation and a MIDI file that can be played with any MIDI player or imported into music notation software.

## Installation

1. Clone this repository
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

```bash
python fuga.py <input_file> [output_prefix]
```

### Arguments
- `input_file`: Text file containing the subject melody (required)
- `output_prefix`: Prefix for output files (optional, default: 'fugue')

### Example

```bash
python fuga.py example_subject.txt my_fugue
```

This will generate:
- `my_fugue.txt` - Text representation of the fugue
- `my_fugue.mid` - MIDI file of the fugue

## Input File Format

The input file should contain notes in a simple text format, one note per line.

### Format
```
NoteName Duration
```

- **NoteName**: Musical note (e.g., C4, D4, E4, F#4, Bb4, REST)
  - C4 is middle C
  - Add # for sharp (C#4)
  - Use REST for rests
- **Duration**: Number of beats (optional, default: 1.0)
  - 1.0 = quarter note
  - 0.5 = eighth note
  - 2.0 = half note
  - 4.0 = whole note

### Example Input File

```
# Simple ascending melody
C4 1.0
D4 1.0
E4 1.0
F4 1.0
G4 2.0
E4 1.0
C4 1.0
D4 2.0
```

Lines starting with `#` are comments and will be ignored.

## Output

### Text Output
The text output shows:
1. The original subject
2. All three voices with their complete note sequences

### MIDI Output
The MIDI file contains three tracks (one per voice) that can be:
- Played with any MIDI player
- Imported into music notation software (MuseScore, Finale, Sibelius, etc.)
- Used in digital audio workstations (DAWs)

## Example

Try the included example:
```bash
python fuga.py example_subject.txt
```

This will create `fugue.txt` and `fugue.mid` based on the example subject.

## Musical Theory

A fugue is a contrapuntal composition technique featuring multiple voices. This generator implements:
- **Subject**: The main theme presented first
- **Answer**: The subject transposed (typically up a perfect 5th, or 7 semitones)
- **Counter-subject**: Accompanying material that complements the subject and answer
- **Episodes**: Transitional sections between subject entries

The generated fugues follow a simplified classical fugue structure suitable for educational purposes and basic composition experiments.

## License

MIT License