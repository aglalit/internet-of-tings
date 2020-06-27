import os
import sys
import numpy
import fs

import essentia
import essentia.standard as es

pool = essentia.Pool()
samples_array = numpy.array([])

mixed_samples_array = numpy.array([])

downloads = os.listdir("../downloads")


for f in range(64):
	if (downloads[f] != '.DS_Store'):
		#  Compute all features, aggregate only 'mean' and 'stdev' statistics for all low-level, rhythm and tonal frame features
		#  features, features_frames = es.MusicExtractor(lowlevelStats=['mean', 'stdev'],
		#                                    rhythmStats=['mean', 'stdev'],
		#                                    tonalStats=['mean', 'stdev'])('./downloads/'+file)
		#  # See all feature names in the pool in a sorted order
		#  (str(sorted(features.descriptorNames())))
		from essentia.standard import *

		# Loading audio file
		full_file_path = os.path.join("../downloads", downloads[f])
		print(full_file_path)
		audio = MonoLoader(filename=full_file_path)()

		# Compute beat positions and BPM
		rhythm_extractor = RhythmExtractor2013(method="multifeature")
		bpm, beats, beats_confidence, _, beats_intervals = rhythm_extractor(audio)

		print("BPM:", bpm)
		print("Beat positions (sec.):", beats)
		print("Beat estimation confidence:", beats_confidence)

		# frame_to_real = FrameToReal()

		mixed_sample = [];

		for i in range(len(beats)):
			trim = Trimmer(startTime=[*map(lambda x: x - 0.01, beats)][i],
			                  endTime=[*map(lambda x: x + 0.15, beats)][i])\
								(audio)
			pool.add('samples.beats', trim)
			# samples_array.append(trim)
			# print(trim)
			# MonoWriter(filename='../samples/' + filename + '_' + 'beat' + str(i) + '.mp3')(pool['samples.beats'][i])

			if (len(mixed_sample)):
				trim = numpy.resize(trim, mixed_sample.size)
				stereo_mix = StereoMuxer()(mixed_sample, trim)
				MonoMixer()(stereo_mix, 2)
			else: mixed_sample = trim

		print(str(pool['samples.beats'][0]))

	samples_array = numpy.concatenate([samples_array, mixed_sample])

samples_array = numpy.concatenate([samples_array, samples_array])
samples_array = numpy.concatenate([samples_array, samples_array])

samples_array = numpy.concatenate([samples_array, samples_array])



#numpy.random.shuffle(samples_array)

MonoWriter(filename='../samples/' + 'mix' + '_' + 'beat' + str(i) + '.mp3')(samples_array)

	# Mark beat positions on the audio and write it to a file
	# Let's use beeps instead of white noise to mark them, as it's more distinctive
	# marker = AudioOnsetsMarker(onsets=beats, type='beep')
	# marked_audio = marker(audio)
	# MonoWriter(filename='../samples/dubstep_beats.flac')(marked_audio)
