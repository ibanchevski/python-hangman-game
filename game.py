import wx
from random import randint

app = wx.App()

FRAME_W = 800
FRAME_H = 640

# Predefined keys for the keyboard
ALPHABET = [
	'A', 'B', 'C', 'D', 'E', 'F', 'G',
	'H', 'I', 'J', 'K', 'L', 'M', 'N',
	'O', 'P', 'Q', 'R', 'S', 'T', 'U',
	'V', 'W', 'X', 'Y', 'Z'
]

# Get all words from words.txt
with open('words.txt') as f:
	WORDS = f.read()

# Sanitze the input from the file e.g remove all tabs, spaces, commas
# and replace them with ":" so they can be splitted and array of words can be created
WORDS = WORDS.replace('\n', ':').replace(' ', ':').replace('\t', ':').replace(',', ':').split(':')
WORDS = [word.upper() for word in WORDS if word != '']

# The main window
main_frame = wx.Frame(None,
					  title="Hangman",
					  size=wx.Size(FRAME_W, FRAME_H),
					  style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
disabled_btns = []

def start_game():
	global hidden_word
	global picked_word
	global TRIES
	global DISPLAYED_WORD
	TRIES = 6

	# Pick word at random and hide its letters
	picked_word = WORDS[randint(1, len(WORDS) - 1)]
	hidden_word = list(picked_word)
	for i in range(1, len(hidden_word) - 1):
		hidden_word[i] = '_'
	hidden_word = "".join(hidden_word)

	# Display the hidden word
	display_word(hidden_word)

	for btn in disabled_btns:
		btn.Enable()
		btn.SetValue(False)

#position_x = (main_frame.Size[0] - (len(word) * 17)) / 2
#DISPLAYED_WORD = wx.StaticText(main_frame, wx.ID_ANY, "", wx.Point(position_x, 300), wx.Size(150, 100))
DISPLAYED_WORD = wx.StaticText(parent=main_frame, id=wx.ID_ANY, label="", size=wx.Size(150, 100))
DISPLAYED_WORD.SetFont(wx.Font(24, wx.DECORATIVE, wx.NORMAL, wx.NORMAL))

ATTEMPTS_NUM = wx.StaticText(parent=main_frame, id=wx.ID_ANY, label="Attempts left: 6", size=wx.Size(150, 100), pos=wx.Point(20, 360))
ATTEMPTS_NUM .SetFont(wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.NORMAL))
def display_letter_btns():
	letter_w = letter_h = 50
	letter_margin = 10
	
	# Calculate x offset based on frame width, letters width and letter margin
	# so that the letters keypad is horizontally centered in the frame
	x_offset = round((main_frame.Size[0] - 13 * (letter_w + letter_margin)) / 2)
	y_offset = 400 
	for index,letter in enumerate(ALPHABET):
		pos_x = x_offset + (letter_w  + letter_margin) * index
		pos_y = y_offset + letter_h
		if index >= 13:
			index -= 13
			pos_x = x_offset + (letter_w + letter_margin) * index
			pos_y = pos_y + letter_h + letter_margin
		wx.ToggleButton(main_frame,
						id=wx.ID_ANY,
						label=letter,
						pos=wx.Point(pos_x, pos_y),
						size=wx.Size(letter_w, letter_h)).Bind(wx.EVT_TOGGLEBUTTON, guess_word)

def display_word(word):
	global DISPLAYED_WORD
	position_x = round((main_frame.Size[0] - (len(word) * 17)) / 2)
	DISPLAYED_WORD.SetPosition(wx.Point(position_x, 200))
	DISPLAYED_WORD.SetLabel(word)

def guess_word(evt):
	global hidden_word
	global TRIES
	global ATTEMPTS_NUM
	letter = evt.GetEventObject().Label
	indices = [pos for pos,char in enumerate(picked_word) if char == letter] 

	if len(indices) == 0:	
		evt.GetEventObject().SetValue(False)
		TRIES = TRIES - 1
		ATTEMPTS_NUM.SetLabel("Attempts left: " + str(TRIES))
		if TRIES == 0:
			continueGame = wx.GenericMessageDialog(main_frame, "You dont have more tries! Start again?", "Game Over", wx.YES_NO).ShowModal()
			if continueGame == wx.ID_NO:
				exit()
			else:
				ATTEMPTS_NUM.SetLabel("Attempts left: 6")	
				start_game()
				return
	else:
		evt.GetEventObject().Disable()
		disabled_btns.append(evt.GetEventObject())
	w = list(hidden_word)
	for i in indices:
		w[i] = letter

	
	hidden_word = "".join(w)
	display_word(hidden_word)
	if hidden_word == picked_word:
		start_over = wx.GenericMessageDialog(main_frame, "Congratulations, you win! Start over?", "Win", wx.YES_NO).ShowModal()
		if start_over == wx.ID_NO:
			exit()
		else:
			ATTEMPTS_NUM.SetLabel("Attempts left: 6")	
			start_game()

# Display the keyboard
display_letter_btns()

start_game()

main_frame.Show()
app.MainLoop()
