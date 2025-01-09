#!/usr/bin/env python3

import argparse
import os


def padding_file(input_file: str, align_num: int) -> None:
    """
    Add padding to make the file size a multiple of align_num.
    """
    filesize = os.stat(input_file).st_size
    padding = align_num - (filesize % align_num) if filesize % align_num != 0 else 0

    if padding > 0:
        with open(input_file, 'ab') as file:
            file.write(b"\x00" * padding)


def append_file(img_file: str, cert_file: str, alignment: int) -> None:
    """
    Append the contents of cert_file to img_file with alignment padding.
    """
    padding_file(img_file, alignment)
    with open(img_file, 'ab') as img, open(cert_file, 'rb') as cert:
        img.write(cert.read())


def main() -> None:
    """
    Parse arguments and execute the file appending process.
    """
    parser = argparse.ArgumentParser(description='Sign an image with provided DER certificates.')
    parser.add_argument('--alignment', type=int, required=True, help='Alignment for calculating padding.')
    parser.add_argument('--cert1', type=str, required=True, help='Path to the first certificate (cert1.der).')
    parser.add_argument('--cert2', type=str, required=True, help='Path to the second certificate (cert2.der).')
    parser.add_argument('--dtbo', type=str, required=True, help='Path to the DTBO image file.')

    args = parser.parse_args()

    append_file(args.dtbo, args.cert1, args.alignment)
    append_file(args.dtbo, args.cert2, args.alignment)


if __name__ == '__main__':
    main()
