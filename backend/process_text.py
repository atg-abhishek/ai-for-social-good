import nltk
import pandas as pd
from requests import get

def eval_semantic_sim(str1, str2):
    """
    take subsentences from each part until we get a max semantic similarity score
    :param str1:
    :param str2:
    :return:
    """

    sss_url = "http://swoogle.umbc.edu/SimService/GetSimilarity"
    type = 'concept'
    corpus = 'webbase'

    try:
        response = get(sss_url,
                       params={'operation': 'api', 'phrase1': str1, 'phrase2': str2, 'type': type, 'corpus': corpus})
        score = float(response.text.strip())
        return score
    except:
        print
        'Error in getting similarity for %s: %s' % ((str1, str2), response)
        return 0.0

def get_pos_contr(pos_tags):
    # possessives
    # differentiate possessives from contractible auxiliary and contractible copula
    verb_tags = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
    adj_tags = ['JJ', 'JJR', 'JJS']
    det_tags = ['DT']
    noun_tags = ['NN', 'NNS', 'NNPS', 'NNP']
    f_possessive_s = 0
    f_cont_aux = 0
    f_cont_copula = 0
    for idx in range(len(pos_tags) - 1):
        if pos_tags[idx] == "POS":
            # if next word is a present participle verb then contractible auxiliary
            if pos_tags[idx+1] in ['VBG']:
                f_cont_aux += 1

            # if next word is a noun then possessive
            elif pos_tags[idx+1] in noun_tags:
                f_possessive_s += 1

            # if next word is an article
            elif pos_tags[idx+1] in det_tags:
                f_cont_copula += 1
            elif pos_tags[idx+1] in adj_tags:
                if pos_tags[idx+2] in noun_tags:
                    f_possessive_s += 1
                else:
                    f_cont_copula += 1

    return f_possessive_s, f_cont_aux, f_cont_copula

def filter_hesitations_from_ibm(tokens):
    new_tokens = []
    # will break if sentence ends in % but whatever
    for i in range(len(tokens)):
        if tokens[i] == '%' and tokens[i + 1].lower() == 'hesitation':
            i = i + 1
        else:
            new_tokens.append(tokens[i])

    return new_tokens


