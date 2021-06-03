#!/usr/bin/env python3

import connexion

from bill_segmentation import encoder


def main():
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': '票据分割 API'},
                pythonic_params=True)

    app.run(port=5000)


if __name__ == '__main__':
    main()
