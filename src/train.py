import argparse
import os

import numpy as np
import pandas as pd

from keras.models import Model
from keras.layers import Input, Embedding, GRU, Dense, TimeDistributed
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

from common.util.nlputils import tokens_to_words, clean_text, tagger
from sklearn.model_selection import train_test_split


def train(name, epochs=10, file_path=None, checkpoint=None, output=None):
    """
    Train model for an ammount of epochs and save checkpoint

    Parameters:

        name (str): name of the model to train

        epochs (int)[default=10]: number of epochs to train

        file_path (str)[default=None]: dataset file path

        checkpoint (str)[default=None]: checkpoint file path
        
        output (str)[default=None]: output file path
    """
    if not file_path:
        file_path = os.path.join("dataset", "data.csv")

    # Read CSV
    df = pd.read_csv(file_path, encoding="utf8")

    df["from"] = df["from"].apply(clean_text)
    df["reply"] = df["reply"].apply(clean_text)

    df["from"] = df["from"].apply(tagger)
    df["reply"] = df["reply"].apply(tagger)

    print(df.head())
    
    # Get both comment and reply
    from_texts = df["from"].to_list()
    reply_texts = df["reply"].to_list()

    # Concatenate texts to tokenize
    all_texts = list(from_texts)
    all_texts.extend(reply_texts)

    # Tokenize texts
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(all_texts)

    # Transform texts to token sequences
    from_seq = tokenizer.texts_to_sequences(from_texts)
    reply_seq = tokenizer.texts_to_sequences(reply_texts)

    from_seq = pad_sequences(from_seq, maxlen=300, dtype='int32', padding='post', truncating='post')
    reply_seq = pad_sequences(from_seq, maxlen=300, dtype='int32', padding='post', truncating='post')

    # Transform lists to numpy arrays to be model compatible
    x_arr = np.array(from_seq)
    y_arr = np.array(reply_seq)

    # Split to train and test arrays
    x_train, x_test, y_train, y_test = train_test_split(x_arr, y_arr, test_size=0.33)
    
    # Get number of tokens created
    vocab_size = len(tokenizer.word_index)
    print(f"Tokens Loaded: {vocab_size}")

    embed_layer = Embedding(vocab_size, 64)

    # Encoder
    encoder_input = Input(shape=(300,), dtype='int32')
    encoder_embedding = embed_layer(encoder_input)
    encoder_GRU = GRU(64, return_state=True)
    encoder_output, state_h = encoder_GRU(encoder_embedding)

    # Decoder
    decoder_input = Input(shape=(300,), dtype='int32')
    decoder_embedding = embed_layer(decoder_input)
    decoder_GRU = GRU(64, return_state=True, return_sequences=True)
    decoder_output, _ = decoder_GRU(decoder_embedding, initial_state=[state_h])

    output = TimeDistributed(Dense(vocab_size, activation='softmax'))(decoder_output)

    model = Model([encoder_input, decoder_input], output)

    print(model.summary())



def validate(name, output=None):
    pass


if __name__ == "__main__":

    # Main Parser
    parser = argparse.ArgumentParser(description="Dont Talk NLP model")
    # Subparsers Parent
    subparsers = parser.add_subparsers(help="sub-command help", dest="cmd")

    # Train Subparser
    train_parser = argparse.ArgumentParser(description="Train Section", add_help=False)
    train_parser.add_argument("--name", required=True, help="name of the model to train")
    train_parser.add_argument("--epochs", type=int, help="number of epochs to train the model for")
    train_parser.add_argument("--file_path", help="dataset file path")
    train_parser.add_argument("--checkpoint", help="checkpoint path to resume ('latest' to resume from the most recent checkpoint)")
    train_parser.add_argument("--output", help="manual output path for the saved checkpoint")

    # Validate Subparser
    val_parser = argparse.ArgumentParser(description="Validation Section", add_help=False)
    val_parser.add_argument("--name", required=True, help="name of the model to validate")
    val_parser.add_argument("--output", help="generate log at given path")

    # Add subparsers to parent
    subparsers.add_parser("train", parents=[train_parser])
    subparsers.add_parser("validate", parents=[val_parser])

    function = None
    kwargs = vars(parser.parse_args())
    
    # Decide which function to call
    cmd = kwargs["cmd"]
    if cmd == "train":
        function = train
    elif cmd == "validate":
        function = validate

    # Call selected function
    if function:
        del kwargs["cmd"]
        function(**kwargs)
    else:
        print("Invalid command!")
