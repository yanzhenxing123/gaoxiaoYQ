# import json
# import collections
import random
import time

import pandas as pd
import numpy as np
# import os
# import copy
import pymysql as pymysql
from tqdm import tqdm, tqdm_notebook
# import pickle
import re

# from sklearn.model_selection import KFold

import torch
from transformers import *
import torch.nn as nn
import torch.nn.functional as F

BERT_MODEL_PATH = './model/'

Max_LEN = 300
SEP_TOKEN_ID = 102

def filter(text):
    text = re.sub(r"[A-Za-z0-9\\=\\%\[\]\,\（\）\>\<:&lt;\/#\. -----\_]", '', text)
    text = text.replace('图片', '')
    # 删除&nbsp
    text = text.replace('\xa0', '')

    # 去除html标签
    cleanr2 = re.compile('<.*?>')
    text = re.sub(cleanr2, ' ', text)
    text = re.sub(r"💪.\u200b\\【.*】+|\\《.*》+|\\#.*#+|[./_,$&%^*()～<>+@|:❤☺~{}#]+|[——\\\，。=、：“”‘’￥……（）《》【】]", '', text)
    text = text.strip()

    return text


def seed_everything(seed):
    """
    Seeds basic parameters for reproductibility of results
    Arguments:
        seed {int} -- Number of the seed
    """
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


# create DataSet
class MyDataSet(torch.utils.data.Dataset):
    def __init__(self, df):
        self.tokenizer = BertTokenizer.from_pretrained(BERT_MODEL_PATH, cache_dir=None)
        self.data = self.get_data(df)

    def get_data(self, df):
        data = []
        row_id = 0
        for _, row in tqdm_notebook(df.iterrows()):
            content_text = row['query']
            'content token'
            text_token = self.tokenizer.tokenize(content_text)[:Max_LEN]
            token_ids = self.tokenizer.convert_tokens_to_ids(['[CLS]'] + text_token + ['[SEP]'])
            #             label = row['label']
            if len(token_ids) < Max_LEN + 2:
                token_ids += [0] * (Max_LEN + 2 - len(token_ids))
            token_ids = token_ids[:Max_LEN + 2]
            seg_ids = self.get_seg_ids(token_ids)
            data.append({'token_ids': token_ids,
                         'seg_ids': seg_ids,
                         #                         'label':label,
                         'row_id': row_id})
            row_id += 1
        return data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        feat = self.data[index]
        token_ids = torch.tensor(np.array(feat['token_ids']).astype(np.float32)).long()
        seg_ids = torch.tensor(np.array(feat['seg_ids']).astype(np.float32)).long()
        #         labels = torch.tensor(np.array(feat['label']).astype(np.float32)).long()
        return token_ids, seg_ids  # ,labels

    def get_seg_ids(self, ids):
        seg_ids = np.zeros_like(ids)
        seg_idx = 0
        for i, e in enumerate(ids):
            seg_ids[i] = seg_idx
            if e == SEP_TOKEN_ID:
                seg_idx = 1
        return seg_ids

    def collate_fn(self, batch):
        token_ids = torch.stack([x[0] for x in batch])
        seg_ids = torch.stack([x[1] for x in batch])
        #         labels = torch.stack([x[2] for x in batch])
        return token_ids, seg_ids  # , labels.squeeze()


# DataLoader
def get_loader(df, batch_size=8, is_train=False):
    ds_df = MyDataSet(df)
    loader = torch.utils.data.DataLoader(ds_df, batch_size=batch_size, shuffle=is_train, num_workers=0,
                                         collate_fn=ds_df.collate_fn, drop_last=is_train)
    loader.num = len(ds_df)
    return loader, ds_df.data


class zy_Model(nn.Module):
    def __init__(self):
        num_labels = 2
        super(zy_Model, self).__init__()
        self.model_name = 'zy_Model'
        self.auto_config = AutoConfig.from_pretrained(BERT_MODEL_PATH + 'config.json')
        self.bert_model = AutoModel.from_config(self.auto_config)
        self.zy_hidden_fc = nn.Sequential(nn.Linear(312, 2))

    def forward(self, ids, seg_ids, is_test=True):
        attention_mask = (ids > 0)
        last_seq, pooled_output = self.bert_model(input_ids=ids, token_type_ids=seg_ids, attention_mask=attention_mask)
        out = self.zy_hidden_fc(pooled_output)
        if not is_test:
            loss_fun = nn.CrossEntropyLoss()
            loss = loss_fun(out, labels)
            return loss
        else:
            return F.softmax(out, 1)[:, 1].cpu().detach().numpy().tolist()


def validation_fn(model, val_loader, is_test=False):
    model.eval()
    bar = tqdm_notebook(val_loader)
    preds = []
    real_labels = []
    print(len(bar))
    for i, (token_ids, seg_ids) in enumerate(bar):  # ,labels
        print(token_ids.size(), seg_ids.size())
        pred = model(token_ids.to(DEVICE), seg_ids.to(DEVICE), is_test=True)  # ,labels.cuda(DEVICE)
        preds.extend(pred)
    return preds
    


conn = pymysql.connect(
    host='localhost',
    user='root',
    passwd='209243',
    db='gaoxiaoYQ',
    port=3306,
    charset='utf8mb4'
)
def get_dataset():
    df = pd.read_sql("select * from `weibo` limit 10", conn)
    df = df[['weibo_id', 'raw_text', 'college', 'aspect']]
    df = df.rename(columns={'weibo_id': 'id', 'raw_text': 'query', 'college': 'collage', 'aspect': 'theme'})
    df['query'] = df['query'].apply(lambda x: filter(x))
    return df

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = zy_Model().to(DEVICE)

def main(text):
    # train data
    # test_data = get_dataset()
    # test_data = pd.read_csv('./test.csv')
    #
    # test_data = test_data[['id', 'query', 'collage', 'theme']]
    # test_data['query'] = test_data['query'].apply(lambda x: filter(x))
    #
    # SEED=2020
    # seed_everything(SEED)
    test_data = [
        {
            "id": "11205758773",
            "query": text,
            'college': "清华大学",
            "aspect": aspect
        }
    for aspect in ['师风师德', '招生就业', '校园基建', '疫情专题', '学科建设', '学术不端']
    ]


    test_data = pd.DataFrame(test_data)
    test_data['query'] = test_data['query'].apply(lambda x: filter(x))


    model_save_path = './BEST_emontion_albert_1.pkl'
    model.load_state_dict(torch.load(model_save_path,  map_location=torch.device('cpu')))

    test_loader, test_features = get_loader(test_data)

    test_preds = validation_fn(model, test_loader, test_features)
    torch.cuda.empty_cache()

    test_data['label_prob'] = test_preds
    test_data['label'] = test_data['label_prob'].apply(lambda x: 1 if x > 0.5 else 0)

    res = []
    for index, row in test_data.iterrows():
        res.append(row['label'])
    return res