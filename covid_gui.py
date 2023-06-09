# file : covid_gui.py
# Authors : dsanmukh, dishantv, jgala, rkacheri, smahapat
# Purpose : this file uses tkinter to create the GUI for the project and its functionalities

# imported by : covid_main.py
# imports : myths_facts.py, keywords.py, vaccine.py

import textwrap
import tkinter as tk
import tkmacosx as tkmac

from functools import partial
from PIL import Image

import keywords
import myths_facts
import stats_visualization
import vaccine


# function to create a tkinter label and place it on canvas
def create_label(screen, canvas, text, text_var, x, y, font_size, bg_color, fg_color, is_underline):
    label = tk.Label(screen, text=text)
    if is_underline:
        label.config(font=('helvetica', font_size, 'bold', 'underline'), bg=bg_color, fg=fg_color)
    else:
        label.config(font=('helvetica', font_size, 'bold'), bg=bg_color, fg=fg_color)

    if text_var is None:
        pass
    else:
        label.config(textvariable=text_var)
    canvas.create_window(x, y, window=label)


# function to create a tkinter entry box and place it on canvas
def create_entry(screen, canvas, width, x, y, font_size, bg_color, fg_color, is_text, tk_var):
    if is_text and tk_var is not None:
        entry = tk.Entry(screen, width=width, justify='center', font=('helvetica', font_size, 'bold'), bg=bg_color,
                         fg=fg_color, textvariable=tk_var, state='readonly')
    else:
        entry = tk.Entry(screen, width=width, font=('helvetica', font_size, 'bold'), bg=bg_color, fg=fg_color)
    canvas.create_window(x, y, window=entry)


# function to create a tkinter button and place it on canvas
def create_button(screen, canvas, text, width, height, x, y, font_size, bg_color, fg_color, fn, *argv):
    if fn is None:
        button = tkmac.Button(screen, text=text, font=('helvetica', font_size, 'bold'), bg=bg_color, fg=fg_color,
                              width=width, height=height)

    else:
        button = tkmac.Button(screen, text=text, command=partial(fn, *argv), font=('helvetica', font_size, 'bold'),
                              bg=bg_color,
                              fg=fg_color,
                              width=width, height=height)
    canvas.create_window(x, y, window=button)


# function to fetch myths and facts on COVID vaccine
def myths_and_facts(screen):
    global maf_idx
    maf_screen = tk.Toplevel(screen)
    maf_screen.title("Myth Busters - Myths and Facts")
    maf_screen_canvas = tk.Canvas(maf_screen, width=1200, height=600, bg="RoyalBlue4")
    maf_screen_canvas.pack()

    create_label(maf_screen, maf_screen_canvas, 'Myth Busters', None, 600, 40, 30, 'RoyalBlue4', 'white', True)

    x = 600
    y = 200

    myths, facts, ind = myths_facts.get_maf_data()

    myth = tk.StringVar()
    fact = tk.StringVar()
    myth.set(f'Myth: {textwrap.fill(myths[maf_idx], 70)}')
    fact.set(f'Fact: {textwrap.fill(facts[maf_idx], 70)}')

    # load next myth and fact
    def next_myth_and_fact():
        global maf_idx
        maf_idx = maf_idx + 1
        if maf_idx == len(myths):
            maf_idx = 0  # restart once over
        myth.set(f'Myth: {textwrap.fill(myths[maf_idx], 70)}')
        fact.set(f'Fact: {textwrap.fill(facts[maf_idx], 70)}')

    create_button(maf_screen, maf_screen_canvas, 'Next', 250, 50, 600, 450, 20, 'SkyBlue4', 'white',
                  next_myth_and_fact)

    create_label(maf_screen, maf_screen_canvas, f'', myth, x, y, 20, 'RoyalBlue4', 'white', False)
    create_label(maf_screen, maf_screen_canvas, f'', fact, x, y + 150, 20, 'RoyalBlue4', 'white', False)


# function to create a word cloud using Twitter, Reddit and YouTube data
def wordcloud():
    keywords.getData()


