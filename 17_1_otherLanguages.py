#   import requests and graphing modules
import requests

from plotly import offline

#   initialize the master dictionaries that require lists as values
languages = ['python','JavaScript','Ruby','C','Java','Perl','Haskell','Go']
urls, repoDictsMaster, repoLinksMaster, starsMaster, labelsMaster, \
dataMaster, layoutMaster, figMaster = {}, {}, {}, {}, {}, {}, {}, {}
for lang in languages:
    repoLinksMaster[lang] = []
    starsMaster[lang] = []
    labelsMaster[lang] = []
    figMaster[lang] = []

#   for each language, examine the API response's repositories. Then for
#   each repository take the relevant data we are wanting to plot, as well
#   as the hovertext requirements. Then organize the data per the language
#   it is referring to in the master lists. Each language needs its
#   own layout since we are changing the title each time. Otherwise,
#   we wouldn't need a master layout list. Finally, make a figure for each
#   language
for lang in languages:
    url = f"https://api.github.com/search/repositories?q=language:" \
          f"{lang}&sort=stars "
    urls[lang] = url
    headers = {'Accept': 'application/vnd.github.v3+json'}
    #   pass the relevant URL and header
    #   assign the response object to a variable, in this cas 'r'
    r = requests.get(urls[lang], headers=headers)
    #   store API response in a variable in json format
    repoDict = r.json()
    #   explore information about the repositories
    repoDictsMaster[lang] = repoDict['items']
    #   examine the first repository
    reDi = repoDictsMaster[lang][0]
    print(f"Status Code:\t{r.status_code}")
    print(f"Total Repositories:\t{repoDict['total_count']}")

    for reDi in repoDictsMaster[lang]:
        #   create HTML hyperlink text for the name of the data location
        repoName = reDi['name']
        repoURL = reDi['html_url']
        repoLink = f"<a href='{repoURL}'>{repoName}</a>"
        repoLinksMaster[lang].append(repoLink)
        starsMaster[lang].append(reDi['stargazers_count'])
        owner = reDi['owner']['login']
        description = reDi['description']
        labelsMaster[lang].append(f"{owner}<br />{description}")

    dataMaster[lang] = [{
            'type'     : 'bar',
            'x'        : repoLinksMaster[lang],
            'y'        : starsMaster[lang],
            'hovertext': labelsMaster[lang],
            'marker'   : {
                    'color': 'rgb(60,100,150)',
                    'line' : {'width': 1.5,
                              'color': 'rgb(25,25,25)'},
            },
            'opacity'  : 0.6,
    }]

    layoutMaster[lang] = {
            'title'    : f"Most-Starred {lang} Projects on Github",
            'titlefont': {'size': 28},
            'xaxis'    : {
                    'title'    : 'Repository',
                    'titlefont': {'size': 24},
                    'tickfont' : {'size': 14},
            },
            'yaxis'    : {
                    'title'    : 'Stars',
                    'titlefont': {'size': 24},
                    'tickfont' : {'size': 14},
            },
    }

    figMaster[lang] = {'data': dataMaster[lang], 'layout': layoutMaster[
        lang]}

#   this step can technically be in the for loop above, but I wanted the
#   code to make sure every language's URL works prior to beginning the
#   plotting process. Once all the figures are made and assigned to their
#   respective language as a key/value ite, in the figure master dictionary,
#   we plot the figures.
for lang, fig in figMaster.items():
    offline.plot(fig, filename=f"{lang}ReposVisual.html")