def get_feature_vec(text, times):

    text = text.lower()
    fillers = ['um', 'uh', 'oh', 'hm', '%HESITATION', 'HESITATION']

    tokens_unfiltered = nltk.word_tokenize(text)

    # remove fillers
    tokens_filtered = filter_hesitations_from_ibm(tokens_unfiltered)
    print(tokens_filtered)
    # tokens_filtered = [word for word in tokens_unfiltered if word not in fillers]

    # get time_tuples for actual words only
    filtered_times = [times[i] for i in range(len(tokens_unfiltered))
                            if tokens_unfiltered[i] in tokens_filtered]

    pos_tags = nltk.pos_tag(tokens_filtered)

    feature_dict = {}

    # get total number of filtered (mor) words
    f_number_of_words = len(tokens_filtered)
    feature_dict["child_TNW"] = f_number_of_words

    # get freq_ttr:
    f_freq_ttr =  len(set(tokens_filtered)) / len(tokens_filtered)
    feature_dict["freq_ttr"]= f_freq_ttr

    # get r_2_i_verbs
    raw_verbs = [verbs for verbs in pos_tags if verbs[1] == 'VB']
    inf_verbs = [verbs for verbs in pos_tags if verbs[1] in ['VBD', 'VBG', 'VBN', 'VBP', 'VBZ']]
    f_r_2_i_verbs = float(len(raw_verbs))/len(inf_verbs)
    feature_dict["r_2_i_verbs"] = f_r_2_i_verbs

    # get num_pos_tags
    pos_tags_set = set([pos[1] for pos in pos_tags])
    f_num_pos_tags = len(pos_tags_set)
    feature_dict["num_pos_tags"] = f_num_pos_tags


    # get n_dos ?

    # get repetition
    f_repetitions = 0
    prev_word = tokens_filtered[0]
    for word in tokens_filtered[1:]:
        if word == prev_word:
            f_repetitions += 1
        prev_word = word

    feature_dict["repetitions"] = f_repetitions

    # get retracing (check for filler or hesitation and semantic similarity)
    threshold = 0.85
    f_retracing = 0
    for word in tokens_unfiltered:
        if word in fillers:
            # partition the text before the word and after
            sep_index = tokens_unfiltered.index(word)
            prev_sentence = tokens_filtered[0:sep_index]
            next_sentence = tokens_filtered[sep_index:]
            semantic_similarity = eval_semantic_sim(' '.join(prev_sentence), ' '.join(next_sentence))
            if semantic_similarity >= threshold:
                f_retracing += 1

    feature_dict["retracing"] = f_retracing

    # get fillers
    f_fillers = len(tokens_unfiltered) - len(tokens_filtered)
    feature_dict['fillers'] = f_fillers

    # get mlu_words (mean length of utterance calculated for actual words)
    time_list = []
    avg = 0
    for time in filtered_times:
        utterance_length = time
        time_list.append(utterance_length)
        avg += utterance_length

    f_mlu_words = avg/f_number_of_words
    feature_dict["mlu_words"] = f_mlu_words

    # verb_utt
    verb_list = []
    f_verb_utt = 0
    for tag in pos_tags:
        if tag[1] in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
            verb_list.append(tag)
            f_verb_utt += 1

    feature_dict["verb_utt"] = f_verb_utt

    # prep_in (number of times 'in' was said)
    f_prep_in = 0
    for word in tokens_filtered:
        if word == "in":
            f_prep_in += 1
    feature_dict["proposition_in"] = f_prep_in

    f_prep_on = 0
    # propositions_on (number of times 'on' was said)
    for word in tokens_filtered:
        if word == "on":
            f_prep_on += 1
    feature_dict["proposition_on"] = f_prep_in

    # present progressive "is doing, is drinking"
    f_present_prog = 0
    for idx in range(len(pos_tags) - 1):
        if pos_tags[idx][0] in ['is', 'are', 'am', "'s", "'re", "'m"]:
            if pos_tags[idx+1][1] == "VBG":
                f_present_prog += 1

    feature_dict["present_progressive"] = f_present_prog

    # f_plural (number of plural nouns)
    f_plural = 0
    for tag in pos_tags:
        if tag[1] == "NNS":
            f_plural += 1

    feature_dict["plural_s"] = f_plural

    # f_irreg_past (number of irregular past verbs)
    f_reg_past = 0
    f_irreg_past = 0
    for verb in verb_list:
        if verb[1] == "VBN":
            word = list(verb[0])
            if word[-2]+word[-1] == "ed":
                f_reg_past += 1
            else:
                f_irreg_past += 1

    feature_dict["regular_past_tense"] = f_reg_past
    feature_dict["irregular_past_tense"] = f_irreg_past

    f_possessive_s, f_cont_aux, f_cont_copula, = get_pos_contr(pos_tags)
    feature_dict["possessive_s"] = f_possessive_s

    # get contr_aux, and contr_copula not singular 3rd persom
    for idx in range(len(pos_tags) - 1):
        if pos_tags[idx][0] in ['re', 'm']:
            # followed by adjectives, nouns, or pronouns
            if pos_tags[idx+1][1] in ['JJ', 'JJR', 'JJS', 'NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'PRP$']:
                f_cont_copula += 1
            elif pos_tags[idx+1][1] in ['VBG', 'VBN', 'VBD']:
                f_cont_aux += 1

    feature_dict["contractible_copula"] = f_cont_copula
    feature_dict["contractible_auxiliary"] = f_cont_aux

   # get uncont_aux, uncont_copula
    f_uncont_aux = 0
    f_uncont_copula = 0
    for idx in range(len(pos_tags) - 1):
        if pos_tags[idx][0] in ['are', 'am', 'is']:
            # followed by adjectives, nouns, or pronouns
            if pos_tags[idx+1][1] in ['JJ', 'JJR', 'JJS', 'NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'PRP$']:
                f_uncont_copula += 1
            elif pos_tags[idx+1][1] in ['VBG', 'VBN', 'VBD']:
                f_uncont_aux += 1

    feature_dict["uncontractible_auxiliary"] = f_uncont_aux
    feature_dict["uncontractible_copula"] = f_uncont_copula

    # get z-score features
    sli_df = pd.read_csv('data/sli.csv', index_col=0)
    td_df = pd.read_csv('data/td.csv', index_col=0)

    mean_mlu_sli = sli_df.loc['mean', 'mlu_words']
    std_mlu_sli = sli_df.loc['std', 'mlu_words']

    mean_ndw_sli = sli_df.loc['mean', 'r_2_i_verbs']
    std_ndw_sli = sli_df.loc['std', 'r_2_i_verbs', ]

    mean_utts_sli = sli_df.loc['mean', 'verb_utt']
    std_utts_sli= sli_df.loc['std', 'verb_utt']

    mean_mlu_td = td_df.loc['mean', 'mlu_words', ]
    std_mlu_td = td_df.loc['std', 'mlu_words']

    mean_ndw_td = td_df.loc['mean', 'r_2_i_verbs']
    std_ndw_td = td_df.loc['std', 'r_2_i_verbs']

    mean_utts_td = td_df.loc['mean', 'verb_utt']
    std_utts_td = td_df.loc['std', 'verb_utt']

    z_mlu_td = (f_mlu_words - mean_mlu_td)/std_mlu_td
    feature_dict["z_mlu_td"] = z_mlu_td

    z_ndw_td = (f_r_2_i_verbs - mean_ndw_td)/std_ndw_td
    feature_dict["z_ndw_td"] = z_ndw_td

    z_utts_td = (f_verb_utt - mean_utts_td)/std_utts_td
    feature_dict["z_utts_td"] = z_utts_td

    z_mlu_sli = (f_mlu_words - mean_mlu_sli)/std_mlu_sli
    feature_dict["z_mlu_sli"] = z_mlu_sli

    z_ndw_sli = (f_r_2_i_verbs - mean_ndw_sli)/std_ndw_sli
    feature_dict["z_ndw_sli"] = z_ndw_sli

    z_utts_sli = (f_verb_utt - mean_utts_sli)/std_utts_sli
    feature_dict["z_utts_sli"] = z_utts_sli


    # grammar errors

    return feature_dict

def get_feature_vec_default_times(text):
    tokens = nltk.word_tokenize(text)
    times = [0.1]*len(tokens)
    pos_tags = nltk.pos_tag(tokens)
    return get_feature_vec(text, times)

def dictionary2row(dictionary):
    df = pd.DataFrame.from_dict(dictionary, orient='columns')
    return [
        df['child_TNW'],
        5.0,
        0,
        df['freq_ttr'],
        df['r_2_i_verbs'],
        df['num_pos_tags'],
        df['repetition'],
        df['retracing'],
        df['fillers'],
        df['z_mlu_sli'],
        df['z_mlu_td'],
        df['z_ndw_td'],
        df['z_utts_sli'],
        df['z_utts_td'],
        df['mlu_words'],
        df['verb_utt'],
        df['present_progressive'],
        df['proposition_in'],
        df['propositions_out'],
        df['plural_s'],
        df['irregular_past_tense'],
        df['possessive_s'],
        df['uncontractible_copula'],
        df['regular_past_tense'],
        2, #regular_3rd,
        2, #irregular_3rd,
        df['uncontractible_auxiliary'],
        df['contractible_copula'],
        df['contractible_auxiliary'],
        5 # total error
    ]
'''
if __name__ == "__main__":
    text_1 = "the red fox jumped over uh the red fox jumped over the hungry dog"
    text_2 = "Last night I was on the subway um so last night I was on the Montreal metro"
    text_3 = "the child eats apples bananas tomatoes uh carrots."
    text_4 = "We like to eat pizza salads sandwiches and uh all food in general"
    text_5 = "The day before last uh before yesterday we went swimming in the uh waterpark"
    text_6 = "The runner has beaten her best running time"
    text_7 = "I don't know how to use SQL"
    text_8 = "My sister's graduating this summer"
    text_9 = "They're coming"
    text_10 = "She's coming"

    tokens = nltk.word_tokenize(text_6)
    times = [0.1]*len(tokens)
    pos_tags = nltk.pos_tag(tokens)
    print(pos_tags)
    print(get_feature_vec(text_6, times))

    # tokens = nltk.word_tokenize(text_8)
    # pos_tags = nltk.pos_tag(tokens)
    # print(pos_tags)
'''
