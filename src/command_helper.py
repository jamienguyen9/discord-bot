import random
import urllib.parse, urllib.request, re

carl_links = [
    "https://i1.sndcdn.com/artworks-000650881924-x9k0sw-t500x500.jpg",
    "https://media1.tenor.com/images/0810e079c392ba3d483ba81f4edeef97/tenor.gif?itemid=17987376",
    "https://media.tenor.com/images/2bfbf4df86550fc5d3ed4b6e74ac7e75/tenor.gif",
    "https://66.media.tumblr.com/f5e7ff72672d00b61f6ee864a5c00c18/tumblr_ppeqbhi97d1wynsudo1_400.png",
    "https://media0.giphy.com/media/fZaAP3pmkgPio/giphy.gif"
]

def get_carl():
    index = random.randint(0, len(carl_links) - 1)
    return carl_links[index]

def get_rolls(arg):
    i = 0
    j = 0
    args = []
    
    if 'd' not in arg:
        return False

    for c in arg:
        if c == 'd':
            args.append(int(arg[i:j]))
            i = j + 1
            j = i
        else:
            j += 1

    if j == i:
        return False

    else:
        args.append(int(arg[i:j]))

    rolls = []
    for c2 in range(args[0]):
        rolls.append(random.randint(1, args[-1]))

    return rolls

def verify_role(role, roles):
    for i in roles:
        if i.name == role:
            return True
    return False

def get_link(link):
    query_str = urllib.parse.urlencode({
        'search_query': link
    })
    content = urllib.request.urlopen(
        'http://www.youtube.com/results?' + query_str
    )
    res = re.findall(r"watch\?v=(\S{11})", content.read().decode())
    return str('http://www.youtube.com/watch?v=' + res[0])