from faker import Faker

from pprint import pprint as print


class Hexaco:
    def __init__(self, seed=None):
        self.gen = Faker()
        if seed:
            Faker.seed(seed)
        self.traits = {
            "honesty_humility": {
                "sincerity": 0,
                "fairness": 0,
                "greed_avoidance": 0,
                "modesty": 0,
            },
            "emotionality": {
                "fearfulness": 0,
                "anxiety": 0,
                "dependence": 0,
                "sentimentality": 0,
            },
            "extraversion": {
                "social_selfesteem": 0,
                "social_boldness": 0,
                "socialability": 0,
                "liveliness": 0,
            },
            "agreeableness": {
                "forgiveness": 0,
                "gentleness": 0,
                "flexibility": 0,
                "patience": 0,
            },
            "conscientiousness": {
                "organization": 0,
                "diligence": 0,
                "perfectionism": 0,
                "prudence": 0,
            },
            "openness_to_experience": {
                "aesthetic_appreciation": 0,
                "inquisitiveness": 0,
                "creativity": 0,
                "unconventionality": 0,
            },
            "interstitial": {"altruism": 0},
        }

    def generate_random_traits(self):
        for section, traits in self.traits.items():
            for name in traits.keys():
                self.traits[section][name] = self.gen.pyfloat(
                    right_digits=3, min_value=0, max_value=1
                )

        print(self.traits)

    def section_score(self, section):
        try:
            return sum(list(self.traits[section].values())) / len(
                self.traits[section].values()
            )
        except Exception:
            return 0


h = Hexaco()

h.generate_random_traits()
print(h.section_score("agreeableness"))

"""
Honesty-Humility Domain
The Sincerity scale assesses a tendency to be genuine in interpersonal relations. Low scorers will flatter others or pretend to like them in order to obtain favors, whereas high scorers are unwilling to manipulate others.
The Fairness scale assesses a tendency to avoid fraud and corruption. Low scorers are willing to gain by cheating or stealing, whereas high scorers are unwilling to take advantage of other individuals or of society at large.
The Greed Avoidance scale assesses a tendency to be uninterested in possessing lavish wealth, luxury goods, and signs of high social status. Low scorers want to enjoy and to display wealth and privilege, whereas high scorers are not especially motivated by monetary or social-status considerations.
The Modesty scale assesses a tendency to be modest and unassuming. Low scorers consider themselves as superior and as entitled to privileges that others do not have, whereas high scorers view themselves as ordinary people without any claim to special treatment.

Emotionality Domain
The Fearfulness scale assesses a tendency to experience fear. Low scorers feel little fear of injury and are relatively tough, brave, and insensitive to physical pain, whereas high scorers are strongly inclined to avoid physical harm.
The Anxiety scale assesses a tendency to worry in a variety of contexts. Low scorers feel little stress in response to difficulties, whereas high scorers tend to become preoccupied even by relatively minor problems.
The Dependence scale assesses one's need for emotional support from others. Low scorers feel self-assured and able to deal with problems without any help or advice, whereas high scorers want to share their difficulties with those who will provide encouragement and comfort.
The Sentimentality scale assesses a tendency to feel strong emotional bonds with others. Low scorers feel little emotion when saying good-bye or in reaction to the concerns of others, whereas high scorers feel strong emotional attachments and an empathic sensitivity to the feelings of others.

Extraversion Domain
The Social Self-Esteem scale assesses a tendency to have positive self-regard, particularly in social contexts. High scorers are generally satisfied with themselves and consider themselves to have likable qualities, whereas low scorers tend to have a sense of personal worthlessness and to see themselves as unpopular.
The Social Boldness scale assesses one's comfort or confidence within a variety of social situations. Low scorers feel shy or awkward in positions of leadership or when speaking in public, whereas high scorers are willing to approach strangers and are willing to speak up within group settings.
The Sociability scale assesses a tendency to enjoy conversation, social interaction, and parties. Low scorers generally prefer solitary activities and do not seek out conversation, whereas high scorers enjoy talking, visiting, and celebrating with others.
The Liveliness scale assesses one's typical enthusiasm and energy. Low scorers tend not to feel especially cheerful or dynamic, whereas high scorers usually experience a sense of optimism and high spirits.

Agreeableness Domain
The Forgivingness scale assesses one's willingness to feel trust and liking toward those who may have caused one harm. Low scorers tend "hold a grudge" against those who have offended them, whereas high scorers are usually ready to trust others again and to re-establish friendly relations after having been treated badly.
The Gentleness scale assesses a tendency to be mild and lenient in dealings with other people. Low scorers tend to be critical in their evaluations of others, whereas high scorers are reluctant to judge others harshly.
The Flexibility scale assesses one's willingness to compromise and cooperate with others. Low scorers are seen as stubborn and are willing to argue, whereas high scorers avoid arguments and accommodate others' suggestions, even when these may be unreasonable.
The Patience scale assesses a tendency to remain calm rather than to become angry. Low scorers tend to lose their tempers quickly, whereas high scorers have a high threshold for feeling or expressing anger.

Conscientiousness Domain
The Organization scale assesses a tendency to seek order, particularly in one's physical surroundings. Low scorers tend to be sloppy and haphazard, whereas high scorers keep things tidy and prefer a structured approach to tasks.
The Diligence scale assesses a tendency to work hard. Low scorers have little self-discipline and are not strongly motivated to achieve, whereas high scorers have a strong "'work ethic" and are willing to exert themselves.
The Perfectionism scale assesses a tendency to be thorough and concerned with details. Low scorers tolerate some errors in their work and tend to neglect details, whereas high scorers check carefully for mistakes and potential improvements.
The Prudence scale assesses a tendency to deliberate carefully and to inhibit impulses. Low scorers act on impulse and tend not to consider consequences, whereas high scorers consider their options carefully and tend to be cautious and self-controlled.

Openness to Experience Domain

The Aesthetic Appreciation scale assesses one's enjoyment of beauty in art and in nature. Low scorers tend not to become absorbed in works of art or in natural wonders, whereas high scorers have a strong appreciation of various art forms and of natural wonders.
The Inquisitiveness scale assesses a tendency to seek information about, and experience with, the natural and human world. Low scorers have little curiosity about the natural or social sciences, whereas high scorers read widely and are interested in travel.
The Creativity scale assesses one's preference for innovation and experiment. Low scorers have little inclination for original thought, whereas high scorers actively seek new solutions to problems and express themselves in art.
The Unconventionality scale assesses a tendency to accept the unusual. Low scorers avoid eccentric or nonconforming persons, whereas high scorers are receptive to ideas that might seem strange or radical.

Interstitial Scale
The Altruism (versus Antagonism) scale assesses a tendency to be sympathetic and soft-hearted toward others. High scorers avoid causing harm and react with generosity toward those who are weak or in need of help, whereas low scorers are not upset by the prospect of hurting others and may be seen as hard-hearted.

"""
