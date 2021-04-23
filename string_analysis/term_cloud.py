from typing import List, Dict
from wordcloud import WordCloud, STOPWORDS,ImageColorGenerator,get_single_color_func
import re
from os import path, makedirs
import matplotlib.pyplot as plt

class Color:
    def __init__(self, color:str):
        if not re.match(r"^#[aAbBcCdDeEfF\d]{6}$",color):
            raise ValueError(f"The color {color} does not match the hex format (ie #FFFFFF)")
        self.hex = color

def generate(term_files:List[str], colors:Dict[int,str], out_dir:str):
    for term_file in term_files:
        try:
            terms = get_terms_from_file(term_file)
            frequencies = get_frequencies(terms)
            color = get_color_for_group(term_file, colors)
            wordcloud = create_wordcloud(color,frequencies)
            out_filepath = generate_outpath(out_dir, term_file)
            create_fig(wordcloud, out_filepath, color)
        except ValueError as e:
            print(str(e))
            print("skipping this one")
            continue


def generate_outpath(out_dir:str, term_file:str):
    out_name = re.sub(r'.txt$',"_cloud.png",path.basename(term_file))
    if not path.exists(out_dir):
        makedirs(out_dir)
    return path.join(out_dir,out_name)

def create_fig(wordcloud:WordCloud, out_filepath:str, color:Color):

    fig = plt.figure(figsize=(2,2),dpi=600)

    #create a patch on the figure to act as the border 
    fig.patches.extend([plt.Rectangle((0,0),1,1,color=color.hex,fill=True,transform=fig.transFigure, figure = fig,alpha = 0.6,zorder=1)])
    #set up the border
    axis = fig.add_subplot(111)
    #remove the axis
    axis.set_axis_off()
    axis.set_zorder(2)
    # create the image
    axis.imshow(wordcloud,interpolation='bilinear')

    #set position of the axis within the figure 
    border = 0.01
    axis.set_position([border,border,1-border*2,1-border*2]) #bottom corner x,y width,height

    # border = plt.Axes(fig,[0,1,1,1],facecolor=group_color)

    plt.savefig(out_filepath,dpi=300)
    plt.close()

def create_wordcloud(color:Color, frequencies:dict) -> WordCloud:
    color_func = get_single_color_func(color.hex)
    return WordCloud(
        background_color="white",
        max_words=15,
        color_func=color_func,
        min_font_size=30,
        width=1200,
        height=1200).fit_words(frequencies)

def get_color_for_group(filename:str, colors:Dict[int,str]) -> Color:

    if not (match := re.search(r'group_(\d+).txt$',filename)):
        raise ValueError(f"Could not identify group for {filename}")

    group_color = colors.get(int(match.group(1)))
    if not group_color:
        raise ValueError(f"There is no color assignable to group {match.group(1)}")

    return Color(group_color)

def get_terms_from_file(filename:str) -> List[str]:
    with open(filename, "r") as f:
        return [l.strip() for l in f.readlines()]

def get_frequencies(terms:list) -> dict:

    frequencies = {}

    for term in terms:
        # skip long terms
        if len(term) >35 :
            continue
        frequencies[term] = frequencies.get(term,0) + 1

    if not frequencies:
        raise ValueError("Cannot create word cloud as all terms are too long")

    return frequencies