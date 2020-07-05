# coding:utf-8
import argparse
from vcf_file import VcfFile
from funcs import fozu


def main():
    parser = argparse.ArgumentParser(description="Replace the GT value of the samples with low coverage depth \
    to missing value in vcf file.")
    parser.add_argument('-s', '--site_name', help='The positions of values in the sample scores, must be separated by\
     ",".')
    parser.add_argument('-v', '--values', help='The value you want to set as a threshold correspond to the positions, \
                                             must be separated by ","')
    parser.add_argument('-f', '--vcf', help='\t Path to the vcf format file.', required=True)
    parser.add_argument('-p', '--prefix', help='The output file name', default='')
    parser.add_argument('-d', '--outdir', help='The directory of the output file', default='')

    args = parser.parse_args()
    fozu()

    my_vcf = VcfFile(args.site_name, args.values, args.vcf, args.prefix, args.outdir)
    my_vcf_file = my_vcf.read_file()
    my_vcf.put_missing_value(my_vcf_file)
    # print(my_vcf.out_file_prefix)


if __name__ == "__main__":
    main()
