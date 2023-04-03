'''
For this assignment, we are using a page from the Legend of Zelda wiki that lists the top runs in each speedrun category for every Legend of Zelda game on Speedrun.com. I originally wanted to use the direct HTML of the page, but found that Ctrl+A copy-pasting the text left it in a format that was easier to work with.
Original webpage: https://zelda.fandom.com/wiki/Speedrun_Records
'''

#import regex
import re

with open('zelda_speedruns.txt', 'r', encoding='utf8' ) as rf:
	text = rf.read()

#unfortunately, have to remove milliseconds from the speedrun times for Excel calculations later
text = re.sub("\d{1,3}ms", "", text)

#save the text as a list of its rows
text_rows = text.split("\n")

'''
we will iterate through the text row by row,
and use the expressions below to identify the data we need.
explanations for each regex below.
'''

'''
Rows which contain a speedrun category typically look like this:
Speedrun category, Runner name, Time, Data
ex. "Any%	chromataclysm	15m 58s 417ms	September 30, 2022"
This regex will also capture the table column rows, so we need to check that later.
'''
one_runner_category = re.compile(r"(.+)\t(.+)\t(.+)\t(.+)")

'''
Some categories contain two runners working together. In the raw text, there is a newline between the runners' names.
ex. "Any% (Multiplayer)	Okaito
RedFrost	25m 50s	July 20, 2021"
These "rows" require a different approach to capture and compile.
We can capture both rows with ^([^\t]+)\t([^\t]+)\n([^\t]+)\t([^\t]+)\t([^\t]+\d{4}),
or just use the first part, ^([^\t]+)\t([^\t]+)\n, to capture the first line. Once we have the first line, we can combine it with text_rows[i+1] and then compile into a string.
'''
#two_runner_category = re.compile(r"^([^\t]+)\t([^\t]+)\n([^\t]+)\t([^\t]+)\t([^\t]+\d{4})")
two_runner_category = re.compile(r"^([^\t]+)\t([^\t]+)$")

'''
In the raw text, first the game is listed, then a table of speedrun categories for that game. Each table begins with "Category\tRunner\tTime\tDate", i.e. the table's column names. This means if the current row is the column names, then the previous row is the title of the game.
'''
table_column_names = re.compile(r"Category\tRunner\tTime\tDate")

'''
This regex captures the line before the table column names, which is the title of the game.
(Unused)
'''
game_and_column_names = re.compile(r"(.+)\nCategory\tRunner\tTime\tDate")


#create a list to save output data in
output_data = []
#need to keep track of what game each category is for
current_game = "a"

#iterate through each row
for i in range(0, len(text_rows)):
	#the row corresponding to this index
	row = text_rows[i]
	
	#check if this is a one-runner category entry and store the match
	one_runner_match = one_runner_category.match(row)
	#check if this is a column-name row
	table_column_match = table_column_names.match(row)
	#check if two runner category
	two_runner_match = two_runner_category.match(row)
	
	if table_column_match:
		#if this is a column name row, then that means we are looking at a new game.
		#set current game to previous row, which contains the title.
		current_game = text_rows[i-1]
		print("found a table column row! current game is now " + current_game)
	#when checking if the row is a one-runner category, we also have to check that the row is not a table-column row.
	elif one_runner_match and not table_column_match:
		#create a tab-separated string and append it to the output_data list
		output_string = '\t'.join(one_runner_match.group(1, 2, 3, 4))
		output_data.append(current_game + "\t" + output_string)
	elif two_runner_match:
		#for two-runner categories, the match only finds the first row.
		#combine the match with the next row to create the full entry.
		first_string = '\t'.join(two_runner_match.group(1, 2))
		second_string = text_rows[i+1]
		output_string = first_string + " with " + second_string
		output_data.append(current_game + "\t" + output_string)
		print("found a two-runner category!")


#now we can write our output data to a .tsv file.
with open("zelda_speedruns.tsv", "w", encoding="utf8") as wf:
	wf.write("\n".join(output_data))


