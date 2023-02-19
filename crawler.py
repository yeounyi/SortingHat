from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import re 
from tqdm import tqdm
tqdm.pandas()

# Each character's house 
house_dict = {'Harry':'Gryffindor','Ron':'Gryffindor','Hermione':'Gryffindor',\
             'Hagrid':'Gryffindor','Dumbledore':'Gryffindor','McGonagall':'Gryffindor',\
             'Riddle':'Slytherin','Draco':'Slytherin','Lockhart':'Ravenclaw',\
             'Snape':'Ravenclaw', 'Neville':'Gryffindor','Quirrell':'Ravenclaw',\
             'Oliver':'Gryffindor','Voldemort':'Slytherin', 'Myrtle':'Ravenclaw',\
             'Crouch':'Ravenclaw', 'Lucius':'Slytherin', 'Bellatrix':'Slytherin',\
             'Flitwick':'Ravenclaw','Ollivander':'Ravenclaw', 'Crabbe':'Slytherin',\
             'Marcus':'Slytherin', 'Umbridge':'Slytherin'}


if __name__ == "__main__":

	with open('urls.txt') as f:
	    urls = [url.replace('\n','') for url in f.readlines()]

	df = pd.DataFrame(columns=['speaker','line'])
	count = 0

	for url in urls:
	    with urllib.request.urlopen(url) as url:
	        doc = url.read()
	        soup = BeautifulSoup(doc, "html.parser")

	        paragraphs = soup.find_all("p") + soup.find_all("dd")  
	        list_of_paragraphs = soup.find_all("dl")
	        for p in list_of_paragraphs:
	            paragraphs.extend(p.find_all("dd"))

	        for paragraph in tqdm(paragraphs):
	            paragraph = str(paragraph)
	            speaker = re.findall('(?<=<b>)[a-zA-Z ]+(?=</b>:)', paragraph)
	            if speaker:
	                line = re.sub('(\[.+?\]|</?[ipd]+>|\n)', '', paragraph.split(':')[1]).strip()
	                df.loc[count] = [speaker[0], line]
	                count += 1    


	
    df['house'] = df.speaker.progress_apply(lambda x: house_dict[x] if x in house_dict else '')
    # Gryffindor: 2150, Slytherin: 194, Ravenclaw: 184
    # df[df.house.apply(lambda x: len(x) > 0)].house.value_counts()
    df[df.house.apply(lambda x: len(x) > 0)][['speaker','house','line']].to_csv('harry_potter_lines_w_house.csv', index=False, encoding='utf-8')
