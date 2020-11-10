from .language_parser import parser


if __name__ == "__main__":
    import pathlib

    parser.Parser("../../schemas/base_language.roset")
