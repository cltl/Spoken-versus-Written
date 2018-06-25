-- The Places 205 Audio Caption Corpus, Part 1 --

This data is distributed under the Creative Commons Attribution-ShareAlike (CC BY-SA) license.
 
If you use this data, please cite the following three papers:

David Harwath, Antonio Torralba, and James Glass, "Unsupervised Learning of Spoken Language with Visual Context," Advances in Neural Information Processing Systems (NIPS), pp. 1858-1866, Barcelona, Spain, December 2016

David Harwath and James Glass, "Learning Word-Like Units from Joint Audio-Visual Analysis," Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (ACL), pp. 506-517, Vancouver, Canada, July 2017

Bolei Zhou, Agata Lapedriza, Jianxiong Xiao, Antonio Torralba, and Aude Oliva, “Learning Deep Features for Scene Recognition using Places Database,” Advances in Neural Information Processing Systems 27 (NIPS), 2014

You will need to download the Places images separately at http://places.csail.mit.edu

Here is a brief description of what is included in this download:

The wavs/ directory contains 229,388 spoken audio captions in .wav audio format. Each caption describes one image from the Places 205 dataset, and no two captions describe the same image.

The metadata/ directory contains Kaldi-style mappings of utterance IDs to .wav file, speaker, associated image file, and ASR-derived text transcriptions. If you are not familiar with Kaldi, an "utterance ID" is a unique string tag associated with each .wav file. You can think of each file as a hash table with a common key set (these are the utterance IDs) that maps the utterance ID to an attribute - in this case the speaker identifier, location of the caption .wav, associated .jpg image, and ASR hypthesis text.

The lists/ directory contains lists of utterance IDs that were used for training and validation in our NIPS 2016 and ACL 2017 papers. Note that only 224,909 of the .wavs distributed appear in these lists.

The audio is sampled at 16000 Hz with 16-bit depth, and stored in Microsoft WAVE audio format

Note that the ASR-derived transcriptions are errorful (approx 20% WER) and should not be treated as absolute ground truth.

There are various recording artifacts in a small amount of the audio data (estimated ~5%). In some cases, segments of the audio are corrupted while in other cases the recording was cut off.

Enjoy working with the data, and please contact David Harwath at dharwath@csail.mit.edu if you have any questions or encounter any problems.
