import pandas as pd
from pprint import pprint
import statistics


def calculate_mean_stdev_entire():
    df = pd.read_csv('data/all_data_R.csv')
    df_sli = df.loc[df['group'] == "SLI"]
    df_td = df.loc[df['group'] == "TD"]

    df_sli.describe().to_csv('data/sli.csv')
    df_td.describe().to_csv('data/td.csv')

    # sli_mlu_list = df['mlu_words'].tolist()
    # td_mlu_list = df['mlu_words'].tolist()

    # sli_mlu_mean = sum(sli_mlu_list)/len(sli_mlu_list)
    # td_mlu_mean = sum(td_mlu_list)/len(td_mlu_list)

    # sli_mlu_stdev = statistics.stdev(sli_mlu_list)
    # td_mlu_stdev = statistics.stdev(td_mlu_list)

    # sli_r_2_i_verbs_list = df['r_2_i_verbs'].tolist()
    # td_r_2_i_verbs_list = df['r_2_i_verbs'].tolist()

    # sli_r_2_i_verbs_mean = sum(sli_r_2_i_verbs_list)/len(sli_r_2_i_verbs_list)
    # td_r_2_i_verbs_mean = sum(td_r_2_i_verbs_list)/len(td_r_2_i_verbs_list)

    # sli_r_2_i_verbs_stdev = statistics.stdev(sli_r_2_i_verbs_list)
    # td_r_2_i_verbs_stdev = statistics.stdev(td_r_2_i_verbs_list)

    # sli_verb_utt_list = df['verb_utt'].tolist()
    # td_verb_utt_list = df['verb_utt'].tolist()

    # sli_verb_utt_mean = sum(sli_verb_utt_list)/len(sli_verb_utt_list)
    # td_verb_utt_mean = sum(td_verb_utt_list)/len(td_verb_utt_list)

    # sli_verb_utt_stdev = statistics.stdev(sli_verb_utt_list)
    # td_verb_utt_stdev = statistics.stdev(td_verb_utt_list)

    # df_res = pd.DataFrame(columns=["mean", "std"], index=["sli_mlu", "td_mlu", ""])
    # df_res.loc["sli_mlu","mean"] =  sli_mlu_mean
    # df_res.loc["sli_mlu","stdev"] =  sli_mlu_stdev

    # df_res.loc["td_mlu","mean"] =  td_mlu_mean
    # df_res.loc["td_mlu","stdev"] =  td_mlu_stdev

    # df_res.loc["sli_r_2_i_verbs","mean"] =  sli_r_2_i_verbs_mean
    # df_res.loc["sli_r_2_i_verbs","stdev"] =  sli_r_2_i_verbs_stdev

    # df_res.loc["sli_r_2_i_verbs","mean"] =  sli_r_2_i_verbs_mean
    # df_res.loc["sli_r_2_i_verbs","stdev"] =  sli_r_2_i_verbs_stdev


calculate_mean_stdev_entire()
