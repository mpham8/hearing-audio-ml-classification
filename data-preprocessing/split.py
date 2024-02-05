from pydub import AudioSegment
import datetime
import os

def convert_timestamp(timestamp):
    # Convert timestamp string to seconds
    time_object = datetime.datetime.strptime(timestamp, '%H:%M:%S')
    return time_object.hour * 3600 + time_object.minute * 60 + time_object.second

def format_timestamp(timestamp):
    # Add leading zero to hour, minute, and second
    return datetime.datetime.strptime(timestamp, '%H:%M:%S').strftime('%H:%M:%S')

def cut_and_combine_audio(input_mp3, timestamps, persons):
    audio = AudioSegment.from_mp3(input_mp3)

    output_folder = "output1"
    os.makedirs(output_folder, exist_ok=True)

    person_segments = {}

    for timestamp, person in zip(timestamps, persons):
        formatted_timestamp = format_timestamp(timestamp)
        start_time = convert_timestamp(formatted_timestamp)
        end_time = start_time + 5  # Adjust the duration as needed

        cut_audio_segment = audio[start_time * 1000:end_time * 1000]

        if person not in person_segments:
            person_segments[person] = cut_audio_segment
        else:
            person_segments[person] += cut_audio_segment

        cut_wav_file_path = os.path.join(output_folder, f"{person}_{formatted_timestamp}.wav")
        cut_audio_segment.export(cut_wav_file_path, format="wav")

    # Combine audio for each person
    for person, audio_segment in person_segments.items():
        combined_wav_file_path = os.path.join(output_folder, f"{person}_combined.wav")
        audio_segment.export(combined_wav_file_path, format="wav")

if __name__ == "__main__":
    input_mp3_path = "audio.mp3"
    timestamps = [
        "0:00:18", "0:05:21", "0:06:04", "0:07:16", "0:07:34",
        "0:08:36", "0:08:57", "0:09:58", "0:11:42", "0:11:26",
        "0:16:30", "0:16:44", "0:17:00", "0:17:09", "0:17:14",
        "0:17:34", "0:17:42", "0:17:54", "0:17:59", "0:18:55",
        "0:19:43", "0:20:02", "0:20:11", "0:20:45", "0:20:51",
        "0:21:34", "0:21:43", "0:25:37", "0:26:02", "0:27:03",
        "0:27:37"
    ]
    persons = [
        "A", "B", "A", "B", "A", "I", "A", "D", "J", "F",
        "K", "G", "F", "G", "F", "G", "F", "G", "F", "G",
        "F", "G", "F", "G", "F", "G", "F", "G", "H", "G",
        "H", "G", "L"
    ]

    cut_and_combine_audio(input_mp3_path, timestamps, persons)