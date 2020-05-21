
import os
import json
import logging
from collections import OrderedDict
from conlleval import return_report
import codecs
import tensorflow as tf

def get_logger(log_file):
    """
    定义日志方法
    :param log_file:
    :return:
    """
    # 创建一个logging的实例 logger
    logger = logging.getLogger(log_file)
    # 设置logger的全局日志级别为DEBUG
    logger.setLevel(logging.DEBUG)
    # 创建一个日志文件的handler，并且设置日志级别为DEBUG
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    # 创建一个控制台的handler，并设置日志级别为DEBUG
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # 设置日志格式
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # add formatter to ch and fh
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # add ch and fh to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger


def config_model(FLAGS, word_to_id, tag_to_id):
    config = OrderedDict()
    config['num_words'] = len(word_to_id)
    config['word_dim'] = FLAGS.word_dim
    config['num_tags'] = len(tag_to_id)
    config['seg_dim'] = FLAGS.seg_dim
    config['lstm_dim'] = FLAGS.lstm_dim
    config['batch_size'] = FLAGS.batch_size
    config['optimizer'] = FLAGS.optimizer
    config['emb_file'] = FLAGS.emb_file

    config['clip'] = FLAGS.clip
    config['dropout_keep'] = 1.0 - FLAGS.dropout
    config['optimizer'] = FLAGS.optimizer
    config['lr'] = FLAGS.lr
    config['tag_schema'] = FLAGS.tag_schema
    config['pre_emb'] = FLAGS.pre_emb
    config['model_type'] = FLAGS.model_type
    config['is_train'] = FLAGS.train
    return config

def make_path(params):
    """
    创建文件夹
    :param params:
    :return:
    """
    if not os.path.isdir(params.result_path):
        os.makedirs(params.result_path)
    if not os.path.isdir(params.ckpt_path):
        os.makedirs(params.ckpt_path)
    if not os.path.isdir('log'):
        os.makedirs('log')

def save_config(config, config_file):
    """
    保存配置文件
    :param config:
    :param config_path:
    :return:
    """
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

def load_config(config_file):
    """
    加载配置文件
    :param config_file:
    :return:
    """
    with open(config_file, encoding='utf-8') as f:
        return json.load(f)

def print_config(config, logger):
    """
    打印模型参数
    :param config:
    :param logger:
    :return:
    """
    for k, v in config.items():
        logger.info("{}:\t{}".format(k.ljust(15), v))

def create(sess, Model, ckpt_path, load_word2vec, config, id_to_word, logger):
    """
    :param sess:
    :param Model:
    :param ckpt_path:
    :param load_word2vec:
    :param config:
    :param id_to_word:
    :param logger:
    :return:
    """
    model = Model(config)

    ckpt = tf.train.get_checkpoint_state(ckpt_path)
    if ckpt and tf.train.checkpoint_exists(ckpt.model_checkpoint_path):
        logger("读取模型参数，从%s" % ckpt.model_checkpoint_path)
        model.saver.restore(sess, ckpt.model_checkpoint_path)

    else:
        logger.info("重新训练模型")
        sess.run(tf.global_variables_initializer())
        if config['pre_emb']:
            emb_weights = sess.run(model.word_lookup.read_value())
            emb_weights = load_word2vec(config['emb_file'], id_to_word, config['word_dim'], emb_weights)
            sess.run(model.word_lookup.assign(emb_weights))
            logger.info("加载词向量成功")
    return model

def test_ner(results, path):
    """
    :param results:
    :param path:
    :return:
    """
    output_file = os.path.join(path, 'ner_predict.utf8')
    with codecs.open(output_file, "w", encoding="utf-8") as f_write:
        to_write = []
        for line in results:
            for iner_line in line:
                to_write.append(iner_line + "\n")
            to_write.append("\n")
        f_write.writelines(to_write)
    eval_lines = return_report(output_file)
    return eval_lines


def save_model(sess, model, path, logger):
    """
    :param sess:
    :param model:
    :param path:
    :param logger:
    :return:
    """
    checkpoint_path = os.path.join(path, "ner.ckpt")
    model.saver.save(sess, checkpoint_path)
    logger.info('模型已经保存')

