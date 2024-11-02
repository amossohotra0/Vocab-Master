import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vocab_flashcards.settings')
django.setup()

from vocabulary.models import WordsBank, WordList, WordType, DifficultyLevel

# Create word types
word_types_data = [
    ('noun', 'n.'),
    ('verb', 'v.'),
    ('adjective', 'adj.'),
    ('adverb', 'adv.'),
    ('preposition', 'prep.'),
    ('conjunction', 'conj.'),
]

for word_type, abbr in word_types_data:
    WordType.objects.get_or_create(word_type=word_type, defaults={'abbreviation': abbr})

# Create difficulty levels
difficulty_levels = ['beginner', 'intermediate', 'advanced', 'expert']
for level in difficulty_levels:
    DifficultyLevel.objects.get_or_create(level=level)

# Create word lists
word_lists_data = [
    ('Barron SAT 3500', 'Essential SAT vocabulary words'),
    ('GRE Vocabulary', 'Graduate Record Examination words'),
    ('Academic Words', 'Common academic vocabulary'),
]

for name, desc in word_lists_data:
    WordList.objects.get_or_create(word_list_name=name, defaults={'description': desc})

# Get objects for foreign keys
noun_type = WordType.objects.get(word_type='noun')
verb_type = WordType.objects.get(word_type='verb')
adj_type = WordType.objects.get(word_type='adjective')
adv_type = WordType.objects.get(word_type='adverb')

beginner = DifficultyLevel.objects.get(level='beginner')
intermediate = DifficultyLevel.objects.get(level='intermediate')
advanced = DifficultyLevel.objects.get(level='advanced')
expert = DifficultyLevel.objects.get(level='expert')