# function to check availability of vaccine in a US state
def vaccine_address(screen):
    global vaccine_loc_idx
    global locations
    vaccine_addr_screen = tk.Toplevel(screen)
    vaccine_addr_screen.title("Vaccine Tracker")
    vaccine_addr_screen_canvas = tk.Canvas(vaccine_addr_screen, width=1200, height=600, bg="RoyalBlue4")
    vaccine_addr_screen_canvas.pack()

    create_label(vaccine_addr_screen, vaccine_addr_screen_canvas, 'Vaccine Tracker', None, 600, 40, 30, 'RoyalBlue4',
                 'white', True)
    #
    x = 600
    y = 350

    state = tk.StringVar()
    addr = tk.StringVar()

    def get_addresses():
        global locations
        locations = vaccine.get_vaccination_slots(state.get())
        if len(locations) == 0:
            addr.set('Oops! No Data Found. Please check the State abbreviation')

        addr.set(f'''{textwrap.fill(locations[vaccine_loc_idx], 70)}
{textwrap.fill(locations[vaccine_loc_idx + 1], 70)}
{textwrap.fill(locations[vaccine_loc_idx + 2], 70)}
{textwrap.fill(locations[vaccine_loc_idx + 3], 70)}
{textwrap.fill(locations[vaccine_loc_idx + 4], 70)}''')

    create_label(vaccine_addr_screen, vaccine_addr_screen_canvas, 'State', None, 500, 100, 20, 'RoyalBlue4',
                 'white', False)
    state_entry = tk.Entry(vaccine_addr_screen, width=10, justify='center', font=('helvetica', 20, 'bold'),
                           bg='SkyBlue4',
                           fg='white', textvariable=state)
    vaccine_addr_screen_canvas.create_window(700, 100, window=state_entry)
    create_label(vaccine_addr_screen, vaccine_addr_screen_canvas, '(use State abbreviations for eg. PA)', None, 900,
                 100, 15, 'RoyalBlue4',
                 'white', False)
    create_button(vaccine_addr_screen, vaccine_addr_screen_canvas, 'Get Locations', 250, 50, 600, 250, 20, 'SkyBlue4',
                  'white',
                  get_addresses)

    def next_vaccine_address():
        global vaccine_loc_idx
        vaccine_loc_idx = vaccine_loc_idx + 5
        if vaccine_loc_idx == len(locations) - 6:
            vaccine_loc_idx = 0
        addr.set(f'''{textwrap.fill(locations[vaccine_loc_idx], 70)}
{textwrap.fill(locations[vaccine_loc_idx + 1], 70)}
{textwrap.fill(locations[vaccine_loc_idx + 2], 70)}
{textwrap.fill(locations[vaccine_loc_idx + 3], 70)}
{textwrap.fill(locations[vaccine_loc_idx + 4], 70)}''')

    create_button(vaccine_addr_screen, vaccine_addr_screen_canvas, 'Next', 250, 50, 600, 450, 20, 'SkyBlue4', 'white',
                  next_vaccine_address)

    create_label(vaccine_addr_screen, vaccine_addr_screen_canvas, f'', addr, x, y, 20, 'RoyalBlue4', 'white', False)


# function to create data visualizations using COVID19 data
def visualize_stats(screen):
    stats_visualization.main()
    stats_screen = tk.Toplevel(screen)
    stats_screen.title("Vaccine Tracker")
    stats_screen_canvas = tk.Canvas(stats_screen, width=1200, height=600, bg="RoyalBlue4")
    stats_screen_canvas.pack()

    create_label(stats_screen, stats_screen_canvas, 'Data Visualization', None, 600, 40, 30, 'RoyalBlue4',
                 'white', True)

    def show_image(*args):
        for i in args:
            im = Image.open(f'img{i}.png')
            im.show()

    create_button(stats_screen, stats_screen_canvas, 'Daily Vaccinations\nin the USA', 200, 150, 240, 200, 20,
                  'SkyBlue4', 'white',
                  show_image, 1)
    create_button(stats_screen, stats_screen_canvas, 'Daily Vaccinations\nby Country\nComparison\n(New vs Old)', 200,
                  150, 480, 200, 18, 'SkyBlue4', 'white',
                  show_image, 2, 3)
    create_button(stats_screen, stats_screen_canvas, 'People Vaccinated\nper Hundred', 200, 150, 720, 200, 20,
                  'SkyBlue4', 'white',
                  show_image, 4)
    create_button(stats_screen, stats_screen_canvas, 'People Fully\nVaccinated\nper Hundred', 200, 150, 960, 200, 20,
                  'SkyBlue4', 'white',
                  show_image, 5)
    create_button(stats_screen, stats_screen_canvas, 'Most Used Vaccine\nin the USA', 200, 150, 300, 400, 20,
                  'SkyBlue4', 'white',
                  show_image, 6)
    create_button(stats_screen, stats_screen_canvas, 'Most Used Vaccine\nin the World', 200, 150, 600, 400, 20,
                  'SkyBlue4', 'white',
                  show_image, 7)
    create_button(stats_screen, stats_screen_canvas, 'Vaccine\nComparison\nin Europe', 200, 150, 900, 400, 20,
                  'SkyBlue4', 'white',
                  show_image, 8)


def main():
    main_screen = tk.Tk()
    main_screen.title("COVID Vaccination Analysis")

    main_screen_canvas = tk.Canvas(main_screen, width=1200, height=800, bg="RoyalBlue4")
    main_screen_canvas.pack()

    create_label(main_screen, main_screen_canvas, 'Project Big Jab', None, 600, 40, 30, 'RoyalBlue4', 'white', True)

    create_button(main_screen, main_screen_canvas, 'Myths & Facts', 200, 100, 150, 300, 20, 'SkyBlue4', 'white',
                  myths_and_facts, main_screen)
    create_button(main_screen, main_screen_canvas, 'Stats', 200, 100, 450, 300, 20, 'SkyBlue4', 'white',
                  visualize_stats, main_screen)
    create_button(main_screen, main_screen_canvas, 'Social Media\nWordCloud', 200, 100, 750, 300, 20, 'SkyBlue4',
                  'white',
                  wordcloud)
    create_button(main_screen, main_screen_canvas, 'Vaccine Tracker', 200, 100, 1050, 300, 20, 'SkyBlue4', 'white',
                  vaccine_address, main_screen)

    main_screen.mainloop()


maf_idx = 0
vaccine_loc_idx = 0
locations = []
if __name__ == '__main__':
    main()
