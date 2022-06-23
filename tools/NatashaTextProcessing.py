from natasha import (Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger, NewsSyntaxParser, NewsNERTagger, PER, NamesExtractor, Doc)
from tools.CommandResult import CommandResult
import random


class NatashaProcessing:

    # Поиск команды в списке
    @staticmethod
    def search_command(commands, command):
        if command in commands:
            return command
        return None

    # Создание и применение модулей к наташе
    @staticmethod
    def get_doc_instance(text):
        segmenter = Segmenter()
        morph_vocab = MorphVocab()
        emb = NewsEmbedding()
        morph_tagger = NewsMorphTagger(emb)
        syntax_parser = NewsSyntaxParser(emb)
        ner_tagger = NewsNERTagger(emb)
        names_extractor = NamesExtractor(morph_vocab)
        doc = Doc(text)
        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)
        for token in doc.tokens:
            token.lemmatize(morph_vocab)
        doc.parse_syntax(syntax_parser)
        doc.tag_ner(ner_tagger)
        for span in doc.spans:
            span.normalize(morph_vocab)
        for span in doc.spans:
            if span.type == PER:
                span.extract_fact(names_extractor)
        return doc

    # Поиск команды
    @staticmethod
    def find_command(text, commands):
        doc = NatashaProcessing.get_doc_instance(text)
        return NatashaProcessing.get_command_answer(doc, commands)

    # Формирование ответа для имен собственных
    @staticmethod
    def get_fact_answer(text):
        doc = NatashaProcessing.get_doc_instance(text)
        answers = NatashaProcessing.get_propn_answer(doc)
        if len(answers) > 0:
            answer = random.choice(answers)
        else:
            answer = "<pre>Что-то я не очень понимаю о чём вы.</pre>"
        return CommandResult(answer, custom_data="Каталог")

    # Формирование ответа для имен собственных
    @staticmethod
    def get_propn_answer(doc):
        answers = []
        for span in doc.spans:
            if span.type == 'PER':
                answer = NatashaProcessing.get_per_answer(span)
                answers.append(answer)
            if span.type == 'LOC':
                answer = NatashaProcessing.get_loc_answer(span)
                answers.append(answer)
            if span.type == 'ORG':
                answer = NatashaProcessing.get_org_answer(span)
                answers.append(answer)
        return answers

    # Формирование ответа для имён
    @staticmethod
    def get_per_answer(item):
        answer = "<b>" + item.normal + "</b>, наверняка отличный человек, раз вы о нем говорите.\n\n" \
                                               "<i>Но может лучше закажите у нас цветы?</i>"
        return answer

    # Формирование ответа для локаций
    @staticmethod
    def get_loc_answer(item):
        answer = "<b>" + item.normal + "</b>. Говорят там красиво, я хотел бы там побывать\n\n" \
                                               "Но вы же сюда пришли не слушать мечты робота, " \
                                               "<i>а купить прекрасные цветы, верно?</i>"
        return answer

    # Формирование ответа для организаций
    @staticmethod
    def get_org_answer(item):
        answer = "Зачем вам <b>" + item.normal + "</b>? Лучше загляните в раздел \"Скидки\"."
        return answer

    # Формирование ответа
    @staticmethod
    def get_command_answer(doc, commands):
        for token in doc.tokens:
            if token.pos == 'NOUN':
                command = NatashaProcessing.search_command(commands, token.lemma)
                if command is not None:
                    return command
        return None
