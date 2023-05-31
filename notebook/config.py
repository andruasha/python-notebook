families = tuple(['Arial', 'Arabic Transparent', 'Modern'])

sizes = tuple(range(8, 74, 2))

weights = tuple(['normal', 'bold'])

slants = tuple(['roman', 'italic'])

underlines = tuple(['0', '1'])

text_colors = tuple(['Черный', 'Белый', 'Красный'])

back_colors = tuple(['Белый', 'Черный', 'Красный'])

color_codes = {
    'Черный': '#000000',
    'Белый': '#ffffff',
    'Красный': '#ff0000'
}

def_text_color = color_codes.get(text_colors[0])
def_back_color = color_codes.get(back_colors[0])
default_tag = f'{families[0]}_{sizes[0]}_{weights[0]}_{slants[0]}_{underlines[0]}_{def_text_color}_{def_back_color}'
