class ScratchProjectBase:
	def __init__(self):
		self.json = {
	"objName": "Stage",
	"sounds": [{
			"soundName": "pop",
			"soundID": 1,
			"md5": "83a9787d4cb6f3b7632b4ddfebf74367.wav",
			"sampleCount": 258,
			"rate": 11025,
			"format": ""
		}],
	"costumes": [{
			"costumeName": "backdrop1",
			"baseLayerID": 3,
			"baseLayerMD5": "739b5e2a2435f6e1ec2993791b423146.png",
			"bitmapResolution": 1,
			"rotationCenterX": 240,
			"rotationCenterY": 180
		}],
	"currentCostumeIndex": 0,
	"penLayerMD5": "5c81a336fab8be57adc039a8a2b33ca9.png",
	"penLayerID": 0,
	"tempoBPM": 60,
	"videoAlpha": 0.5,
	"children": [
		{
			"objName": "Sprite1",
			"scripts": [[5, 128, [["doRepeat", 5, [["doPlaySoundAndWait", "meow"]]]]]],
			"sounds": [{
					"soundName": "meow",
					"soundID": 0,
					"md5": "83c36d806dc92327b9e7049a565c6bff.wav",
					"sampleCount": 18688,
					"rate": 22050,
					"format": ""
				}],
			"costumes": [{
					"costumeName": "costume1",
					"baseLayerID": 1,
					"baseLayerMD5": "09dc888b0b7df19f70d81588ae73420e.svg",
					"bitmapResolution": 1,
					"rotationCenterX": 47,
					"rotationCenterY": 55
				},
				{
					"costumeName": "costume2",
					"baseLayerID": 2,
					"baseLayerMD5": "3696356a03a8d938318876a593572843.svg",
					"bitmapResolution": 1,
					"rotationCenterX": 47,
					"rotationCenterY": 55
				}],
			"currentCostumeIndex": 0,
			"scratchX": 0,
			"scratchY": 0,
			"scale": 1,
			"direction": 90,
			"rotationStyle": "normal",
			"indexInLibrary": 1,
			"visible": True,
			"spriteInfo": {
			}
		}
	],
	"info": {
		"swfVersion": "v459.1",
		"flashVersion": "MAC 29,0,0,171",
		"scriptCount": 0,
		"spriteCount": 1,
		"userAgent": "Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/66.0.3359.139 Safari\/537.36"
	}
}