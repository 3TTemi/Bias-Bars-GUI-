

import tkinter
import biasbarsdata
import biasbarsgui as gui


# Provided constants to load and plot the word frequency data
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

FILENAME = "data/full-data.txt"

VERTICAL_MARGIN = 30
LEFT_MARGIN = 60
RIGHT_MARGIN = 30
LABELS = ["Low Reviews", "Medium Reviews", "High Reviews"]
LABEL_OFFSET = 10
BAR_WIDTH = 75
LINE_WIDTH = 2
TEXT_DX = 2
NUM_VERTICAL_DIVISIONS = 7
TICK_WIDTH = 15

def get_centered_x_coordinate(width, idx):

    sub_width = (width - LEFT_MARGIN - RIGHT_MARGIN) / 3
    if idx == 0:
        return (sub_width / 2) + LEFT_MARGIN
    elif idx == 1:
        return (sub_width + (sub_width / 2)) + LEFT_MARGIN
    else:
        return (sub_width + sub_width + (sub_width / 2)) + LEFT_MARGIN


def draw_fixed_content(canvas):

    canvas.delete('all')           
    width = canvas.winfo_width()   
    height = canvas.winfo_height() 
    canvas.create_rectangle(LEFT_MARGIN, VERTICAL_MARGIN, width - RIGHT_MARGIN, height - VERTICAL_MARGIN, width=LINE_WIDTH)

    text_y = (height - VERTICAL_MARGIN) + LABEL_OFFSET
    canvas.create_text(get_centered_x_coordinate(width, 0), text_y, text = LABELS[0], anchor=tkinter.N)
    canvas.create_text(get_centered_x_coordinate(width, 1), text_y, text = LABELS[1], anchor=tkinter.N)
    canvas.create_text(get_centered_x_coordinate(width, 2), text_y, text = LABELS[2],  anchor=tkinter.N)



def plot_word(canvas, word_data, word):

    draw_fixed_content(canvas)
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    gender_data = word_data[word]
    max_frequency = max(max(gender_data[biasbarsdata.KEY_WOMEN]), max(gender_data[biasbarsdata.KEY_MEN]))


    canvas_height = height - (2 * VERTICAL_MARGIN)

    change_y = max_frequency / NUM_VERTICAL_DIVISIONS

    for i in range(NUM_VERTICAL_DIVISIONS + 1):
        report_text = round(change_y * (i))
        tick_height = height - VERTICAL_MARGIN - ((i/NUM_VERTICAL_DIVISIONS) * canvas_height)
        canvas.create_line(LEFT_MARGIN - (TICK_WIDTH / 2), tick_height, LEFT_MARGIN + (TICK_WIDTH / 2),tick_height, width=LINE_WIDTH)
        canvas.create_text(LEFT_MARGIN - LABEL_OFFSET, tick_height, text = report_text, anchor=tkinter.E)

    for i in range(3):
        wbar = (gender_data[biasbarsdata.KEY_WOMEN][i] / max_frequency) * canvas_height
        mbar = (gender_data[biasbarsdata.KEY_MEN][i] / max_frequency) * canvas_height
        center_x = get_centered_x_coordinate(width, i)
        canvas.create_rectangle(center_x - BAR_WIDTH, height - VERTICAL_MARGIN - 1, center_x, height - VERTICAL_MARGIN - wbar, fill = "#BBBBFF")
        canvas.create_rectangle(center_x, height - VERTICAL_MARGIN - 1, center_x + BAR_WIDTH, height - VERTICAL_MARGIN - mbar, fill = "#FFFFC0")
        if (gender_data[biasbarsdata.KEY_WOMEN][i] != 0):
            canvas.create_text(center_x - BAR_WIDTH + TEXT_DX, height - VERTICAL_MARGIN - wbar, text="W", anchor=tkinter.NW)
        if (gender_data[biasbarsdata.KEY_MEN][i] != 0):
            canvas.create_text(center_x + TEXT_DX, height - VERTICAL_MARGIN - mbar, text="M", anchor=tkinter.NW)




def convert_counts_to_frequencies(word_data):
  
    K = 1000000
    total_words_men = sum([sum(counts[biasbarsdata.KEY_MEN]) for word, counts in word_data.items()])
    total_words_women = sum([sum(counts[biasbarsdata.KEY_WOMEN]) for word, counts in word_data.items()])
    for word in word_data:
        gender_data = word_data[word]
        for i in range(3):
            gender_data[biasbarsdata.KEY_MEN][i] *= K / total_words_men
            gender_data[biasbarsdata.KEY_WOMEN][i] *= K / total_words_women


def main():
    import sys
    args = sys.argv[1:]
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    if len(args) == 2:
        WINDOW_WIDTH = int(args[0])
        WINDOW_HEIGHT = int(args[1])

    word_data = biasbarsdata.read_file(FILENAME)
    convert_counts_to_frequencies(word_data)

    top = tkinter.Tk()
    top.wm_title('Bias Bars')
    canvas = gui.make_gui(top, WINDOW_WIDTH, WINDOW_HEIGHT, word_data, plot_word, biasbarsdata.search_words)

    draw_fixed_content(canvas)

    top.mainloop()


if __name__ == '__main__':
    main()