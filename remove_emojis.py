import re

def remove_emojis():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Known HTML entity emojis
    html = html.replace('&#127891;', '') # Student login hat
    html = html.replace('&#128188;', '') # Project coordinator briefcase
    html = html.replace('&#127963;', '') # Director pillar
    html = html.replace('&#9733;', '')   # Team leader star
    html = html.replace('&#128640;', '') # Rocket
    html = html.replace('&#128200;', '') # Chart increasing
    html = html.replace('&#128172;', '') # Speech bubble
    html = html.replace('&#128221;', '') # Memo
    html = html.replace('&#128101;', '') # People
    html = html.replace('&#127919;', '') # Direct hit (target)

    # Unicode emoji ranges
    # Matches emojis and miscellaneous symbols
    emoji_pattern = re.compile(
        u"(\ud83d[\ude00-\ude4f])|"  # emoticons
        u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
        u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
        u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
        u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
        "+", flags=re.UNICODE)
    
    # Python 3 handles unicode differently, let's just use a wide range regex
    wide_emoji_pattern = re.compile(r'[\U00010000-\U0010ffff\u2600-\u27BF]', flags=re.UNICODE)
    html = wide_emoji_pattern.sub('', html)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Emojis removed")

if __name__ == '__main__':
    remove_emojis()
