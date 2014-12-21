'''
sudople---offer solution to sudoku game

sudople = "sudo" + reverse("help")

Author: Zex Lynch
'''

class sudople:

	def __init__(self, matrix, row, col):

		self.oriMatrix = matrix		#original sudo matrix
		self.newMatrix = matrix		#solution matrix
		self.row = row			#total row of sudo matrix
		self.col = col			#total column of sudo matrix
		self.posList = dict()		#possible list of each empty cell
			
	def get_orimatrix(self):
		
		return self.oriMatrix

	def get_newmatrix(self):
		
		return self.newMatrix

	def print_orimatrix(self):
		
		for i in range(self.row):
			print self.oriMatrix[i]

	def print_newmatrix(self):
		
		for i in range(self.row):
			print self.newMatrix[i]

	'''
	are they the same cell
	'''
	def ishimself(self, i1, j1, i2, j2):

		if (i1 == i2) and (j1 == j2):
			return True
		return False
	'''
	are they in the same 3x3 cell?
	'''
	def insame3cell(self, i1, j1, i2, j2):

		if (i1/3 == i2/3) and (j1/3 == j2/3):
			return True
		return False

	'''
	is this number a possible value?
	'''
	def ispossible(self, value, row, col):
		
		'''check row'''
		for j in range(self.col):
			if value == self.newMatrix[row][j]:
				return False
		
		'''check column'''
		for i in range(self.row):
			if value == self.newMatrix[i][col]:
				return False
		
		'''check 3x3 cell'''
		for i in range(self.row):
			for j in range(self.col):
				if not self.ishimself(i, j, row, col) \
					and self.insame3cell(i, j, row, col) \
					and value == self.newMatrix[i][j]:
						return False

		return True

	'''
	get possible list of each empty cell
	'''
	def get_possible_list(self):
		
		for i in range(self.row):
			for j in range(self.col):
				if self.newMatrix[i][j] == 0:
					self.posList[str(i)+str(j)] = []
					for val in range(1, 10):
						if self.ispossible(val, i, j):
							self.posList[str(i)+str(j)].append(val)

		return self.posList

	'''
	is this value exist in this list?
	'''
	def exist_in(self, val, alist):

		for i in range(len(alist)):
			if val == alist[i]:
				return i
		return -1		

	'''
	does this guy has a brother in the same row or column?
	'''
	def istwinlist(self, list1, list2):

		if len(list1) != len(list2):return False
		lenght = len(list1)

		for i in range(lenght):
			if self.exist_in(list1[i], list2) == -1:
				return False
		return True

	'''
	clean rubbish,remove impossible value from each possible list
	'''
	def clean_rub(self, tagi, tagj):

		for i in range(self.row):
			for j in range(self.col):
				if self.posList.has_key(str(i)+str(j)):
					ind = self.exist_in(self.newMatrix[tagi][tagj], self.posList[str(i)+str(j)])
					if ind > -1 and \
						not self.ispossible(self.posList[str(i)+str(j)][ind], i, j):
						self.posList[str(i)+str(j)].pop(ind)
					
		del(self.posList[str(tagi)+str(tagj)])
		print '...............clean_rub'
		self.print_pos_list()

	'''
		for i in range(self.row):
			for j in range(self.col):
				if self.posList.has_key(str(i)+str(j)):
					print (i, j),self.posList[str(i)+str(j)]
	'''

	'''
	is each possible list empty?
	'''
	def each_pos_list_empty(self):

		for i in range(self.row):
			for j in range(self.col):
				if self.posList.has_key(str(i)+str(j)):
					return False
		return True

	'''
	is there any empty cell
	'''
	def no_empty_cell(self):

		for i in range(self.row):
			for j in range(self.col):
				if newMatrix[i][j] == 0:return False
		return True

	'''
	check big triangle model,which has 4 or more value in possible list of corner cell
	ex:1467........17
	   :
	   :
	   17
	in this case, 1 and 7 in 1467 should be removed
	'''
	def slim_big_triangle(self, tagi, tagj):

		'''check row'''
		for j in range(self.col):
			if self.posList.has_key(str(tagi)+str(j)) and \
				len(self.posList[str(tagi)+str(j)]) == 2:
				ind_c = []
				tri_row = 0
				
				for x in range(2):
					indr = self.exist_in(self.posList[str(tagi)+str(j)][x], \
						self.posList[str(tagi)+str(tagj)])
					if indr > -1:
						tri_row += 1
						ind_c.append(self.posList[str(tagi)+str(tagj)][indr])
						print self.posList[str(tagi)+str(j)],self.posList[str(tagi)+str(tagj)][indr],(tagi,j)
				print "slim_triangle::checking row",ind_c
				if tri_row == 2:
					'''check column'''
					print "slim_triangle::checking col"
					for i in range(self.row):
						if self.posList.has_key(str(i)+str(tagj)) and \
							len(self.posList[str(i)+str(tagj)]) == 2:
							tri_col = 0
							for x in range(2):
								indl = self.exist_in(self.posList[str(i)+str(tagj)][x], \
									self.posList[str(tagi)+str(tagj)])
								if indl > -1:tri_col += 1
							if tri_col == 2 and \
							  self.exist_in(self.posList[str(i)+str(tagj)][0], ind_c) != -1 and \
							  self.exist_in(self.posList[str(i)+str(tagj)][1], ind_c) != -1:
								print "ind_c in slim_triangle",ind_c
								for k in ind_c:
									print "k in ind_c in slim_::::",k
									ind = self.posList[str(tagi)+str(tagj)].index(k)
									self.posList[str(tagi)+str(tagj)].pop(ind)
								return True
							
		return False
		
	'''
	check triangle model
	ex:	145........14
		.
		.
		14
		
		this is a triangle model.5 would be returned.
	'''
	def istriangle(self, tagi, tagj):
		
		'''check row'''
		for j in range(self.col):
			if self.posList.has_key(str(tagi)+str(j)) and \
				len(self.posList[str(tagi)+str(j)]) == 2:

				ind_c = []
				tri_row = 0

				for x in range(2):
					indr = self.exist_in(self.posList[str(tagi)+str(j)][x], \
						self.posList[str(tagi)+str(tagj)])
					if indr > -1:
						tri_row += 1
						ind_c.append(self.posList[str(tagi)+str(tagj)][indr])

				if indr == 2:		
					'''check column'''
					for i in range(self.row):
						if self.posList.has_key(str(i)+str(tagj)) and \
							len(self.posList[str(i)+str(tagj)]) == 2:
		
							tri_col = 0

							for x in range(2):
								indl = self.exist_in(self.posList[str(i)+str(tagj)][x], \
									self.posList[str(tagi)+str(tagj)])
								if indl > -1:tri_col += 1
							if indl == 2 and \
							  self.exist_in(self.posList[str(i)+str(tagj)][0],ind_c) != -1 and \
							  self.exist_in(self.posList[str(i)+str(tagj)][1],ind_c) != -1:

								for k in ind_c:
									ind = self.posList[str(tagi)+str(tagj)].index(k)
								   	self.posList[str(tagi)+str(tagj)].pop(ind)
								return self.posList[str(tagi)+str(tagj)][0]
							
		return 0

	'''
	print all possible lists
	'''
	def print_pos_list(self):

		for i in range(self.row):
			for j in range(self.col):
				if self.posList.has_key(str(i)+str(j)):
					print self.posList[str(i)+str(j)],
				else:
					print "::",
			print

	'''
	is there a uniq value in this 3x3 cell?
	if a number does not have twin brother in other possible lists in same 3x3 cell,
	this number is a uniq value.
	has_3x3_uniq_val---determine a possible list does/doesn't own a uniq value
	True:	return uniq value(1..9)
	False:	return False
	'''
	def has_3x3_uniq_val(self, tagi, tagj):

		cnt = []

		while len(cnt) != len(self.posList[str(tagi)+str(tagj)]):
			cnt.append(0)
		'''
		check uniq value in 3x3 cell
		'''
		for i in range(self.row):
			for j in range(self.col):
				if self.insame3cell(i, j, tagi, tagj) and \
					self.posList.has_key(str(i)+str(j)):
					for x in range(len(self.posList[str(tagi)+str(tagj)])):
						if self.exist_in(self.posList[str(tagi)+str(tagj)][x], \
							self.posList[str(i)+str(j)]) != -1:
							cnt[x] += 1

		for i in cnt:
			if i == 1:
				return self.posList[str(tagi)+str(tagj)][cnt.index(i)]

		return False

	'''
	determine possible list has/hasn't uniq value in row
	if a possible list has uniq value in possible lists of a row
	this value fits this cell which own former possible list
	'''
	def has_row_uniq_val(self, tagi, tagj):
		
		cnt = []

		while len(cnt) != len(self.posList[str(tagi)+str(tagj)]):
			cnt.append(0)

		for j in range(self.col):
			if self.posList.has_key(str(tagi)+str(j)):
				for x in range(len(self.posList[str(tagi)+str(tagj)])):
					if self.exist_in(self.posList[str(tagi)+str(tagj)][x], \
					  self.posList[str(tagi)+str(j)]) != -1:
					  cnt[x] += 1
		for k in cnt:
			if k == 1:
				return self.posList[str(tagi)+str(tagj)][cnt.index(k)]
		return False
	
	'''
	determine a possible list has/hasn't uniq value in column
	if a possible list has uniq value in possible lists of a column
	this value fits this cell which own former possible list
	'''
	def has_col_uniq_val(self, tagi, tagj):
		
		cnt = []

		while len(cnt) != len(self.posList[str(tagi)+str(tagj)]):
			cnt.append(0)

		for i in range(self.row):
			if self.posList.has_key(str(i)+str(tagj)):
				for x in range(len(self.posList[str(tagi)+str(tagj)])):
					if self.exist_in(self.posList[str(tagi)+str(tagj)][x], \
					  self.posList[str(i)+str(tagj)]) != -1:
					  cnt[x] += 1
		for k in cnt:
			if k == 1:
				return self.posList[str(tagi)+str(tagj)][cnt.index(k)]
		return False

	'''
	is this possible list has uniq value?
	true: return uniq value
	false: return false
	'''
	def hasuniqval(self, tagi, tagj):

		'''
		check uniq value in row
		'''
		v = self.has_row_uniq_val(tagi, tagj)
		if v: print 'row uniq val';return v
		'''
		check uniq value in column
		'''
		v = self.has_col_uniq_val(tagi, tagj)
		if v: print 'col uniq val';return v
		'''
		check 3x3 cell
		'''
		v = self.has_3x3_uniq_val(tagi, tagj)
		if v: print '3x3';return v

		return False

	'''
	this guy has a twin brother in the same row
	'''
	def exist_twins_in_row(self, tagi, tagj):

		for j in range(self.col):
			if self.posList.has_key(str(tagi)+str(j)) \
			  and not self.ishimself(tagi, j, tagi, tagj) \
		    	  and self.istwinlist(self.posList[str(tagi)+str(j)], self.posList[str(tagi)+str(tagj)]):
				return True
		return False

	'''
	this guy has a twin brother in the same column
	'''
	def exist_twins_in_col(self, tagi, tagj):

		for i in range(self.row):
			if self.posList.has_key(str(i)+str(tagj)) \
			  and not self.ishimself(i, tagj, tagi, tagj) \
			  and self.istwinlist(self.posList[str(i)+str(tagj)], self.posList[str(tagi)+str(tagj)]):
				return True
		return False
	
	'''
	cut impossible values,make possible lists slim
	in_ could be "row" or "col"
	'''
	def slim_pos_list(self, tagi, tagj, in_):

		if in_ == "row":
			'''check row'''
			for j in range(self.col):
				if self.posList.has_key(str(tagi)+str(j)) \
				  and not self.ishimself(tagi, j, tagi, tagj):
					
					ind_c = []
					
					for x in range(len(self.posList[str(tagi)+str(tagj)])):
						ind = self.exist_in(self.posList[str(tagi)+str(tagj)][x], \
						  self.posList[str(tagi)+str(j)])
						if ind > -1:
							ind_c.append(self.posList[str(tagi)+str(j)][ind])

					if len(ind_c) > 0 and not self.istwinlist(self.posList[str(tagi)+str(j)], \
						  self.posList[str(tagi)+str(tagj)]):
						  	
							for k in ind_c:
								try:
									ind = self.posList[str(tagi)+str(j)].index(k)
									self.posList[str(tagi)+str(j)].pop(ind)
								except IndexError:
									print "IndexError in slim_pos_list::check row:k=",k

		if in_ == "col":
			'''check col'''
			for i in range(self.row):
				if self.posList.has_key(str(i)+str(tagj)) \
				  and not self.ishimself(i, tagj, tagi, tagj):
					ind_c = []
					for x in range(len(self.posList[str(tagi)+str(tagj)])):
						ind = self.exist_in(self.posList[str(tagi)+str(tagj)][x], \
						  self.posList[str(i)+str(tagj)])
						if ind > -1:
							ind_c.append(self.posList[str(i)+str(tagj)][ind])

					if len(ind_c) > 0 and not self.istwinlist(self.posList[str(i)+str(tagj)], \
						  self.posList[str(tagi)+str(tagj)]):
							for k in ind_c:
								try:
									ind = self.posList[str(i)+str(tagj)].index(k)
									self.posList[str(i)+str(tagj)].pop(ind)
								except IndexError:
									print "IndexError in slim_pos_list::check col:k=",k
		self.print_pos_list()
		self.print_newmatrix()


	'''
	try to solute original matrix
	'''
	def solute(self):

		self.get_possible_list()
		'''	
		for i in range(self.row):
			for j in range(self.col):
				:if self.posList.has_key(str(i)+str(j)):
					print str(i)+str(j),':',self.posList[str(i)+str(j)]
		'''
		self.print_pos_list()
		while(True):
			
			for i in range(self.row):
				for j in range(self.col):
					if self.newMatrix[i][j] == 0 \
						and self.posList.has_key(str(i)+str(j)):
					
						if not len(self.posList[str(i)+str(j)]):
							del self.posList[str(i)+str(j)]
							continue	
						
						'''
						if exist uniq value in a 3x3 cell,the value is correct one
						'''
						uniq_val = self.hasuniqval(i, j)
						if uniq_val:
							print "uniq_val =",uniq_val,(i,j)
							self.newMatrix[i][j] = uniq_val
							self.clean_rub(i, j)
							self.print_newmatrix()
							break
						
						'''
						if exist only ONE possible value,that's it,of course
						'''
						if self.posList.has_key(str(i)+str(j)) \
						  and len(self.posList[str(i)+str(j)]) == 1:
							print 'len=1',(i,j)
							print self.posList[str(i)+str(j)]
							self.newMatrix[i][j] = self.posList[str(i)+str(j)][0]
							self.clean_rub(i, j)
							self.print_newmatrix()
							break
						
						'''
						if exist 2-value twin possible lists in the same row or column,these 2
						values are impossible for other empty celles in same row or column
						'''
						if self.posList.has_key(str(i)+str(j)) \
						  and len(self.posList[str(i)+str(j)]) == 2:
							print 'len=2',(i,j)
							print self.posList[str(i)+str(j)]
							if self.exist_twins_in_row(i, j):
								self.slim_pos_list(i, j, "row")	
							if self.exist_twins_in_col(i, j):
								self.slim_pos_list(i, j, "col")
							continue
													
						'''
						if exist triangle model,the uniq value in a triangle model is wanted
						'''
						if self.posList.has_key(str(i)+str(j)) \
						  and len(self.posList[str(i)+str(j)]) == 3:
							print 'len=3',(i,j)
							print self.posList[str(i)+str(j)]
							corner_value = self.istriangle(i, j)
							if corner_value:
								self.newMatrix[i][j] = corner_value
								self.clean_rub(i, j)
								self.print_newmatrix()
							continue	
						
						'''
						if exist trangle model,but possible list of corner cell has 4 or more value,
						values in possible list of right angle side are impossible for corner cell.
						'''
						if self.posList.has_key(str(i)+str(j)) \
						  and len(self.posList[str(i)+str(j)]) > 3:
							print 'len>3',(i,j)
							print self.posList[str(i)+str(j)]
							if self.slim_big_triangle(i, j):
								print "is big triangle"
								self.print_newmatrix()
							continue

			if self.each_pos_list_empty():
				break
			

if __name__ == "__main__":

	print 
	print "                           Sudople                             "
	print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
	print "1.Sudo matrix should be 9x9 matrix"
	print "2.Sudo matrix splited by ','"
	print "3.Use 0 replace empty cell"
	print "4.End with '***'"
	print "5.Enjoy it!!"
	print
	print "Sudoku matrix:"

	matrix = []
	row = 0
	col = 0

	while(True):

		inp = raw_input()
		if inp == '***': break
		
		'''process input data'''
		inp = inp.split(',')
		intinp = []
		for x in inp:
			intinp.append(int(x))
		inp = intinp

		'''initialize matrix'''
		matrix.append([])
		row += 1
		
		matrix[row-1].extend(inp)
		col = len(inp)

	if matrix:

		sudople = sudople(matrix, row, col)

		print "row: %d" % row
		print "col: %d" % col
		print "Original Sudo Matrix"
		print "----------------------------------------"
		sudople.print_orimatrix()
		print "----------------------------------------"
		sudople.solute()
		print "Solution"
		print "----------------------------------------"
		#sudople.print_newmatrix()
		print "----------------------------------------"

