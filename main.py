# Gets the average base stats of Pokemon by generation

from lxml import html
import requests

last_gen_entries = [0, 151, 251, 386, 493, 649, 721]
gen = 1;
gen_stats = []

LAST_MON = 809
AVG_GEN_STATS = []

page = requests.get(r'https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_base_stats_(Generation_VII-present)')

tree = html.fromstring(page.content)

tr_elems = tree.xpath('//tr')


def average_stats():
	avg_stats = [round(sum(x)/len(gen_stats), 2) for x in zip(*gen_stats)]
	AVG_GEN_STATS.append(avg_stats)
	gen_stats.clear()


for T in tr_elems[2:]:
	dex_num = int(T[0].text_content())

	if (dex_num == LAST_MON) or (gen != 7 and dex_num > last_gen_entries[gen]):
		average_stats()

		if dex_num == LAST_MON:
			break

		gen += 1

	stats = [int(n.text_content()) for n in T[3:-2]]
	# print(T[2].text_content())
	# print(gen)

	gen_stats.append(stats)


for region, stats in zip(['KANTO', 'JOHTO', 'HOENN', 'SINNOH', 'UNOVA', 'KALOS', 'ALOLA'], AVG_GEN_STATS):
	print(region + ": " + str(stats))

print ('Generating HTML')

style = """
<style type="text/css">

ul {
	float: center;
}

body {
	background-color: #D3D3D3
}

ul li {
    display: inline-block;
    zoom: 1;
    *display: inline;
    list-style-type: none;
    vertical-align: middle;
}

.container {
	padding: 1.5em;
}

img {
	display: inline;
	float: left;
	padding-right: 1em;
	vertical-align:middle;
	display: block;
	margin-left: auto;
	margin-right: auto;
}

table {
    font-size: 100%;
    vertical-align:middle;
    width: 100%;
}

.mw-content-ltr {
    direction: ltr;
}

body {
    font: x-small sans-serif;
}

.mw-body {
    color: black;
    line-height: 1.5em;
}

</style>
"""


templatefile = open('template.html', 'r')

if templatefile.mode == 'r':
	template = templatefile.read()
	templatefile.close()

	out = open('out.html','w+')
	out.write(style)
	out.write('<ul>')

	for i, g in enumerate(AVG_GEN_STATS):

		replaced = template
		replaced = replaced.replace('GAME_NAME', 'game_' + str(i) )
		replaced = replaced.replace('TOTAL_STAT', str( round(sum(g),2) ) )

		for n, stat in enumerate(g):
			replaced = replaced.replace('STAT_' + str(n), str(stat) )

		out.write('<li>'+ replaced + '</li>')

	out.write('</ul>')

	out.close()	

print('done!')	