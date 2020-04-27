#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Austin
# date: 2020/4/24
import re
from bert_base.client import BertClient
from general_tools.database_handle import bert_153


class ContactParser:
    pat1 = '\d{11}'
    pat2 = '((\d{3})?-?\d{8}(-\d{3,4})*)'

    def __init__(self, contact_info):
        self.contact_info = contact_info
        self.length = len(self.contact_info)
        self.phones = []
        self.contact = []

    def extract_phone(self):
        phones1 = re.findall(self.pat1, self.contact_info)
        left = self.contact_info
        for phone in phones1:
            self.phones.extend(phone)
            left = self.contact_info.replace(phone, '')
        left = left.replace('转', '-').replace('/', '-').replace(')', '-').replace('）', '-')
        phones2 = re.findall(self.pat2, left)
        for phone in phones2:
            self.phones.append(phone[0])

    def complete_contact(self, a_contact, loc):
        identity_1 = ['工']
        identity_2 = ['先生', '小姐', '女士', '老师', '警官', '科长', '部长', '站长', '主任', '医生', '经理']
        if loc + 3 <= self.length and self.contact_info[loc+1:loc+3] in identity_2:
            a_contact += self.contact_info[loc+1:loc+3]
        elif loc + 1 < self.length and self.contact_info[loc+1] in identity_1:
            a_contact += self.contact_info[loc + 1]
        if len(a_contact) == 1:
            a_contact += 'XX'
        return a_contact

    def contact_from_pos(self, pos_list):
        a_contact = ''
        loc = 0
        for i in range(self.length):
            if pos_list[i] == 'B-PER':
                if a_contact:
                    a_contact = self.complete_contact(a_contact, loc)
                    self.contact.append(a_contact)
                a_contact = self.contact_info[i]
                loc = i
            elif pos_list[i] == 'I-PER':
                a_contact += self.contact_info[i]
                loc = i
            if pos_list[i] != 'B-PER' and i == self.length - 1:
                if a_contact:
                    a_contact = self.complete_contact(a_contact, loc)
                    self.contact.append(a_contact)

    def extract_contact(self):
        with BertClient(**bert_153) as bc:
            contact_info = self.contact_info.replace(' ', '，')
            if contact_info:
                poses = list(bc.encode([list(contact_info)], is_tokenized=True)[0])
                print(poses)
                self.contact_from_pos(poses)


if __name__ == '__main__':
    cp = ContactParser('刘可心张迎春 010-69323298 卢科长')
    cp.extract_phone()
    cp.extract_contact()
    print(cp.contact, cp.phones)
