#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Version : Python 3.6
import json
import os
import sklearn.metrics
import torch
import torch.nn.functional as F
import numpy as np
from tqdm import tqdm


class Eval(object):
    def __init__(self, class_num, config, id2rel):
        self.class_num = class_num
        self.device = config.device
        self.id2rel = id2rel

    def __scorer(self, all_probs, labels):
        all_probs = np.concatenate(all_probs, axis=0).\
            reshape(-1, self.class_num).astype(np.float32)
        labels = np.concatenate(labels, axis=0).\
            reshape(-1).astype(np.int64)

        facts_num = int(np.count_nonzero(labels))
        pred_result = []
        for i in range(all_probs.shape[0]):
            for j in range(1, self.class_num):
                pred_result.append(
                    {
                        'prob': all_probs[i][j],
                        'flag': int(j == labels[i])
                    }
                )
        

        sorted_pred_result = sorted(
            pred_result, key=lambda x: x['prob'], reverse=True)
        precision = []
        recall = []
        correct = 0
        for i, item in enumerate(sorted_pred_result):
            correct += item['flag']
            precision.append(float(correct) / float(i + 1))
            recall.append(float(correct) / float(facts_num))
        auc = sklearn.metrics.auc(x=recall, y=precision)
        return auc, precision, recall

    def evaluate(self, model, data_loader):
        all_probs = []
        labels = []
        total_loss = 0.0
        with torch.no_grad():
            model.eval()
            data_iterator = tqdm(data_loader, desc='Eval')
            for step, (data, label, scope) in enumerate(data_iterator):
                data = data.to(self.device)
                label = label.to(self.device)

                loss, probs = model(data, scope, label)
                total_loss += loss.item()

                probs = probs.cpu().detach().numpy().\
                    reshape((-1, self.class_num))
                label = label.cpu().detach().numpy().reshape((-1, 1))
                all_probs.append(probs)
                labels.append(label)

        eval_loss = total_loss / len(data_loader)
        auc, precision, recall = self.__scorer(all_probs, labels)
        return auc, eval_loss, precision, recall

    def predict(self, model, data_loader):
        output = []
        with torch.no_grad():
            # data_iterator = tqdm(data_loader, desc='Eval')
            # for step, (data, entity) in enumerate(data_iterator):
            print(data_loader)
            for a in iter(data_loader):
                for i in range(len(list(a))):
                    data, entity = list(a)[i]
                    data = data.to(self.device)
                    _, probs = model(data)

                    relid = np.argmax(probs)

                    output.append([entity[0].split('\t')[:3], self.id2rel[int(relid)]])

            output = sorted(output, key=lambda x: x[1])

            with open('predict_output.json', 'w') as outfile:
                json.dump(output, outfile, indent=4)

            print(output)
