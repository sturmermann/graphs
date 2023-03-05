import argparse
def argsMain():
    parser = argparse.ArgumentParser(
                    prog = 'Optical Graph Recognition',
                    description = 'University project of Hermann \
                    Nestermann that allows recognite graphs from visual to matrix',
                    epilog = '_/ bottom of help \_')
    parser.add_argument('filename', help = "Filename, nothing more")
    return parser