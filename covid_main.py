# file : covid_main.py
# Authors : dsanmukh, dishantv, jgala, rkacheri, smahapat
# Purpose : main module, supports CLI for the project

# imports : covid_gui.py, keywords.py, myths_facts.py, stats_visualization.py, vaccine.py

import os
import sys
from sys import platform

from PIL import Image

import covid_gui
import keywords
import myths_facts
import stats_visualization
import vaccine


def clear_console():
    if sys.platform == 'darwin':
        os.system('clear')
    else:
        os.system('cls')


def main():
    cli_or_gui = 'Z'
    clear_console()
    while cli_or_gui != 'Q':
        print('---------------------------')
        print('Welcome to Project Big Jab')
        print('---------------------------')

        print('''The purpose of this project is to improve the 
COVID vaccination rate of the world''')

        print('---------------------------')

        print('A to continue with CLI')
        print('B to continue with GUI')
        print('Q to quit the program')

        print('---------------------------')

        cli_or_gui = input('Enter A or B or Q: ')

        if cli_or_gui == 'A':
            cli_option = -1
            while cli_option != '0':
                print('---------------------------')
                print('0 to go BACK')
                print('1 to see the Myths and Facts about COVID Vaccines')
                print('2 to visualize the Stats on COVID Vaccination')
                print('3 to see what\'s trending on Twitter, Youtube and Reddit around COVID Vaccination')
                print('4 to check COVID Vaccine availability in your State')

                cli_option = input('Enter a number: ')

                if cli_option == '0':
                    break

                elif cli_option == '1':
                    myths_facts.main()

                elif cli_option == '2':
                    stats_visualization.main()
                    clear_console()
                    graph_option = -1
                    while graph_option != '0':
                        print('---------------------------')
                        print('Which graph visualization do you want to see?')
                        print('---------------------------')
                        print('0 for BACK')
                        print('1 for Daily Vaccinations in the USA')
                        print('2 for Daily Vaccinations by Country (New vs Old) Comparison')
                        print('3 for People Vaccinated per Hundred')
                        print('4 for People Fully Vaccinated per Hundred')
                        print('5 for Most Used Vaccine in the USA')
                        print('6 for Most Used Vaccine in the World')
                        print('7 for Vaccine Comparison in the Europe')
                        print('---------------------------')

                        graph_option = input('Enter: ')

                        if graph_option == '0':
                            break

                        elif graph_option == '1':
                            im = Image.open('img1.png')
                            im.show()

                        elif graph_option == '2':
                            im = Image.open('img2.png')
                            im.show()
                            im = Image.open('img3.png')
                            im.show()

                        elif graph_option == '3':
                            im = Image.open('img4.png')
                            im.show()

                        elif graph_option == '4':
                            im = Image.open('img5.png')
                            im.show()

                        elif graph_option == '5':
                            im = Image.open('img6.png')
                            im.show()

                        elif graph_option == '6':
                            im = Image.open('img7.png')
                            im.show()

                        elif graph_option == '7':
                            im = Image.open('img8.png')
                            im.show()

                        else:
                            print('Oops! Try again.')

                elif cli_option == '3':
                    keywords.getData()

                elif cli_option == '4':
                    print('---------------------------')
                    state = input('Enter the US State abbreviation you live in (for eg. NY): ')
                    print('---------------------------')
                    locations = vaccine.get_vaccination_slots(state)
                    if len(locations) == 0:
                        print('Oops! No Data Found. Please check the State abbreviation')
                    else:
                        print('---------------------------')
                        print('Vaccines Available Here')
                        print('---------------------------')
                        for loc in locations:
                            print(loc)
                else:
                    print('Oops! Try again.')

        elif cli_or_gui == 'B':
            covid_gui.main()

        elif cli_or_gui == 'Q':
            print('Thank you for visiting, stay vaccinated!')
            break

        else:
            print('Oops! Try again')


if __name__ == '__main__':
    main()
