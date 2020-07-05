import argparse


def build_model(name=None, output=None):
    pass


def train(name, epochs=10, file_path=None, checkpoint=None, output=None):
    pass


def validate(name, output=None):
    pass


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Dont Talk NLP model")
    subparsers = parser.add_subparsers(help="sub-command help", dest="cmd")

    model_parser = argparse.ArgumentParser(description="Model Section", add_help=False)
    model_parser.add_argument("--name", help="model's name")
    model_parser.add_argument("--output", help="manual model output")

    train_parser = argparse.ArgumentParser(description="Train Section", add_help=False)
    train_parser.add_argument("--name", required=True, help="name of the model to train")
    train_parser.add_argument("--epochs", type=int, help="number of epochs to train the model for")
    train_parser.add_argument("--file_path", help="dataset file path")
    train_parser.add_argument("--checkpoint", help="checkpoint path to resume ('latest' to resume from the most recent checkpoint)")
    train_parser.add_argument("--output", help="manual output path for the saved checkpoint")

    val_parser = argparse.ArgumentParser(description="Validation Section", add_help=False)
    val_parser.add_argument("--name", required=True, help="name of the model to validate")
    val_parser.add_argument("--output", help="generate log at given path")

    subparsers.add_parser("build", parents=[model_parser])
    subparsers.add_parser("train", parents=[train_parser])
    subparsers.add_parser("validate", parents=[val_parser])

    function = None
    kwargs = vars(parser.parse_args())
    
    cmd = kwargs["cmd"]
    if cmd == "build":
        function = build_model
    elif cmd == "train":
        function = train
    elif cmd == "validate":
        function = validate

    if function:
        del kwargs["cmd"]
        function(**kwargs)
    else:
        print("Invalid command!")
