'''
This class contains modules that process vcf files
'''
import os
import sys


class VcfFile:
    '''

    #CHROM  POS ID  REF ALT QUAL    FILTER  INFO    FORMAT  SRR5725918_sort SRR5725919_sort

    '''
    def __init__(self, site_name, vals, path_to_vcf, pre, out_dir):
        self.input_vcf_path = os.path.abspath(path_to_vcf)
        self.input_vcf_name = os.path.basename(self.input_vcf_path)
        self.out_dir = out_dir
        self.out_file_prefix = self.input_vcf_name.split('.')[:-1]
        self.out_file_prefix = '.'.join(self.out_file_prefix)
        self.out_file_prefix = pre if pre else self.out_file_prefix

        self.out_site_names = site_name.replace(',', '_')
        self.out_site_values = vals.replace(',', '_')
        self.out_file_name = self.out_file_prefix + '.{name}.{value}.vcf'.format(name=self.out_site_names, value=self.out_site_values)
        self.out_file_path = os.path.join(self.out_dir, self.out_file_name)

        if not out_dir:
            self.out_dir = os.getcwd()
        else:
            if os.path.isdir(out_dir):
                self.out_dir = out_dir
            else:
                print('The directory for output files does not exist.')
                sys.exit()

        self.site_names = site_name.upper().split(',')
        self.values = [float(value) for value in vals.split(',')]
        print('Filter using {}'.format(self.site_names))
        print('Values using {}'.format(self.values))

    def read_file(self):
        vcf_file = open(self.input_vcf_path, 'r')
        # for line in vcf_file.readlines():
        #     if not line.startswith('#'):
        #         line_lst = line.split('\t')
        #         info_lst = line_lst[8].split(':')
        #         self.sites = []
        #         for name in self.site_names:
        #             self.sites.append(info_lst.index(name))
        #         print(self.sites)
        #         break
        return vcf_file



    def put_missing_value(self, vcf_file):
        out_file = open(self.out_file_path, 'w')
        for line in vcf_file.readlines():
            # write the head of the file
            if line.startswith('#'):
                out_file.writelines(line)
            else:
                line_info_list = line.split('\t')
                sites = []
                for name in self.site_names:
                    info_lst = line_info_list[8].split(':')
                    sites.append(info_lst.index(name))

                # check if the sample contains low value
                for info_pos in range(9, len(line_info_list)):
                    sample_values = line_info_list[info_pos].split(':')
                    if sample_values[0].startswith('.'):
                        continue
                    else:
                        sample_vlaues_keep = []
                        for idx in sites:
                            sample_vlaues_keep.append(float(sample_values[idx]))
                        for i in range(len(sample_vlaues_keep)):
                            if sample_vlaues_keep[i] < self.values[i]:
                                line_info_list[info_pos] = '.' + sample_values[0][1] + '.' + line_info_list[info_pos][3:]
                                break
                #     if change_flag:
                #         line_info_list[info_pos] = '.|.' + line_info_list[info_pos][3:]
                line = '\t'.join(line_info_list)
                out_file.writelines(line)
