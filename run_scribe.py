from transcribe.render import transcribe

for scribe_object in transcribe('/tmp/stockpile.json', 'stockpile'):
    print(scribe_object)
