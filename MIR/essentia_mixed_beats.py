import os
import numpy as np
import essentia.standard as esst

output_array = np.array([])

with os.scandir("../downloads") as d:
	for entry in d:
		if entry.is_file() and not entry.name.startswith('.DS_Store'):
			mixed_sample = np.array([])
			# Compute all features, aggregate only 'mean' and 'stdev' statistics for all low-level, rhythm and tonal frame
			# features features, features_frames = es.MusicExtractor(lowlevelStats=['mean', 'stdev'], rhythmStats=['mean',
			# 'stdev'], tonalStats=['mean', 'stdev'])('./downloads/'+file) # See all feature names in the pool in a sorted
			# order (str(sorted(features.descriptorNames())))

			# Loading audio file
			audio = esst.MonoLoader(filename=f"../downloads/{entry.name}")()

			# Compute beat positions and BPM
			rhythm_extractor = esst.RhythmExtractor2013(method="multifeature")
			bpm, beats, beats_confidence, _, beats_intervals = rhythm_extractor(audio)

			# print("BPM:", bpm)
			# print("Beat positions (sec.):", beats)
			print("Beat estimation confidence:", beats_confidence)

			for i in range(len(beats)):
				trim = esst.Trimmer(startTime=[*map(lambda x: x - 0.01, beats)][i],
									endTime=[*map(lambda x: x + 0.15, beats)][i]) \
					(audio)

				if len(mixed_sample):
					trim = np.resize(trim, mixed_sample.size)
					stereo_mix = esst.StereoMuxer()(mixed_sample, trim)
					esst.MonoMixer()(stereo_mix, 2)
				else:
					mixed_sample = trim
			output_array = np.concatenate([output_array, mixed_sample])

esst.MonoWriter(filename=f"../samples/mix_beat{str(i)}.mp3")(output_array)

# Mark beat positions on the audio and write it to a file
# Let's use beeps instead of white noise to mark them, as it's more distinctive
# marker = AudioOnsetsMarker(onsets=beats, type='beep')
# marked_audio = marker(audio)
# MonoWriter(filename='../samples/dubstep_beats.flac')(marked_audio)
