import os

# Get parameters
w,h = 24,24
numPos = len(os.listdir('imgs/positive_imgs')) - len(os.listdir('imgs/img_teste'))
numNeg = len(os.listdir('imgs/negative_imgs'))
numStages = 6
path = 'C:/Users/raaro/OneDrive/Documentos/CS/S6/PoleP/rec_obj/cascade/cascade3'

# Command opencv_createsamples
createsamples = "opencv_createsamples "
createsamples += '-bg bg.txt '
createsamples += '-info annotations.txt '
createsamples += '-num '+str(numPos)+' '
createsamples += '-w '+str(w)+' '
createsamples += '-h '+str(h)+' '
createsamples += '-vec positives.vec'
os.system(createsamples) # Run command

# Command opencv_traincascadecascade
traincascade ='opencv_traincascade '
traincascade += f'-data {path} '
traincascade += '-vec positives.vec '
traincascade += '-bg bg.txt '
traincascade += '-numPos '+str(numPos)+' '
traincascade += '-numNeg '+str(numNeg)+' '
traincascade += '-numStages '+str(numStages)+' '
traincascade += '-w '+str(w)+' '
traincascade += '-h '+str(h)+' '
traincascade += '-precalcValBufSize 4048 '
traincascade += '-precalcIdxBufSize 4048 '
traincascade += '-maxFalseAlarmRate 0.05 '
os.system(traincascade) # Run command
