import nltk
from requests import get
from nltk import grammar, parse
from collections import Counter

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
    except:
        print
        'Error in getting similarity for %s: %s' % ((str1, str2), response)
        return 0.0

def get_pos_contr(str, pos_tags):
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


def get_feature_vec(text, time_tuples):

    text = text.lower()
    fillers = ['um', 'uh', 'oh', 'hm', '%HESITATION']

    tokens_unfiltered = nltk.word_tokenize(text)

    # remove fillers
    tokens_filtered = [word for word in tokens_unfiltered if word not in fillers]

    # get time_tuples for actual words only
    filtered_time_tuples = [time_tuples[i] for i in range(len(tokens_unfiltered))
                            if tokens_unfiltered[i] in tokens_filtered]

    pos_tags = nltk.pos_tag(tokens_filtered)

    # get total number of filtered (mor) words
    f_number_of_words = len(tokens_filtered)

    # get freq_ttr:
    f_freg_ttr =  len(set(tokens_filtered)) / len(tokens_filtered)

    # get r_2_i_verbs
    raw_verbs = [verbs for verbs in pos_tags if verbs[1] == 'VB']
    inf_verbs = [verbs for verbs in pos_tags if verbs[1] in ['VBD', 'VBG', 'VBN', 'VBP', 'VBZ']]
    f_r_2_i_verbs = float(len(raw_verbs))/len(inf_verbs)

    # get num_pos_tags
    pos_tags_set = set([pos[1] for pos in pos_tags])
    f_num_pos_tags = len(pos_tags_set)

    # get n_dos ?

    # get repetition
    f_repetitions = 0
    prev_word = tokens_filtered[0]
    for word in tokens_filtered[1:]:
        if word == prev_word:
            f_repetitions += 1
        prev_word = word

    # get retracing (check for filler or hesitation and semantic similarity)
    # threshold = 0.7
    # f_retracing = 0
    # for word in tokens_unfiltered:
    #     if word in fillers:
    #         # partition the text before the word and after
    #         sep_index = tokens_unfiltered.index(word)
    #         prev_sentence = tokens_filtered[0:sep_index]
    #         next_sentence = tokens_filtered[sep_index:]
    #         semantic_similarity = eval_semantic_sim(' '.join(prev_sentence), ' '.join(next_sentence))
    #         if semantic_similarity >= threshold:
    #             f_retracing += 1

    # get fillers
    f_fillers = len(tokens_unfiltered) - len(tokens_filtered)

    # get mlu_words (mean length of utterance calculated for actual words)
    time_list = []
    avg = 0
    for tuple in filtered_time_tuples:
        utterance_length = tuple[1]-tuple[0]
        time_list.append(utterance_length)
        avg += utterance_length

    f_mlu_words = avg/f_number_of_words

    # verb_utt
    verb_list = []
    f_verb_utt = 0
    for tag in pos_tags:
        if tag[1] in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
            verb_list.append(tag)
            f_verb_utt += 1

    # prep_in (number of times 'in' was said)
    f_prep_in = 0
    for word in tokens_filtered:
        if word == "in":
            f_prep_in += 1

    f_prep_on = 0
    # propositions_on (number of times 'on' was said)
    for word in tokens_filtered:
        if word == "on":
            f_prep_on += 1

    # present progressive "is doing, is drinking"
    f_present_prog = 0
    for idx in range(len(pos_tags) - 1):
        if pos_tags[idx][0] == "is" or pos_tags[idx][0] == "are":
            if pos_tags[idx+1][1] == "VBG":
                f_present_prog += 1

    # f_plural (number of plural nouns)
    f_plural = 0
    for tag in pos_tags:
        if tag[1] == "NNS":
            f_plural += 1

    # f_irreg_past (number of irregular past verbs)
    f_irreg_past = 0
    for verb in verb_list:
        if verb[1] == "VBN":
            word = list(verb[0])
            if word[-2]+word[-1] == "ed":
                f_irreg_past += 1

    # word errors (CHILDES)


    return pos_tags

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

    # print(get_feature_vec(text_6))

    tokens = nltk.word_tokenize(text_8)
    pos_tags = nltk.pos_tag(tokens)
    print(pos_tags)