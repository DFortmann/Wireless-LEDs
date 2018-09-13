import os

class Saver():

	def __init__(self):
		self.Frames = []
		self.movie = op('moviefilein1')
		self.out = op('null1')		
		self.gamma = bytearray(256)
		
		for i in range(256):
			self.gamma[i] = int(pow(float(i) / 255.0, 2.7) * 255.0 + 0.5)
			
		self.folders = []
		
		for i in range(1,11):
			self.folders.append('/Output/Gilet' + str(i))
		for i in range(1,11):
			self.folders.append('/Output/Snare' + str(i))
			
		self.lookups = []
		
		for i in range(1,11):
			self.lookups.append(op('g' + str(i) + 'Table'))
		for i in range(1,11):
			self.lookups.append(op('s' + str(i) + 'Table'))
		return

	def Save(self):
		numFrames = self.movie.numImages
		height = self.movie.fileHeight
		width = self.movie.fileWidth
		name = parent().par.Name
		
		self.movie.par.index = 0
		self.movie.cook(force=True)
				
		for i in range(len(self.folders)):
			lookup = self.lookups[i]
			path = project.folder + self.folders[i]
			
			if not os.path.exists(path):
				os.makedirs(path)
		
			self.Frames = []
			
			for i in range(0, numFrames):
				self.movie.par.index = i
				self.movie.cook(force=True)
				pixs = self.GetPixs(lookup, height)
				self.CheckSum(pixs, 1)
				self.CheckSum(pixs, 2)
				self.SaveFrame(pixs)
				
			with open(path + '/' + name + '.txt', 'w') as fp:
				fp.write("".join(self.Frames))
				
		return
		
	def GetPixs(self, lookup, height):
		pixs = []
		
		for row in range(lookup.numRows):
			sample = self.out.sample(x=lookup[row, 0],y=height-1-lookup[row, 1])
			
			r = self.gamma[int(sample[0]*255)]
			g = self.gamma[int(sample[1]*255)]
			b = self.gamma[int(sample[2]*255)]

			pixs.append([r,g,b])
		return pixs
		
	def CheckSum(self, pixs, half):
		halfSize = int(len(pixs) / 2)
		start = halfSize * (half - 1)
		sum = 0
		
		for i in range(start, halfSize * half):
			pix = pixs[i]
			sum += ((pix[0] / 255) * 0.02)
			sum += ((pix[1] / 255) * 0.02)
			sum += ((pix[2] / 255) * 0.02)

		if sum > 2.9:	
			overDraw = sum / 2.9
			#newSum = 0
			for row in range(start, halfSize * half):
				for c in range(3):
					pixs[row][c] = pixs[row][c] / overDraw	
					#newSum += (pixs[row][c] / overDraw / 255) * 0.02
		return
		
	def SaveFrame(self, pixs):
		for pix in pixs:
			self.Frames.append('{:02x}'.format(255))
			self.Frames.append('{:02x}'.format(int(pix[2])))
			self.Frames.append('{:02x}'.format(int(pix[1])))
			self.Frames.append('{:02x}'.format(int(pix[0])))

		self.Frames.append('\n')
		return