# 100 comprehensive vocabulary words
words_data = [
    ("aberrant", adj_type, intermediate, "غیر معمولی، منحرف", "deviating from what is normal", "His aberrant behavior worried his friends.", "abnormal, deviant", "normal, typical", "/ˈæbərənt/"),
    ("abscond", verb_type, advanced, "فرار ہونا", "to leave hurriedly and secretly", "The thief absconded with the stolen jewelry.", "flee, escape", "remain, stay", "/æbˈskɒnd/"),
    ("acumen", noun_type, advanced, "تیز فہمی", "ability to make good judgments", "Her business acumen helped the company grow.", "insight, shrewdness", "stupidity, ignorance", "/əˈkjuːmən/"),
    ("admonish", verb_type, intermediate, "تنبیہ کرنا", "to warn or reprimand someone firmly", "The teacher admonished the student for cheating.", "warn, scold", "praise, commend", "/ədˈmɒnɪʃ/"),
    ("aesthetic", adj_type, intermediate, "جمالیاتی", "concerned with beauty or art", "The museum's aesthetic appeal attracted many visitors.", "artistic, beautiful", "ugly, unattractive", "/iːsˈθetɪk/"),
    ("benevolent", adj_type, beginner, "مہربان", "well meaning and kindly", "The benevolent donor helped many students.", "kind, generous", "cruel, malicious", "/bɪˈnevələnt/"),
    ("candid", adj_type, intermediate, "صاف گو", "truthful and straightforward", "She gave a candid assessment of the situation.", "honest, frank", "dishonest, deceptive", "/ˈkændɪd/"),
    ("diligent", adj_type, beginner, "محنتی", "having or showing care in one's work", "The diligent student always completed assignments on time.", "hardworking, careful", "lazy, careless", "/ˈdɪlɪdʒənt/"),
    ("eloquent", adj_type, intermediate, "فصیح", "fluent or persuasive in speaking", "The eloquent speaker moved the audience to tears.", "articulate, fluent", "inarticulate, tongue-tied", "/ˈeləkwənt/"),
    ("frugal", adj_type, intermediate, "کفایت شعار", "sparing or economical with money", "His frugal lifestyle helped him save for retirement.", "thrifty, economical", "wasteful, extravagant", "/ˈfruːɡəl/"),
    ("gregarious", adj_type, intermediate, "ملنسار", "fond of company; sociable", "She was gregarious and made friends easily.", "sociable, outgoing", "antisocial, solitary", "/ɡrɪˈɡeərɪəs/"),
    ("hackneyed", adj_type, advanced, "گھسا پٹا", "lacking originality or freshness", "The movie's plot was hackneyed and predictable.", "clichéd, trite", "original, fresh", "/ˈhæknɪd/"),
    ("immutable", adj_type, expert, "غیر متبدل", "unchanging over time", "The laws of physics are considered immutable.", "unchangeable, fixed", "changeable, variable", "/ɪˈmjuːtəbəl/"),
    ("jovial", adj_type, intermediate, "خوش مزاج", "cheerful and friendly", "His jovial personality made him popular at parties.", "cheerful, jolly", "gloomy, morose", "/ˈdʒoʊviəl/"),
    ("kinetic", adj_type, advanced, "حرکی", "relating to or resulting from motion", "The kinetic energy of the moving car was enormous.", "dynamic, active", "static, motionless", "/kɪˈnetɪk/"),
    ("lucid", adj_type, intermediate, "واضح", "expressed clearly; easy to understand", "Her lucid explanation helped everyone understand.", "clear, coherent", "confusing, unclear", "/ˈluːsɪd/"),
    ("meticulous", adj_type, intermediate, "باریک بین", "showing great attention to detail", "The meticulous researcher checked every fact twice.", "careful, precise", "careless, sloppy", "/mɪˈtɪkjələs/"),
    ("nonchalant", adj_type, advanced, "لاپرواہ", "feeling or appearing casually calm", "He remained nonchalant despite the crisis.", "casual, indifferent", "concerned, anxious", "/ˌnɒnʃəˈlɑːnt/"),
    ("ostentatious", adj_type, advanced, "نمائشی", "characterized by vulgar display", "Her ostentatious jewelry drew unwanted attention.", "showy, flashy", "modest, understated", "/ˌɒstənˈteɪʃəs/"),
    ("pragmatic", adj_type, intermediate, "عملی", "dealing with things sensibly", "She took a pragmatic approach to solving the problem.", "practical, realistic", "idealistic, impractical", "/præɡˈmætɪk/"),
    ("quixotic", adj_type, expert, "خیالی", "extremely idealistic and unrealistic", "His quixotic plan to end world hunger was admirable but impossible.", "idealistic, impractical", "realistic, practical", "/kwɪkˈsɒtɪk/"),
    ("resilient", adj_type, intermediate, "لچکدار", "able to withstand or recover quickly", "The resilient community rebuilt after the disaster.", "tough, adaptable", "fragile, brittle", "/rɪˈzɪliənt/"),
    ("sanguine", adj_type, advanced, "پر امید", "optimistic or positive", "Despite setbacks, she remained sanguine about success.", "optimistic, hopeful", "pessimistic, gloomy", "/ˈsæŋɡwɪn/"),
    ("tenacious", adj_type, intermediate, "ثابت قدم", "tending to keep a firm hold", "His tenacious grip on the rope saved his life.", "persistent, determined", "weak, yielding", "/tɪˈneɪʃəs/"),
    ("ubiquitous", adj_type, advanced, "ہر جگہ موجود", "present everywhere", "Smartphones have become ubiquitous in modern society.", "omnipresent, widespread", "rare, scarce", "/juːˈbɪkwɪtəs/"),
    ("verbose", adj_type, intermediate, "بہت بولنے والا", "using more words than needed", "The verbose speaker lost the audience's attention.", "wordy, long-winded", "concise, brief", "/vɜːˈboʊs/"),
    ("wary", adj_type, beginner, "محتاط", "feeling or showing caution", "She was wary of strangers offering help.", "cautious, careful", "trusting, careless", "/ˈweri/"),
    ("xenophobic", adj_type, expert, "غیر ملکیوں سے نفرت", "having dislike of foreigners", "The xenophobic politician promoted isolationist policies.", "prejudiced, bigoted", "welcoming, accepting", "/ˌziːnəˈfoʊbɪk/"),
    ("zealous", adj_type, intermediate, "جوشیلا", "having great energy for a cause", "The zealous activist campaigned tirelessly for change.", "enthusiastic, fervent", "apathetic, indifferent", "/ˈzeləs/"),
    ("abate", verb_type, intermediate, "کم ہونا", "to become less intense", "The storm began to abate after midnight.", "diminish, subside", "increase, intensify", "/əˈbeɪt/"),
    ("capitulate", verb_type, advanced, "ہتھیار ڈالنا", "to cease to resist", "The army was forced to capitulate after the siege.", "surrender, yield", "resist, fight", "/kəˈpɪtʃəleɪt/"),
    ("debilitate", verb_type, advanced, "کمزور کرنا", "to make weak", "The illness debilitated him for months.", "weaken, enfeeble", "strengthen, invigorate", "/dɪˈbɪlɪteɪt/"),
    ("elucidate", verb_type, advanced, "وضاحت کرنا", "to make clear", "The professor elucidated the complex theory.", "clarify, explain", "confuse, obscure", "/ɪˈluːsɪdeɪt/"),
    ("fabricate", verb_type, intermediate, "بنانا، جھوٹ بولنا", "to invent or make up", "He fabricated an excuse for being late.", "invent, concoct", "tell truth, reveal", "/ˈfæbrɪkeɪt/"),
    ("galvanize", verb_type, advanced, "متحرک کرنا", "to shock into action", "The speech galvanized the crowd into action.", "stimulate, energize", "discourage, demotivate", "/ˈɡælvənaɪz/"),
    ("hamper", verb_type, intermediate, "رکاوٹ ڈالنا", "to hinder or impede", "Bad weather hampered the rescue efforts.", "hinder, obstruct", "help, facilitate", "/ˈhæmpər/"),
    ("impede", verb_type, intermediate, "رکاوٹ ڈالنا", "to delay or prevent", "Traffic congestion impeded our progress.", "hinder, obstruct", "help, assist", "/ɪmˈpiːd/"),
    ("jeopardize", verb_type, intermediate, "خطرے میں ڈالنا", "to put at risk", "His reckless behavior jeopardized the mission.", "endanger, threaten", "protect, safeguard", "/ˈdʒepərdaɪz/"),
    ("kindle", verb_type, beginner, "جلانا، بھڑکانا", "to light or arouse", "The speech kindled hope in the audience.", "ignite, arouse", "extinguish, dampen", "/ˈkɪndəl/"),
    ("languish", verb_type, advanced, "کمزور ہونا", "to lose vigor", "The plants languished without water.", "weaken, decline", "flourish, thrive", "/ˈlæŋɡwɪʃ/"),
    ("mitigate", verb_type, advanced, "کم کرنا", "to make less severe", "The medicine helped mitigate the pain.", "alleviate, reduce", "worsen, aggravate", "/ˈmɪtɪɡeɪt/"),
    ("nullify", verb_type, advanced, "منسوخ کرنا", "to make legally null", "The court nullified the contract.", "cancel, void", "validate, confirm", "/ˈnʌlɪfaɪ/"),
    ("obviate", verb_type, expert, "ضرورت ختم کرنا", "to remove a need", "The new system obviated manual calculations.", "eliminate, prevent", "necessitate, require", "/ˈɒbvieɪt/"),
    ("perpetuate", verb_type, advanced, "برقرار رکھنا", "to make continue indefinitely", "The tradition perpetuated through generations.", "maintain, preserve", "end, discontinue", "/pərˈpetʃueɪt/"),
    ("quell", verb_type, advanced, "دبانا", "to put an end to", "The police quelled the riot quickly.", "suppress, subdue", "incite, provoke", "/kwel/"),
    ("rectify", verb_type, intermediate, "درست کرنا", "to put right", "We need to rectify this mistake immediately.", "correct, fix", "worsen, damage", "/ˈrektɪfaɪ/"),
    ("substantiate", verb_type, advanced, "ثابت کرنا", "to provide evidence", "He could not substantiate his claims.", "prove, verify", "disprove, refute", "/səbˈstænʃieɪt/"),
    ("truncate", verb_type, advanced, "کاٹنا", "to shorten by cutting", "The editor truncated the lengthy article.", "shorten, cut", "extend, lengthen", "/ˈtrʌŋkeɪt/"),
    ("undermine", verb_type, intermediate, "کمزور کرنا", "to erode the base", "Constant criticism undermined his confidence.", "weaken, sabotage", "strengthen, support", "/ˌʌndərˈmaɪn/"),
    ("vindicate", verb_type, advanced, "بری کرنا", "to clear of blame", "New evidence vindicated the accused.", "exonerate, justify", "blame, condemn", "/ˈvɪndɪkeɪt/"),
    ("wane", verb_type, intermediate, "کم ہونا", "to decrease in size", "His enthusiasm began to wane over time.", "decline, diminish", "increase, grow", "/weɪn/"),
    ("exacerbate", verb_type, advanced, "بڑھانا", "to make worse", "The medication exacerbated his symptoms.", "worsen, aggravate", "improve, alleviate", "/ɪɡˈzæsərbeɪt/"),
    ("alacrity", noun_type, advanced, "تیزی", "brisk eagerness", "She accepted the offer with alacrity.", "eagerness, enthusiasm", "reluctance, hesitation", "/əˈlækrɪti/"),
    ("brevity", noun_type, intermediate, "اختصار", "concise expression", "The brevity of his speech was appreciated.", "conciseness, terseness", "verbosity, wordiness", "/ˈbrevɪti/"),
    ("cacophony", noun_type, advanced, "شور", "harsh discordant sound", "The cacophony of car horns was deafening.", "noise, discord", "harmony, melody", "/kəˈkɒfəni/"),
    ("duplicity", noun_type, advanced, "دوغلا پن", "deceitfulness", "His duplicity was eventually exposed.", "deception, dishonesty", "honesty, sincerity", "/duːˈplɪsɪti/"),
    ("euphoria", noun_type, intermediate, "خوشی", "feeling of elation", "Winning the lottery filled him with euphoria.", "elation, joy", "depression, sadness", "/juːˈfɔːriə/"),
    ("fallacy", noun_type, intermediate, "غلط فہمی", "mistaken belief", "His argument was based on a logical fallacy.", "misconception, error", "truth, fact", "/ˈfæləsi/"),
    ("grandeur", noun_type, intermediate, "عظمت", "splendor and impressiveness", "The grandeur of the palace was breathtaking.", "magnificence, splendor", "simplicity, modesty", "/ˈɡrændʒər/"),
    ("hierarchy", noun_type, intermediate, "درجہ بندی", "ranking system", "The company has a strict hierarchy.", "ranking, order", "equality, disorder", "/ˈhaɪərɑːrki/"),
    ("impunity", noun_type, advanced, "سزا سے بچاؤ", "exemption from punishment", "He acted with complete impunity.", "immunity, exemption", "accountability, liability", "/ɪmˈpjuːnɪti/"),
    ("juxtaposition", noun_type, expert, "پاس پاس رکھنا", "placing close together", "The juxtaposition of old and new architecture was striking.", "contrast, comparison", "separation, isolation", "/ˌdʒʌkstəpəˈzɪʃən/"),
    ("lethargy", noun_type, intermediate, "سستی", "lack of energy", "The hot weather induced lethargy in everyone.", "sluggishness, fatigue", "energy, vigor", "/ˈleθərdʒi/"),
    ("malice", noun_type, intermediate, "بغض", "desire to harm others", "She spoke without malice, only concern.", "spite, hatred", "kindness, goodwill", "/ˈmælɪs/"),
    ("nostalgia", noun_type, beginner, "ماضی کی یاد", "sentimental longing", "The old photos filled her with nostalgia.", "longing, reminiscence", "anticipation, future-focus", "/nɒˈstældʒə/"),
    ("opulence", noun_type, advanced, "دولت", "great wealth", "The opulence of the mansion was overwhelming.", "luxury, wealth", "poverty, simplicity", "/ˈɒpjələns/"),
    ("paradox", noun_type, intermediate, "تضاد", "seemingly contradictory statement", "It's a paradox that the more choices we have, the harder it is to choose.", "contradiction, puzzle", "consistency, clarity", "/ˈpærədɒks/"),
    ("quandary", noun_type, intermediate, "مشکل", "state of uncertainty", "She found herself in a quandary about which job to take.", "dilemma, predicament", "certainty, clarity", "/ˈkwɒndəri/"),
    ("rancor", noun_type, advanced, "کینہ", "bitterness or resentment", "Despite their divorce, there was no rancor between them.", "resentment, animosity", "goodwill, friendship", "/ˈræŋkər/"),
    ("scrutiny", noun_type, intermediate, "جانچ پڑتال", "critical observation", "The proposal came under intense scrutiny.", "examination, inspection", "neglect, oversight", "/ˈskruːtɪni/"),
    ("trepidation", noun_type, advanced, "خوف", "feeling of fear", "She approached the interview with trepidation.", "anxiety, apprehension", "confidence, boldness", "/ˌtrepɪˈdeɪʃən/"),
    ("unanimity", noun_type, advanced, "اتفاق رائے", "complete agreement", "The committee reached unanimity on the proposal.", "consensus, agreement", "disagreement, discord", "/ˌjuːnəˈnɪmɪti/"),
    ("veracity", noun_type, advanced, "سچائی", "conformity to truth", "The veracity of his statement was questioned.", "truthfulness, accuracy", "falsehood, deception", "/vəˈræsɪti/"),
    ("whimsy", noun_type, intermediate, "سودا", "playful fancy", "The garden was designed with delightful whimsy.", "playfulness, caprice", "seriousness, solemnity", "/ˈwɪmzi/"),
    ("xenophobia", noun_type, expert, "غیر ملکیوں سے نفرت", "dislike of foreigners", "The rise in xenophobia concerned human rights groups.", "prejudice, bigotry", "acceptance, tolerance", "/ˌziːnəˈfoʊbiə/"),
    ("yearning", noun_type, beginner, "تڑپ", "intense longing", "His yearning for home grew stronger each day.", "longing, craving", "satisfaction, contentment", "/ˈjɜːrnɪŋ/"),
    ("zeal", noun_type, intermediate, "جوش", "great energy or enthusiasm", "Her zeal for the project inspired the team.", "enthusiasm, passion", "apathy, indifference", "/ziːl/"),
    ("arduous", adj_type, intermediate, "مشکل", "involving hard work", "The arduous journey took three days.", "difficult, strenuous", "easy, effortless", "/ˈɑːrdjuəs/"),
    ("banal", adj_type, advanced, "عام", "lacking originality", "The movie's plot was disappointingly banal.", "commonplace, trite", "original, unique", "/bəˈnæl/"),
    ("cogent", adj_type, advanced, "مؤثر", "clear and logical", "She made a cogent argument for the proposal.", "convincing, compelling", "weak, unconvincing", "/ˈkoʊdʒənt/"),
    ("dormant", adj_type, intermediate, "سوتا ہوا", "temporarily inactive", "The volcano has been dormant for centuries.", "inactive, sleeping", "active, awake", "/ˈdɔːrmənt/"),
    ("ephemeral", adj_type, expert, "عارضی", "lasting for a short time", "The beauty of cherry blossoms is ephemeral.", "temporary, fleeting", "permanent, lasting", "/ɪˈfemərəl/"),
    ("fastidious", adj_type, advanced, "نکتہ چین", "very attentive to detail", "He was fastidious about his appearance.", "meticulous, particular", "careless, sloppy", "/fæˈstɪdiəs/"),
    ("garrulous", adj_type, advanced, "بہت بولنے والا", "excessively talkative", "The garrulous old man told endless stories.", "talkative, chatty", "quiet, taciturn", "/ˈɡærələs/"),
    ("hapless", adj_type, intermediate, "بدقسمت", "unfortunate", "The hapless tourist lost his wallet and passport.", "unlucky, unfortunate", "fortunate, lucky", "/ˈhæpləs/"),
    ("inane", adj_type, advanced, "بے معنی", "lacking sense", "His inane comments annoyed everyone.", "silly, senseless", "sensible, meaningful", "/ɪˈneɪn/"),
    ("jocular", adj_type, advanced, "مزاحیہ", "fond of joking", "His jocular manner lightened the mood.", "humorous, playful", "serious, solemn", "/ˈdʒɒkjələr/"),
    ("laconic", adj_type, expert, "کم گو", "using few words", "His laconic response surprised everyone.", "brief, concise", "verbose, wordy", "/ləˈkɒnɪk/"),
    ("mundane", adj_type, intermediate, "عام", "lacking interest", "She was tired of her mundane daily routine.", "ordinary, boring", "exciting, extraordinary", "/mʌnˈdeɪn/"),
    ("nascent", adj_type, advanced, "ابتدائی", "just coming into existence", "The nascent technology showed great promise.", "emerging, developing", "mature, established", "/ˈnæsənt/"),
    ("obtuse", adj_type, advanced, "کند ذہن", "slow to understand", "He was being deliberately obtuse about the issue.", "dense, stupid", "sharp, intelligent", "/əbˈtuːs/"),
    ("palpable", adj_type, intermediate, "محسوس", "able to be touched or felt", "The tension in the room was palpable.", "tangible, obvious", "intangible, imperceptible", "/ˈpælpəbəl/"),
    ("quaint", adj_type, beginner, "دلچسپ", "attractively unusual", "The quaint village charmed all visitors.", "charming, picturesque", "modern, ordinary", "/kweɪnt/"),
    ("raucous", adj_type, intermediate, "شور مچانے والا", "making harsh noise", "The raucous crowd cheered loudly.", "noisy, rowdy", "quiet, peaceful", "/ˈrɔːkəs/"),
    ("serene", adj_type, beginner, "پرسکون", "calm and peaceful", "The serene lake reflected the mountains.", "peaceful, tranquil", "chaotic, turbulent", "/səˈriːn/"),
    ("taciturn", adj_type, advanced, "کم بولنے والا", "reserved in speech", "The taciturn man rarely spoke in meetings.", "quiet, reserved", "talkative, chatty", "/ˈtæsɪtɜːrn/"),
    ("urbane", adj_type, advanced, "شہری", "refined in manner", "His urbane sophistication impressed everyone.", "suave, polished", "crude, unsophisticated", "/ɜːrˈbeɪn/"),
    ("vivacious", adj_type, intermediate, "زندہ دل", "attractively lively", "Her vivacious personality lit up the room.", "lively, spirited", "dull, lifeless", "/vɪˈveɪʃəs/"),
    ("wistful", adj_type, intermediate, "اداس", "having a feeling of longing", "She cast a wistful glance at her childhood home.", "nostalgic, yearning", "content, satisfied", "/ˈwɪstfəl/"),
    ("xenial", adj_type, expert, "مہمان نواز", "of hospitality", "The xenial customs of the culture impressed visitors.", "hospitable, welcoming", "inhospitable, unwelcoming", "/ˈziːniəl/"),
    ("youthful", adj_type, beginner, "جوان", "having youth characteristics", "Despite his age, he maintained a youthful appearance.", "young, vigorous", "old, aged", "/ˈjuːθfəl/"),
    ("zestful", adj_type, intermediate, "پر جوش", "characterized by enthusiasm", "Her zestful approach to life was contagious.", "enthusiastic, energetic", "apathetic, listless", "/ˈzestfəl/"),
    ("adroitly", adv_type, advanced, "مہارت سے", "in a skillful manner", "She adroitly handled the difficult situation.", "skillfully, cleverly", "clumsily, awkwardly", "/əˈdrɔɪtli/"),
    ("brusquely", adv_type, advanced, "رکھے انداز میں", "in an abrupt manner", "He brusquely dismissed their concerns.", "abruptly, curtly", "gently, politely", "/ˈbrʌskli/"),
    ("circumspectly", adv_type, expert, "احتیاط سے", "in a careful manner", "She circumspectly approached the sensitive topic.", "carefully, cautiously", "recklessly, carelessly", "/ˈsɜːrkəmspektli/"),
    ("deftly", adv_type, intermediate, "مہارت سے", "in a skillful way", "He deftly avoided answering the question.", "skillfully, adeptly", "clumsily, awkwardly", "/ˈdeftli/"),
    ("earnestly", adv_type, beginner, "سنجیدگی سے", "with sincere conviction", "She earnestly pleaded for understanding.", "sincerely, seriously", "insincerely, jokingly", "/ˈɜːrnɪstli/"),
]

# Add words to database
barron_list = WordList.objects.get(word_list_name='Barron SAT 3500')

for word_data in words_data:
    word, word_type, difficulty, meaning_urdu, meaning_english, example, synonyms, antonyms, pronunciation = word_data
    
    word_obj, created = WordsBank.objects.get_or_create(
        word=word,
        defaults={
            'word_type': word_type,
            'difficulty_level': difficulty,
            'meaning_urdu': meaning_urdu,
            'meaning_english': meaning_english,
            'example_sentence': example,
            'synonyms': synonyms,
            'antonyms': antonyms,
            'pronunciation': pronunciation,
        }
    )
    
    if created:
        word_obj.word_lists.add(barron_list)

print(f"Added {len(words_data)} comprehensive vocabulary words to the database!")